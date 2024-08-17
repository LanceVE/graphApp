def bwt(input_string):
    input_string += '$'
    rotations = [input_string[i:] + input_string[:i] for i in range(len(input_string))]
    rotations_tuple = tuple(rotations)
    rotations.sort()
    rotations_sort = tuple(rotations)

    bwt_transform = ''.join(rotation[-1] for rotation in rotations)

    return [rotations_tuple, rotations_sort, bwt_transform]
