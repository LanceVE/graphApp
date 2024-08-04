import heapq

class huffman:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __eq__(self, other):
        return self.freq == other.freq

def build_huffman_tree(freq_dict):
    heap = []
    for char, freq in freq_dict.items():
        heapq.heappush(heap, huffman(char, freq))
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = huffman(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

def encode_huffman_tree(node, prefix="", code_map={}):
    if node:
        if node.char:
            code_map[node.char] = prefix
        encode_huffman_tree(node.left, prefix + "0", code_map)
        encode_huffman_tree(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(letters, frequencies):
    freq_dict = dict(zip(letters, frequencies))

    root = build_huffman_tree(freq_dict)

    code_map = encode_huffman_tree(root)

    encoded_message = "".join(code_map[char] for char in letters)

    return encoded_message, code_map
