
from collections import deque

def graphreader(file_path):
    graph = {}
    nodeCount = 0
    with open(file_path, 'r') as file:
        for line in file:
            node_and_edges = line.strip().split(' ')
            node = node_and_edges[0]
            edges_dict = {}
            for edge in node_and_edges[1:]:
                end_node, weight = edge.split(':')
                edges_dict[f'{int(end_node)}'] = int(weight)
            graph[node] = edges_dict
            nodeCount += 1
    return graph, nodeCount


def graphreaderStartNode(file_path):
    graph = {}
    nodeCount = 0
    startNode = None 
    with open(file_path, 'r') as file:
        # Read the first line to determine the startNode
        startNode = file.readline().strip()
        
        for line in file:
            node_and_edges = line.strip().split(' ')
            node = node_and_edges[0]
            edges_dict = {}
            for edge in node_and_edges[1:]:
                end_node, weight = edge.split(':')
                edges_dict[end_node] = int(weight)
            graph[node] = edges_dict
            nodeCount += 1
    return graph, nodeCount, startNode


def graphreaderNeg(file_path):
    graph = {}
    nodeCount = 0
    with open(file_path, 'r') as file:
        for line in file:
            node_and_edges = line.strip().split(' ')
            node = node_and_edges[0]
            edges_dict = {}
            for edge in node_and_edges[1:]:
                if ':' in edge:
                    end_node, weight = edge.split(':')
                    edges_dict[f'{int(end_node)}'] = int(weight)
                elif '-' in edge:
                    end_node, weight = edge.split('-')
                    edges_dict[f'{int(end_node)}'] = -int(weight)
            graph[node] = edges_dict
            nodeCount += 1
    return graph, nodeCount

def readKnapSack(file_path):
    with open(file_path, 'r') as file:
        data = file.read().split()
        first_number = int(data.pop(0))
        first_array = []
        second_array = []
        for item in data:
            key, value = item.split(':')
            first_array.append(int(key))
            second_array.append(int(value))
        n = len(second_array)
        return first_number, first_array, second_array, n
    

def read2LineText(file_path):
    with open(file_path, 'r') as file:
        seq1 = ""
        seq2 = ""
        for i, line in enumerate(file):
            if i == 0:
                seq1 = line.strip()
            elif i == 1:
                seq2 = line.strip()
                break
        return seq1, seq2

def readIntervals(file_Path):
    intervals = []
    with open(file_Path, 'r') as file:
        data = file.read().strip().split()
        for segment in data:
            parts = segment.split(':')
            if len(parts) == 2:
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                intervals.append((start, end))
                
    return intervals

def readHuffman(file_path):
    letters = []
    numbers = []
    with open(file_path, 'r') as file:
        data = file.read().strip().split()
        for segment in data:
            parts = segment.split(':')
            if len(parts) == 2:
                letter = parts[0].strip()
                number = int(parts[1].strip())
                letters.append(letter)
                numbers.append(number)
    
    return letters, numbers


def readNumbers(file_path):
    numbers = []
    with open(file_path, 'r') as file:
        data = file.read().strip().split(',')
        for num_str in data:
                number = int(num_str.strip())
                numbers.append(number)
    return numbers



def readSelectNumbers(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        first_entry = int(lines[0].strip())
        second_line_numbers = [int(num_str.strip()) for num_str in lines[1].strip().split(',')]
        print(first_entry)

        print(second_line_numbers)
        return [first_entry, second_line_numbers]
def readQueue(file_path):
    queue = deque()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('MS'):
                _, number = line.split()
                queue.append(('MS', int(number)))
            elif line.startswith('U'):
                parts = line.split()
                queue.append(('U', (int(parts[1]), int(parts[2]))))
            elif line.startswith('F'):
                _, number = line.split()
                queue.append(('F', int(number)))
    return queue

def readBWT(file_path):
    with open(file_path, 'r') as file:
        string = file.read().strip()  
    return string


def readWords(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words
