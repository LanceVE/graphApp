def isMajority(arr, n):
    candidate = -1
    votes = 0

    states = []

    for i in range(n):
        if votes == 0:
            candidate = arr[i]
            votes = 1
        else:
            if arr[i] == candidate:
                votes += 1
            else:
                votes -= 1
        
        states.append((i, candidate, votes))


    count = 0
    for i in range(n):
        if arr[i] == candidate:
            count += 1

    states.append(('Final', candidate, count))
    print(count)

    if count > n // 2:
        return states, candidate
    else:
        return states, candidate