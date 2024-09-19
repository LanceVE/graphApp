def bubbleSort(numbers):
    length = len(numbers)
    rows = []
    for i in range(length):
        for j in range(length - i - 1):
            if numbers[j] > numbers[j+1]:
                rows.append((numbers[:], j, j+1, 1))
                numbers[j], numbers[j+1] = numbers[j + 1], numbers[j]
            else:
                rows.append((numbers[:], j, j+1, 0))
    return rows