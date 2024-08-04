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
    
    if depth <= max_depth:
        depth_arrays.append((depth, list(array)))

    if len(array) <= 1:
        return array, depth_arrays

    mid = len(array) // 2


    leftArray, left_depth_arrays = mergeSort(array[:mid], depth + 1, max_depth, depth_arrays[:])
    rightArray, right_depth_arrays = mergeSort(array[mid:], depth + 1, max_depth, depth_arrays[:])
    

    combined_depth_arrays = left_depth_arrays + right_depth_arrays

    return merge(leftArray, rightArray), combined_depth_arrays
