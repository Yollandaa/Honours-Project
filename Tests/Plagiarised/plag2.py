import math


def search_binary(collection, target_value):
    lower_bound = 0
    upper_bound = len(collection) - 1
    position = -1

    while upper_bound >= lower_bound and position == -1:
        middle = int(math.floor((upper_bound + lower_bound) / 2.0))

        # Debug statement to trace computation
        print(
            f"Searching at position {middle} with bounds ({lower_bound}, {upper_bound})"
        )

        if collection[middle] == target_value:
            position = middle
        elif collection[middle] > target_value:
            upper_bound = middle - 1
        else:
            lower_bound = middle + 1

    return position


# Sample data for demonstration
data_list = [22, 25, 21, 29, 21, 217, 2]
# Test cases
print(search_binary(data_list, 21))  # Expected output: 4
print(search_binary(data_list, 12))  # Expected output: -1
