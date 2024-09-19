def merge(leftArray, rightArray):
    sortedArray = []
    i = j = 0

    while i < len(leftArray) and j < len(rightArray):
        if leftArray[i] <= rightArray[j]:
            sortedArray.append(leftArray[i])
            i += 1
        else:
            sortedArray.append(rightArray[j])
            j += 1

    while i < len(leftArray):
        sortedArray.append(leftArray[i])
        i += 1

    while j < len(rightArray):
        sortedArray.append(rightArray[j])
        j += 1

    return sortedArray

def mergeSort(array, depth=0, max_depth=3, depth_arrays=None):
    if depth_arrays is None:
        depth_arrays = []

    # Record the current state of the array at this depth
    if depth <= max_depth:
        depth_arrays.append((depth, list(array)))

    if len(array) <= 1:
        return array, depth_arrays

    mid = len(array) // 2

    # Recursively sort the two halves and collect depth information
    leftArray, left_depth_arrays = mergeSort(array[:mid], depth + 1, max_depth, depth_arrays[:])
    rightArray, right_depth_arrays = mergeSort(array[mid:], depth + 1, max_depth, depth_arrays[:])

    # Combine the depth information from both sides
    combined_depth_arrays = left_depth_arrays + right_depth_arrays

    return merge(leftArray, rightArray), combined_depth_arrays




def reverse_merge_sort(split_data):
    def merge(left, right):
        # Merging two sorted lists into one sorted list
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_all_levels(levels):
        results = []
        while len(levels) > 1:
            results.append(levels)
            next_level = []
            for i in range(0, len(levels), 2):
                if i + 1 < len(levels):
                    merged = merge(levels[i], levels[i + 1])
                else:
                    merged = levels[i]
                next_level.append(merged)
            levels = next_level
        results.append(levels)  # Append the final level
        return results
    
    # Extract levels from split data
    level4 = split_data[3]
    level3 = split_data[2]
    level2 = split_data[1]
    level1 = split_data[0]
    
    # Merge Level 4 to get Level 3
    level3_results = merge_all_levels(level4)
    level3_result = level3_results[1]  # The second element is the result after one merge
    
    # Merge Level 3 to get Level 2
    level2_results = merge_all_levels(level3_result)
    level2_result = level2_results[1]  # The second element is the result after one merge
    
    # Merge Level 2 to get Level 1
    level1_results = merge_all_levels(level2_result)
    level1_result = level1_results[1]  # The second element is the result after one merge
    

    
    # Collect all levels
    all_levels = [level3_result, level2_result, level1_result, ]
    
    return all_levels




def swap_positions(tuples_list, swaps):
    for index_a, index_b in swaps:
        # Swap elements in the list
        tuples_list[index_a], tuples_list[index_b] = tuples_list[index_b], tuples_list[index_a]
    
    return tuples_list