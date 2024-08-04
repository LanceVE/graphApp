def insertionSort(numbers):
    length = len(numbers)
    rows = []
    if length <= 1:
        return rows
    
    for i in range(1, length):
        key = numbers[i]
        j = i - 1
        swap = False
        while j >= 0 and key < numbers[j]:
            rows.append((numbers[:], j, j+1))
            numbers[j+1] = numbers[j]
            j -= 1
            swap = True
        numbers[j+1] = key
        if swap:
            rows.append((numbers[:], j, j+1))
    print(rows) 
    return rows
