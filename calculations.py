import difflib
from zss import simple_distance, Node
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Bio import pairwise2

PLAGIARISM_THRESHOLD = 60


def structural_analysis(
    original_lines,
    normalized_original,
    graph1,
    plagiarized_lines,
    normalized_plagiarized,
    graph2,
):
    # Base Case
    if nx.is_isomorphic(graph1, graph2):
        print("The two codes are structurally similar.")
    else:
        print("The two codes are structurally dissimilar.")

    # Calculation of structural similarity
    similarity_score, similar_lines = calculate_weighted_similarity_and_report_lines(
        normalized_original, normalized_plagiarized
    )

    print("Similarity score: ", similarity_score)
    # if similarity_score > PLAGIARISM_THRESHOLD:
    print("Potential plagiarism detected.")
    print("\n Similar lines: ", len(similar_lines))
    for line1, line2 in similar_lines:
        print(f"Code 1: {original_lines[line1]}\nCode 2: {plagiarized_lines[line2]}\n")
    # else:
    #     print("No plagiarism detected.")


def calculate_weighted_similarity_and_report_lines(graph1, graph2):
    print("Weighted Something")
    print(graph1)
    total_nodes = len(graph1) + len(graph2)
    matching_nodes = 0
    similar_lines = []

    all_nodes1 = set(graph1.keys())
    all_nodes2 = set(graph2.keys())

    common_nodes = all_nodes1.intersection(all_nodes2)

    for node in common_nodes:
        if set(graph1[node]) == set(graph2[node]):
            matching_nodes += 1
            similar_lines.append((node, node))

    similarity_score = (2 * matching_nodes / total_nodes) * 100

    return similarity_score, similar_lines


#
# def calculate_token_similarity(norm_code1, norm_code2):
#     tokens1 = norm_code1.split()
#     tokens2 = norm_code2.split()

#     similarity_ratio = difflib.SequenceMatcher(None, tokens1, tokens2).ratio()
#     return similarity_ratio * 100


def calculate_token_similarity(norm_code1, norm_code2):
    # Create a list containing both code snippets
    codes = [norm_code1, norm_code2]

    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Convert the code snippets to TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform(codes)

    # Compute cosine similarity between the two vectors
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Return the similarity as a percentage
    return similarity[0][0] * 100


def flatten_trace(trace):
    # Convert each dictionary in the trace to a string
    trace_str_list = [str(item) for item in trace]
    return " ".join(trace_str_list)


def calculate_execution_trace_similarity(trace1, trace2):
    # Convert execution traces to strings for alignment
    trace1_str = flatten_trace(trace1)
    trace2_str = flatten_trace(trace2)

    # Perform sequence alignment
    alignments = pairwise2.align.globalxx(trace1_str, trace2_str)

    # Get the best alignment score
    best_alignment = alignments[0]
    score = best_alignment[2]  # Alignment score
    max_score = max(len(trace1_str), len(trace2_str))  # Maximum possible score

    similarity_percentage = (score / max_score) * 100

    return similarity_percentage


def calculate_weighted_average(
    static_similarity, dynamic_similarity, weight_static=0.4, weight_dynamic=0.6
):
    return (static_similarity * weight_static) + (dynamic_similarity * weight_dynamic)
