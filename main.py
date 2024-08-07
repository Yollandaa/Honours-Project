from static_analysis import *
from normalize_code import normalize_code
from dynamic_analysis import *
from calculations import *
from itertools import combinations


def read_file_content(filename):
    with open(filename, "r") as file:
        return file.read()


def write_file_content(filename, content):
    filepath = os.path.join("./Results", filename)
    with open(filepath, "w") as file:
        file.write(content)


def main(files):
    # Generate all pairwise combinations of files
    file_pairs = list(combinations(files, 2))  # This creates tuples of unique pairs
    print(
        "===================================================================================================================================================================================="
    )
    for file1, file2 in file_pairs:
        python_code1 = read_file_content(file1)
        python_code2 = read_file_content(file2)

        # Normalize the code
        normalized_code1 = normalize_code(python_code1)
        normalized_code2 = normalize_code(python_code2)

        # Write normalized code to new files with unique names
        write_file_content(f"normalized_{os.path.basename(file1)}", normalized_code1)
        write_file_content(f"normalized_{os.path.basename(file2)}", normalized_code2)

        print(
            f"Normalized Code for {file1} has been written to 'normalized_{os.path.basename(file1)}'"
        )
        print(
            f"Normalized Code for {file2} has been written to 'normalized_{os.path.basename(file2)}'"
        )

        #   Build AST graphs
        graph1 = build_ast_graph(python_code1)
        graph2 = build_ast_graph(python_code2)

        print(
            "---------------------------------- Structural Analysis: Static --------------------------------------------"
        )
        static_birthmarks1, static_lines1 = normalize_ast(graph1, python_code1)
        static_birthmarks2, static_lines2 = normalize_ast(graph2, python_code2)
        structural_analysis(
            static_lines1,
            static_birthmarks1,
            graph1,
            static_lines2,
            static_birthmarks2,
            graph2,
        )

        print(
            "--------------------------------- Token Similarity: Static Side ----------------------------------"
        )
        # Calculate token similarity
        static_token_similarity = calculate_token_similarity(
            normalized_code1, normalized_code2
        )
        print(normalized_code1)
        print(f"Token Similarity: {static_token_similarity:.2f}%")

        print(
            "------------------------------------ Tracing Analysis --------------------------------"
        )
        # Trace and compare execution traces
        start_tracing()
        exec(normalized_code1, globals())
        stop_tracing("runtime_data1.json")
        trace1 = load_runtime_data("runtime_data1.json")

        start_tracing()
        exec(normalized_code2, globals())
        stop_tracing("runtime_data2.json")
        trace2 = load_runtime_data("runtime_data2.json")

        # Tokenize the execution traces
        # trace_tokens1 = tokenize_trace(trace1)
        # trace_tokens2 = tokenize_trace(trace2)

        print(
            "--------------------------------- Token Similarity: Dynamic Side ----------------------------------"
        )
        # print(trace_tokens1)
        # print()
        # print(trace_tokens2)

        # Calculate token similarity for dynamic execution traces
        dynamic_token_similarity = calculate_execution_trace_similarity(trace1, trace2)
        print(f"Dynamic Token Similarity: {dynamic_token_similarity:.2f}%")

        print(
            "--------------------------------- Call graphs Similarity: Dynamic Side ----------------------------------"
        )

        call_sequences1 = analyze_runtime_data(trace1)
        call_sequences2 = analyze_runtime_data(trace2)

        exec(python_code1)
        generate_call_graph(python_code1, "call_graph_1.png")
        exec(python_code2)
        generate_call_graph(python_code2, "call_graph_2.png")

        are_isomorphic = compare_call_graphs(call_sequences1, call_sequences2)
        print(f"Call graphs are isomorphic: {are_isomorphic}")

        print(
            "--------------------------------- Combined Similarity: Static and Dynamic Side ----------------------------------"
        )
        # Combine static and dynamic similarities
        combined_similarity = calculate_weighted_average(
            static_token_similarity, dynamic_token_similarity
        )
        print(f"Combined Similarity: {combined_similarity:.2f}%")

        # Determine potential plagiarism
        if combined_similarity > PLAGIARISM_THRESHOLD:
            print("Potential plagiarism detected.")
        else:
            print("No plagiarism detected.")


if __name__ == "__main__":
    # Check if at least two file paths are provided
    if len(sys.argv) < 3:
        print("Usage: python plagiarism_checker.py <file1> <file2> ...")
    else:
        # Pass all file paths to the main function, excluding the script name
        main(sys.argv[1:])
