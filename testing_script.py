import subprocess
import os
import difflib


def extract_code_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def analyze_similarity(code1, code2):
    diff = difflib.unified_diff(code1.splitlines(), code2.splitlines())
    return "\n".join(diff)


def run_similarity_analysis(commit_hashes):
    base_dir = os.getcwd()
    results = []

    for commit in commit_hashes:
        subprocess.run(["git", "checkout", commit], check=True)

        # Extract code from relevant files
        # Modify this according to your file structure and requirements
        code_files = ["pandas/core/frame.py", "pandas/core/series.py"]  # Example files
        for file_path in code_files:
            if os.path.exists(file_path):
                code = extract_code_from_file(file_path)
                results.append((commit, file_path, code))

    # Compare code across different commits
    for i in range(len(results)):
        commit1, file1, code1 = results[i]
        for j in range(i + 1, len(results)):
            commit2, file2, code2 = results[j]
            if file1 == file2:
                similarity = analyze_similarity(code1, code2)
                print(f"Commit {commit1} vs Commit {commit2} - File: {file1}")
                print(similarity)


if __name__ == "__main__":
    commit_hashes = ["commit_hash1", "commit_hash2", "commit_hash3"]
    run_similarity_analysis(commit_hashes)
