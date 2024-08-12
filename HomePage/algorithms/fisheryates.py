from random import randint
def randomize(arr, n):
    states = [] 
    for i in range(n-1, 0, -1):
        j = randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
        states.append((arr.copy(), i))
    return states