import random

def one_pass_two_index_partition(A, left, right, pivot_index): #Algorithm 7
    i = left
    lower_partition_index = left
    upper_partition_index = right
    pivot = A[pivot_index]
    
    while i <= upper_partition_index:
        if A[i] < pivot:
            A[lower_partition_index], A[i] = A[i], A[lower_partition_index]
            i += 1
            lower_partition_index += 1
        elif A[i] > pivot: 
            A[upper_partition_index], A[i] = A[i], A[upper_partition_index]
            upper_partition_index -= 1
        else:
            i += 1
    
    return lower_partition_index, upper_partition_index

def quicksort(A, left, right, states=None):
    if states is None:
        states = []
    
    state_info = {
        'array': A.copy(),
        'left': left,
        'right': right,
        'pivot': None,
        'pivot_index': None,
        'partition_indexes': None
    }
    states.append(state_info)
    
    if left < right:
        pivot_index = generate_pivot(A, left, right)
        pivot_value = A[pivot_index]
        partition_indexes = one_pass_two_index_partition(A, left, right, pivot_index)
        
        state_info['pivot'] = pivot_value
        state_info['pivot_index'] = pivot_index
        state_info['partition_indexes'] = partition_indexes
        
        quicksort(A, left, partition_indexes[0] - 1, states)
        quicksort(A, partition_indexes[1] + 1, right, states)
    
    return states


def quickselect(A, left, right, k, states=None):
    if states is None:
        states = []
    
    state_info = {
        'array': A.copy(),
        'left': left,
        'right': right,
        'pivot': None,
        'pivot_index': None,
        'partition_indexes':None
    }
    states.append(state_info)
    
    if left == right:
        return A[left]
    
    pivot_index = generate_pivot(A, left, right)
    pivot_value = A[pivot_index]
    partition_indexes = one_pass_two_index_partition(A, left, right, pivot_index)
    
    state_info['pivot'] = pivot_value
    state_info['pivot_index'] = pivot_index
    state_info['partition_indexes'] = partition_indexes
    
    if partition_indexes[0] <= k <= partition_indexes[1]:
        return states
    elif k < partition_indexes[0]:
        return quickselect(A, left, partition_indexes[0] - 1, k, states)
    else:
        return quickselect(A, partition_indexes[1] + 1, right, k, states)


def generate_pivot(A, left, right):
    return random.randint(left, right)