def countSort(input_array):
    M = max(input_array)
 
    countArr = [0] * (M + 1)
 
    for num in input_array:
        countArr[num] += 1
 
    for i in range(1, M + 1):
        countArr[i] += countArr[i - 1]
 
    outArr = [0] * len(input_array)
 
    for i in range(len(input_array) - 1, -1, -1):
        outArr[countArr[input_array[i]] - 1] = input_array[i]
        countArr[input_array[i]] -= 1
    return outArr, countArr