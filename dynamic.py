import sys
import json
import trace

# Dictionary to store runtime data
runtime_data = []


# Tracing function
def trace_calls(frame, event, arg):
    if event == "call":
        func_name = frame.f_code.co_name
        func_line_no = frame.f_lineno
        func_filename = frame.f_code.co_filename
        runtime_data.append(
            {
                "event": "call",
                "func_name": func_name,
                "line_no": func_line_no,
                "filename": func_filename,
            }
        )
    elif event == "return":
        func_name = frame.f_code.co_name
        runtime_data.append({"event": "return", "func_name": func_name})
    return trace_calls


# Function to save runtime data
def save_runtime_data(filepath):
    with open(filepath, "w") as f:
        json.dump(runtime_data, f, indent=4)


# Enable tracing
def start_tracing():
    sys.settrace(trace_calls)


# Disable tracing and save the data
def stop_tracing(filepath):
    sys.settrace(None)
    save_runtime_data(filepath)


def load_runtime_data(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def analyze_runtime_data(runtime_data):
    call_sequences = []
    current_sequence = []

    for event in runtime_data:
        if event["event"] == "call":
            current_sequence.append(event["func_name"])
        elif event["event"] == "return":
            call_sequences.append(current_sequence)
            current_sequence = []

    return call_sequences


# if __name__ == "__main__":
#     # Sample code to be traced
#     python_code = """
# import math

# def search_binary(collection, target_value):
#     lower_bound = 0
#     upper_bound = len(collection) - 1
#     position = -1

#     while upper_bound >= lower_bound and position == -1:
#         middle = int(math.floor((upper_bound + lower_bound) / 2.0))

#         print(f"Searching at position {middle} with bounds ({lower_bound}, {upper_bound})")

#         if collection[middle] == target_value:
#             position = middle
#         elif collection[middle] > target_value:
#             upper_bound = middle - 1
#         else:
#             lower_bound = middle + 1

#     return position

# def sum_of_list(lst):
#     total = 0
#     for num in lst:
#         total += num
#     return total

# data_list = [2, 5, 7, 9, 11, 17, 222]
# print(search_binary(data_list, 11))
# print(search_binary(data_list, 12))
# print(sum_of_list(data_list))
# """

#     start_tracing()
#     exec(python_code)
#     stop_tracing("runtime_data.json")
