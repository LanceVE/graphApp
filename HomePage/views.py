from django.shortcuts import render
from django.conf import settings
from .forms import numbersForm, numbersFormDijk, numbersFormKnapsack, numbersFormLCS, stringFormKMP, huffmanForm, csvForm, GraphForm, ImageForm
from HomePage.algorithms.insertionSort import insertionSort
from HomePage.algorithms.bubbleSort import bubbleSort
from HomePage.algorithms.dijkstras import dijkstras, getDijkEdgeColors, getDijkNodeColors
from HomePage.algorithms.knapsackDP import knapsackDP, buildTable
from HomePage.algorithms.lcs import lcs
from HomePage.algorithms.kruskals import kruskals
from HomePage.algorithms.prims import prims
from HomePage.algorithms.intervalGreed import intervalGreed, to_military_time
from HomePage.algorithms.kmp import kmp, compute_failure_function
from HomePage.algorithms.bellmanford import bellmanford
from HomePage.algorithms.floydwarshall import floydwarshall
from HomePage.algorithms.huffman import huffman_encode
from HomePage.algorithms.unionfind import UnionFind 
from HomePage.algorithms.trie import trieBuild
from HomePage.algorithms.rabinkarp import search
from HomePage.algorithms.bwt import bwt
from HomePage.algorithms.boyermoore import isMajority
from HomePage.algorithms.fisheryates import randomize
from HomePage.algorithms.countsort import countSort
from HomePage.algorithms.mergesort import mergeSort, reverse_merge_sort, swap_positions
from HomePage.algorithms.MIS import maximumindependentset, build_and_save_graphMIS
from HomePage.algorithms.quickstuff import quicksort, quickselect
from HomePage.algorithms.maxincreaseDP import maxincrease
from HomePage.helper.csvreader import graphreader, graphreaderNeg, readKnapSack, read2LineText, readIntervals, readHuffman, readNumbers, readQueue, readBWT, readWords, readSelectNumbers, graphreaderStartNode
from django.shortcuts import render
from django.http import HttpResponse
from .models import GraphModel

from collections import defaultdict
from typing import List, Tuple


import matplotlib
matplotlib.use('Agg')  
import networkx as nx
import matplotlib.pyplot as plt
import datetime
from django.core.files.storage import FileSystemStorage
import os


def new_home(request):  
    form = numbersForm()
    formDijk = numbersFormDijk()
    formKnapsack = numbersFormKnapsack()
    formLCS = numbersFormLCS()
    formKMP = stringFormKMP()
    formHuffman = huffmanForm()
    formCSV = csvForm()
    formTest = stringFormKMP()
    return render(request, "new_home.html", {'form':form, 'formCSV':formCSV, 'formDijk':formDijk, 'formKnapsack': formKnapsack, 'formLCS': formLCS,'formKMP':formKMP, 'formHuffman':formHuffman , 'formTest':formTest } ) 

#Interemediate Page
def upload_graph(request):
    if request.method == 'POST':
        form = GraphForm(request.POST, request.FILES)
        imageform = ImageForm(request.POST, request.FILES)

        print("FORM", form)
        print("IMAGEFORM", imageform)
        full_url = request.get_full_path()
        algo = extract_value_from_url(full_url)
        displayImage = False
        updateText = False
        if algo in ['Dijkstra','Kruskal', 'Bellmanford', 'FloydWarshall', 'Prims', 'MaxIndependentSet', 'Graph']:
            displayImage = True
            updateText = True
        if algo in ['Knapsack','KMP', 'Huffman', 'InsertionSort', 'BubbleSort', 'UnionFind', 'Trie', 'Rabinkarp', 'FisherYate', 'CountSort', 'MergeSort',]:
            updateText = True
       
       
       
        if form.is_valid():
            instance = form.save()
            url = instance.graph.path
            if displayImage == True:
                graph, numNodes = graphreader(url)
            else:
                numNodes = 0
                graph = {'0': {'1': 0}}
           

            filename = os.path.basename(instance.graph.url)
            filenameNoTxt = os.path.splitext(filename)[0]
            filename = f"{filenameNoTxt}.png"
       
            filepath = os.path.join(settings.MEDIA_URL, 'graph/upload/', filename)
            return render(request, 'upload_graph.html', {
                'form': ImageForm(), 
                'readGraph': graph, 
                'numNodes': numNodes,
                'filepath': filepath,
                'filename': filename,
                'filenameNoTxt': filenameNoTxt,
                'algo': algo,
                'displayImage': displayImage,
                'updateText': updateText,
                'imageform': ImageForm()
              
            })
        elif imageform.is_valid():
            instance = imageform.save()
            
            
            url = instance.image.path

            #WE HAVE THE IMAGE SAVED HERE WE NEED TO NOW TRANSLATE TO GRAPH OBJECT 
        
            if displayImage == True:
                graph, numNodes = graphreader(url)
            else:
                numNodes = 0
                graph = {'0': {'1': 0}}
           

            filename = os.path.basename(instance.graph.url)
            filenameNoTxt = os.path.splitext(filename)[0]
            filename = f"{filenameNoTxt}.png"
       

            filepath = os.path.join(settings.MEDIA_URL, 'graph/upload/', filename)
            return render(request, 'upload_graph.html', {
                'form': ImageForm(), 
                'readGraph': graph, 
                'numNodes': numNodes,
                'filepath': filepath,
                'filename': filename,
                'filenameNoTxt': filenameNoTxt,
                'algo': algo,
                'displayImage': displayImage,
                'updateText': updateText,
                'imageform': ImageForm()
              
            })
       
    else:
        form = GraphForm()
        imageform = ImageForm()
    return render(request, 'upload_graph.html', {'form': form, 'imageform':imageform})

#Processing Page
def new_processing_view(request):
    if request.method == 'POST':
        if 'DijkPreset' in request.POST:
            g, nodeCount = graphreader('HomePage/samplefiles/dijkstra2.txt')
            data, nodeCount, startingNode, filename, filename2 = callDijkstra(g, nodeCount)
            vStartNode = 'v'+ startingNode
            is_Dijk = True
            nodesplit = []
            for item in data:
                nodesplit_item = []
                for index, cell in enumerate(item):
                    if index == 1 or index == 4:
                        if isinstance(cell, list):
                            for sub_item in cell:
                                nodesplit_item.append(str(sub_item))
                        else:
                            nodesplit_item.append(str(cell))
                    else:
                        nodesplit_item.append(cell)
                nodesplit.append(nodesplit_item)
            data = nodesplit
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            return render(request, 'processing.html', {'data':data, 'nodeCount':nodeCount, 'vertexArr':vertexArr, 'startNode':vStartNode, 'is_Dijk': is_Dijk, 'image':filename, 'imagemst':filename2,})
        elif 'DijkNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, nodeCount = graphreader('media/graph/upload/' + filenametxt)
            data, nodeCount, startingNode, filename, filename2 = callDijkstra(g, nodeCount)
            vStartNode = 'v'+ startingNode
            is_Dijk = True
            nodesplit = []
            for item in data:
                nodesplit_item = []
                for index, cell in enumerate(item):
                    if index == 1 or index == 4:
                        if isinstance(cell, list):
                            for sub_item in cell:
                                nodesplit_item.append(str(sub_item))
                        else:
                            nodesplit_item.append(str(cell))
                    else:
                        nodesplit_item.append(cell)
                nodesplit.append(nodesplit_item)
            data = nodesplit
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            return render(request, 'processing.html', {'data':data, 'nodeCount':nodeCount, 'vertexArr':vertexArr, 'startNode':vStartNode, 'is_Dijk': is_Dijk, 'image':filename, 'imagemst':filename2,})      
        elif 'KruskalPreset' in request.POST:
            g, numSets = graphreader('HomePage/samplefiles/kruskals.txt')
            data, numSets, uniqueEdges, filename, filename2 = callKruskals(g, numSets)
            is_Kruskals = True
            sets = [f"{{{i}}}" for i in range(numSets + 1)]
            return render(request, 'processing.html', {'data':data, 'is_Kruskals': is_Kruskals, 'numSets':numSets, 'sets':sets, 'uniqueEdges':uniqueEdges, 'image':filename, 'imagemst':filename2,})
        elif 'KruskalNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, numSets = graphreader('media/graph/upload/' + filenametxt)
            data, numSets, uniqueEdges, filename, filename2 = callKruskals(g, numSets)
            is_Kruskals = True
            sets = [f"{{{i}}}" for i in range(numSets + 1)]
            return render(request, 'processing.html', {'data':data, 'is_Kruskals': is_Kruskals, 'numSets':numSets, 'sets':sets, 'uniqueEdges':uniqueEdges, 'image':filename, 'imagemst':filename2,})
        elif 'KnapsackPreset' in request.POST:
            W, weight, profit, n = readKnapSack('HomePage/samplefiles/knapsack.txt')
            data = callKnapsackDP(W, weight, profit, n)
            is_Knapsack = True
            return render(request, 'processing.html', {'data':data, 'is_Knapsack': is_Knapsack}) 
        elif 'KnapsackNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            W, weight, profit, n = readKnapSack('media/graph/upload/' + filenametxt)
            data = callKnapsackDP(W, weight, profit, n)
            is_Knapsack = True
            return render(request, 'processing.html', {'data':data, 'is_Knapsack': is_Knapsack}) 
        elif 'KMPPreset' in request.POST:
            text, pattern = read2LineText('HomePage/samplefiles/kmp.txt')
            data, fail, length, text = callKMP(text, pattern)
            numbers = []
            for i in range(length):
                numbers.append(i)
            is_KMP = True
            return render(request, 'processing.html', {'data':data, 'fail':fail, 'is_KMP': is_KMP, 'numbers':numbers, 'text':text})
        elif 'KMPNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            text, pattern = read2LineText('media/graph/upload/' + filenametxt)
            data, fail, length, text = callKMP(text, pattern)
            numbers = []
            for i in range(length):
                numbers.append(i)
            is_KMP = True
            return render(request, 'processing.html', {'data':data, 'fail':fail, 'is_KMP': is_KMP, 'numbers':numbers, 'text':text})
        elif 'IntervalPreset' in request.POST:
            intervals = readIntervals('HomePage/samplefiles/intervals.txt')
            optimal, data = callIntervalGreed(intervals)
            is_IntervalGreed = True
            return render(request, 'processing.html', {'data':data, 'is_IntervalGreed':is_IntervalGreed, 'optimal':optimal,})
        elif 'IntervalNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            intervals = readIntervals('media/graph/upload/' + filenametxt)
            is_IntervalGreed = True
            optimal, data = callIntervalGreed(intervals)
            return render(request, 'processing.html', {'data':data, 'is_IntervalGreed':is_IntervalGreed, 'optimal':optimal,})
        elif 'BellmanFordPreset' in request.POST:
            g, nodeCount = graphreader('HomePage/samplefiles/bellmanford.txt')
            data, nodeCount, startNode = callBellmanFord(g, nodeCount)
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            startNode = 'v'+ startNode
            is_BF = True
            return render(request, 'processing.html', {'data':data, 'is_BF': is_BF, 'nodeCount': nodeCount, 'vertexArr': vertexArr, 'startNode': startNode})
        elif 'BellmanFordNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, nodeCount = graphreader('media/graph/upload/' + filenametxt)
            data, nodeCount, startNode = callBellmanFord(g, nodeCount)
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            startNode = 'v'+ startNode
            is_BF = True
            return render(request, 'processing.html', {'data':data, 'is_BF': is_BF, 'nodeCount': nodeCount, 'vertexArr': vertexArr, 'startNode': startNode})
        elif 'PrimsPreset' in request.POST:
            g, nodeCount = graphreaderNeg('HomePage/samplefiles/prims.txt')
            data, nodeCount, filename, filename2  = callPrims(g, nodeCount)
            is_Prims = True
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            return render(request, 'processing.html', {'data':data, '' 'is_Prims': is_Prims, 'vertexArr':vertexArr, 'nodeCount':nodeCount, 'image':filename, 'imagemst':filename2,}) 
        elif 'PrimsNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, nodeCount = graphreaderNeg('media/graph/upload/' + filenametxt)
            data, nodeCount, filename, filename2 = callPrims(g, nodeCount)
            is_Prims = True
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            # print(vertexArr)
            # print(nodeCount)
            return render(request, 'processing.html', {'data':data, '' 'is_Prims': is_Prims, 'vertexArr':vertexArr, 'nodeCount':nodeCount,'image':filename, 'imagemst':filename2}) 
        elif 'InsertionPreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/numbers2sort.txt')
            numbers, data = callInsertionSort(numbers)
            is_sort = True
            is_sorted = False
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
            return render(request, 'processing.html', {'data':data, 'is_sort':is_sort, 'is_sorted':False})
        elif 'InsertionNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            numbers, data = callInsertionSort(numbers)
            is_sort = True
            is_sorted = False
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
            return render(request, 'processing.html', {'data':data, 'is_sort':is_sort, 'is_sorted':False})
        elif 'BubblePreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/numbers2sort.txt')
            numbers, data = callBubbleSort(numbers)
            is_bubble = True
            is_sorted = False

            print(data)
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
            return render(request, 'processing.html', {'data':data, 'is_bubble':is_bubble, 'is_sorted':False})
        elif 'BubbleNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            numbers, data = callBubbleSort(numbers)


            is_sort = True
            is_sorted = False
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
    
            return render(request, 'processing.html', {'data':data, 'is_bubble':is_bubble, 'is_sorted':False})
        elif 'HuffmanPreset' in request.POST:
            character, frequency = readHuffman('HomePage/samplefiles/huffman.txt')
            code_map, encoded_message, original_message = callHuffman(character, frequency)
            is_Huffman = True
            return render(request, 'processing.html', {'code_map':code_map, 'encoded_message':encoded_message, 'original_message':original_message, 'is_Huffman': is_Huffman})     
        elif 'HuffmanNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            character, frequency = readHuffman('media/graph/upload/' + filenametxt)

            code_map, encoded_message, original_message = callHuffman(character, frequency)
            is_Huffman = True
            return render(request, 'processing.html', {'code_map':code_map, 'encoded_message':encoded_message, 'original_message':original_message, 'is_Huffman': is_Huffman})
        elif 'LCSPreset' in request.POST:
            seq1, seq2 = read2LineText('HomePage/samplefiles/LCS.txt')
            data, LCS = callLCS(seq1, seq2)
            is_LCS = True
            return render(request, 'processing.html', {'data':data, 'is_LCS': is_LCS, 'LCS':LCS})
        elif 'LCSNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            seq1, seq2 = read2LineText('media/graph/upload/' + filenametxt)
            data, LCS = callLCS(seq1, seq2)
            is_LCS = True
            return render(request, 'processing.html', {'data':data, 'is_LCS': is_LCS, 'LCS':LCS})
        elif 'FloydWarshallPreset' in request.POST:
            g, nodeCount = graphreader('HomePage/samplefiles/dijkstra.txt')
            data, parent, nodeList = callFloydWarshall(g, nodeCount)
            is_FloydWarshall = True 
            length = len(nodeList)
            data = [[nodeList[i]] + data[i] for i in range(length)]
            parent = [[nodeList[i]] + parent[i] for i in range(length)]
            return render(request, 'processing.html', {'data':data, 'is_FloydWarshall':is_FloydWarshall, 'nodeList':nodeList, 'length':length, 'parent': parent,  })
        elif 'FloydWarshallNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, nodeCount = graphreader('media/graph/upload/' + filenametxt)
            data, parent, nodeList = callFloydWarshall(g, nodeCount)
            is_FloydWarshall = True 
            length = len(nodeList)
            data = [[nodeList[i]] + data[i] for i in range(length)]
            parent = [[nodeList[i]] + parent[i] for i in range(length)]
            return render(request, 'processing.html', {'data':data, 'is_FloydWarshall':is_FloydWarshall, 'nodeList':nodeList, 'length':length, 'parent': parent,  })
        elif 'UnionFindPreset' in request.POST:
            Q = readQueue('HomePage/samplefiles/unionfind.txt')
            data = callUnionFind(Q)
            is_UnionFind = True
            return render(request, 'processing.html', {'data':data, 'is_UnionFind':is_UnionFind, })
        elif 'UnionFindNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            Q = readQueue('media/graph/upload/' + filenametxt)
            data = callUnionFind(Q)
            is_UnionFind = True
            return render(request, 'processing.html', {'data':data, 'is_UnionFind':is_UnionFind, })
        elif 'BWTPreset' in request.POST:
            string = readBWT('HomePage/samplefiles/bwt.txt')
            data = callBWT(string)
            is_BWT = True
            return render(request, 'processing.html', {'data':data, 'is_BWT':is_BWT, 'string':string })
        elif 'BWTNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            string = readBWT('media/graph/upload/' + filenametxt)
            data = callBWT(string)
            is_BWT = True
            return render(request, 'processing.html', {'data':data, 'is_BWT':is_BWT,'string':string })
        elif 'TriePreset' in request.POST:
            words = readWords('HomePage/samplefiles/trie.txt')
            data, filename = callTrie(words)
            is_Trie = True
            return render(request, 'processing.html', {'data':data, 'is_Trie':is_Trie, 'filename':filename, 'words':words })
        elif 'TrieNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            words = readWords('media/graph/upload/' + filenametxt)
            data, filename = callTrie(words)
            is_Trie = True
            return render(request, 'processing.html', {'data':data, 'is_Trie':is_Trie, 'filename':filename, 'words':words })
        elif 'RabinKarpPreset' in request.POST:
            text, pattern = read2LineText('HomePage/samplefiles/rabinkarp.txt')
            q = 101
            data = callRabinKarp(text,pattern,q)
            is_RK = True
            n = len(text)
            index = [i for i in range(n)]
            return render(request, 'processing.html', {'data':data, 'is_RK':is_RK, 'text': text, 'pattern': pattern, 'index':index })
        elif 'RabinKarpNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            text, pattern = read2LineText('media/graph/upload/' + filenametxt)
            q = 101
            data = callRabinKarp(text,pattern,q)
            is_RK = True
            n = len(text)
            index = [i for i in range(n)]
            return render(request, 'processing.html', {'data':data, 'is_RK':is_RK, 'text': text, 'pattern': pattern, 'index':index})
        elif 'BoyerMoorePreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/boyermoore.txt')
            n = len(numbers)
            data, candidate = callBoyerMoore(numbers, n)
            is_BoyerMoore = True
            n = n
            return render(request, 'processing.html', {'data':data, 'is_BoyerMoore':is_BoyerMoore, 'data':data, 'numbers': numbers, 'n':range(n)})
        elif 'BoyerMooreNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            n = len(numbers) 
            data, candidate = callBoyerMoore(numbers, n)
            n = n
            is_BoyerMoore = True
            return render(request, 'processing.html', {'data':data, 'is_BoyerMoore':is_BoyerMoore,  'data':data, 'numbers': numbers, 'n':range(n)})
        elif 'CountPreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/numbers2sort.txt')
            data, countArr = callCountSort(numbers)
            is_CountSort = True
            is_sorted = False
            length = len(countArr)
            n = [i for i in range(length)]
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
            return render(request, 'processing.html', {'data':data, 'is_CountSort':is_CountSort, 'is_sorted':False, 'countArr':countArr, 'inputArr':numbers, 'n':n})
        elif 'CountNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            data, countArr = callCountSort(numbers)
            is_CountSort = True
            length = len(countArr)
            n = [i for i in range(length)]
            is_sorted = False
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
            return render(request, 'processing.html', {'data':data, 'is_CountSort':is_CountSort, 'is_sorted':False, 'countArr':countArr, 'inputArr':numbers, 'n':n})
        elif 'MergePreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/numbers2sort.txt')
            data, sortDepth = callMergeSort(numbers)
            is_MergeSort = True
            is_sorted = False
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
    
            depth_dict = defaultdict(list)
            for depth, values in sortDepth:
                depth_dict[depth].append(values)
            grouped_by_depth = defaultdict(list)

            # Populate the dictionary
            for depth, array in sortDepth:
                grouped_by_depth[depth].append(array)

            # Convert the dictionary to a list of lists
            sorted_depths = sorted(grouped_by_depth.keys())
            result = [grouped_by_depth[depth] for depth in sorted_depths]
                
      
            test = reverse_merge_sort(result)

            result_with_index = [(index, items) for index, items in enumerate(result)]
            test_with_index = [(index, items) for index, items in enumerate(test)]
            
            
            return render(request, 'processing.html', {'data':data, 'is_MergeSort':is_MergeSort, 'is_sorted':False, 'sortDepth':sortDepth, 'result':result, 'result_with_index':result_with_index, 'test_with_index':test_with_index})
        elif 'MergeNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            data, sortDepth = callMergeSort(numbers)
            is_MergeSort = True
            is_sorted = False
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
            
            depth_dict = defaultdict(list)
            for depth, values in sortDepth:
                depth_dict[depth].append(values)
            grouped_by_depth = defaultdict(list)

            # Populate the dictionary
            for depth, array in sortDepth:
                grouped_by_depth[depth].append(array)

            # Convert the dictionary to a list of lists
            sorted_depths = sorted(grouped_by_depth.keys())
            result = [grouped_by_depth[depth] for depth in sorted_depths]
                
      
            test = reverse_merge_sort(result)

            result_with_index = [(index, items) for index, items in enumerate(result)]
            test_with_index = [(index, items) for index, items in enumerate(test)]
            

            return render(request, 'processing.html', {'data':data, 'is_MergeSort':is_MergeSort, 'is_sorted':False, 'sortDepth':sortDepth, 'result':result, 'result_with_index':result_with_index, 'test_with_index':test_with_index})
        elif 'MaxIncreasePreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/numbersincrease.txt')
           
            data, inputArr, n = callMaxIncrease(numbers)
            is_MaxIncrease = True
           
            print(data)
            return render(request, 'processing.html', {'data':data, 'is_MaxIncrease':is_MaxIncrease, 'is_sorted':False, 'n':n, 'inputArr':inputArr})
        elif 'MaxIncreaseNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            n = len(numbers)
            data, inputArr, n = callMaxIncrease(numbers)
            is_MaxIncrease = True   
            return render(request, 'processing.html', {'data':data, 'is_MaxIncrease':is_MaxIncrease, 'is_sorted':False, 'n':n, 'inputArr':inputArr})
        elif 'QuickSortPreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/numbers2sort.txt')
            data, original = callQuickSort(numbers)
            is_QS = True
            is_sorted = False
            if original == sorted(numbers):
                is_sorted = True
            elif original == sorted(numbers, reverse=True):
                is_sorted = True
            if original == True:
                return render(request, 'processing.html', {'is_sorted': True})
            return render(request, 'processing.html', {'data':data, 'is_QS':is_QS, 'is_sorted':False})
        elif 'QuickSortNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            data, original = callQuickSort(numbers)
            is_QS = True
            is_sorted = False
    
            if original == sorted(numbers):
                is_sorted = True
            elif original == sorted(numbers, reverse=True):
                is_sorted = True
            if original == True:
                return render(request, 'processing.html', {'is_sorted': True})
    
            return render(request, 'processing.html', {'data':data, 'is_QS':is_QS, 'is_sorted':False})
        elif 'QuickSelectPreset' in request.POST:
            k, numbers = readSelectNumbers('HomePage/samplefiles/quickselect.txt')
            data = callQuickSelect(k, numbers)
            print(data)
            is_QSelect = True
            return render(request, 'processing.html', {'data':data, 'is_QSelect':is_QSelect, 'is_sorted':False, 'k':k})
        elif 'QuickSelectNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            k, numbers = readSelectNumbers('media/graph/upload/' + filenametxt)
       
            data = callQuickSelect(k, numbers)
            is_QSelect = True

            return render(request, 'processing.html', {'data':data, 'is_QSelect':is_QSelect, 'is_sorted':False, 'k':k})
        elif 'MISPreset' in request.POST:
            g, numSets = graphreader('HomePage/samplefiles/mis.txt')
            print(g)
            data, filename, filenameMIS, progress = callMIS(g)
            is_MIS = True
            sets = [f"{{{i}}}" for i in range(numSets + 1)]
            return render(request, 'processing.html', {'data':data, 'is_MIS': is_MIS, 'image':filename, 'imageMIS':filenameMIS })
        elif 'MISNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, numSets = graphreader('media/graph/upload/' + filenametxt)
            data, filename, filenameMIS, progress = callMIS(g)
            is_MIS = True
            sets = [f"{{{i}}}" for i in range(numSets + 1)]
            return render(request, 'processing.html', {'data':data, 'is_MIS': is_MIS, 'image':filename, 'imageMIS':filenameMIS })
            # 'numSets':numSets, 'sets':sets, 'uniqueEdges':uniqueEdges, 'image':filename, 'imagemst':filename2,
        elif 'DijkstraInteractivePreset' in request.POST:
            g, nodeCount, startNode = graphreaderStartNode('HomePage/samplefiles/dijkstra2.txt')
            data, nodeCount, startingNode, filename, filename2, filenameIteration = callDijkstra(g, nodeCount, startNode)
            filenameState = filenameIteration + [filename2]
            vStartNode = 'v'+ startingNode
            is_DijkInteractive = True
            nodesplit = []
            for item in data:
                nodesplit_item = []
                for index, cell in enumerate(item):
                    if index == 1 or index == 4:
                        if isinstance(cell, list):
                            for sub_item in cell:
                                nodesplit_item.append(str(sub_item))
                        else:
                            nodesplit_item.append(str(cell))
                    else:
                        nodesplit_item.append(cell)
                nodesplit.append(nodesplit_item)
            data = nodesplit
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            return render(request, 'processing.html', {'data':data, 'nodeCount':nodeCount, 'vertexArr':vertexArr, 'startNode':vStartNode, 'is_DijkInteractive': is_DijkInteractive, 'filename':filename, 'imagemst':filename2, 'filenameState':filenameState})
        elif 'DijkstraInteractiveNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, nodeCount, startNode = graphreaderStartNode('media/graph/upload/' + filenametxt)
            data, nodeCount, startingNode, filename, filename2, filenameIteration = callDijkstra(g, nodeCount, startNode)
            filenameState = filenameIteration + [filename2]
            vStartNode = 'v'+ startingNode
            is_DijkInteractive = True
            nodesplit = []
            for item in data:
                nodesplit_item = []
                for index, cell in enumerate(item):
                    if index == 1 or index == 4:
                        if isinstance(cell, list):
                            for sub_item in cell:
                                nodesplit_item.append(str(sub_item))
                        else:
                            nodesplit_item.append(str(cell))
                    else:
                        nodesplit_item.append(cell)
                nodesplit.append(nodesplit_item)
            data = nodesplit
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            return render(request, 'processing.html', {'data':data, 'nodeCount':nodeCount, 'vertexArr':vertexArr, 'startNode':vStartNode, 'is_DijkInteractive': is_DijkInteractive, 'filename':filename, 'imagemst':filename2, 'filenameState':filenameState})
        elif 'BellmanFordInteractivePreset' in request.POST:
          
            g, nodeCount, startingNode = graphreaderStartNode('HomePage/samplefiles/bellmanford.txt')
            data, nodeCount, startNode, filenameIteration, filename, filenameMST = callBellmanFord(g, nodeCount, startingNode)
            filenameState = filenameIteration + [filenameMST]
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            startNode = 'v'+ startNode
            is_BFInteractive = True
            filename = 'graph.png'
            filenameState = ['0graph.png', '1graph.png', '2graph.png', '3graph.png', 'graphMST.png']
            return render(request, 'processing.html', {'data':data, 'is_BFInteractive': is_BFInteractive, 'nodeCount': nodeCount, 'vertexArr': vertexArr, 'startNode': startNode, 'filenameState':filenameState, 'filename':filename})
        elif 'BellmanFordInteractiveNotPreset' in request.POST:
            # NEED TO UPDATE ONCE REGULAR IS FIXED
            filename = request.POST.get('filenameNoTxt')
            
            filenametxt = filename + '.txt'
            g, nodeCount, startingNode = graphreaderStartNode('media/graph/upload/' + filenametxt)
            data, nodeCount, startNode = callBellmanFord(g, nodeCount, startingNode)
            vertexArr = []
            for i in range(nodeCount):
                vertexArr.append("v" + str(i))
            startNode = 'v'+ startNode
            is_BFInteractive = True
           
            return render(request, 'processing.html', {'data':data, 'is_BFInteractive': is_BFInteractive, 'nodeCount': nodeCount, 'vertexArr': vertexArr, 'startNode': startNode, 'filenameState':filenameState, 'filename':filename})
        elif 'FisherYatesPreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/fisheryates.txt')
            n = len(numbers)
            data = callFisherYates(numbers, n)
            is_FisherYate = True
            full_Randomized = data[-1]
            data[-1] = (data[-1][0], 0)
            return render(request, 'processing.html', {'data':data, 'is_FisherYate':is_FisherYate,  'data':data, 'numbers': numbers, 'n':n, 'full_Randomized':full_Randomized, 'row_count': len(data)})
        elif 'FisherYatesNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            n = len(numbers)
            data = callFisherYates(numbers, n)
      
            full_Randomized = data[-1]
            data[-1] = (data[-1][0], 0)
            is_FisherYate = True
            return render(request, 'processing.html', {'data':data, 'is_FisherYate':is_FisherYate,  'data':data, 'numbers': numbers, 'n':n, 'full_Randomized':full_Randomized, 'row_count': len(data) })
    else:
        return HttpResponse('Invalid method or action')

def callMaxIndepdentSet(g):
    g, nodeCount = graphreader('HomePage/samplefiles/prims.txt')
    mst = prims(g)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"graph_{timestamp}.png"
    filenameMST = f"graphMST_{timestamp}.png"
    pos = build_and_save_graph(g, filename)
    if mst is not None:
        build_and_save_graph(g, filenameMST, mst, pos=pos)
    return mst, nodeCount, filename, filenameMST

def callMaxIncrease(numbers):
    original = numbers[:]
    len, data = maxincrease(numbers)
    return data, original, len


def callBubbleSort(numbers):
    original = numbers[:]
    bubble = bubbleSort(numbers)
    return original, bubble

def callInsertionSort(numbers):
    original = numbers[:] 
    data = insertionSort(numbers)
    return original, data


def callBoyerMoore(numbers, n):
    original = numbers[:]
    states, candidate = isMajority(numbers, n)
    print(states)
    print(candidate)
    return states, candidate

def callFisherYates(numbers, n):
    original = numbers[:]
    states = randomize(numbers, n)
    return states

def callRabinKarp(text, pattern, q):

    data = search(text, pattern, q)
    return data

def callLCS(seq1, seq2):
    data, LCS  = lcs(seq1, seq2)
    return data, LCS

def callKnapsackDP(W, weight, profit, n):
    global t 
    t = [[-1 for i in range(W + 1)] for j in range(n + 1)]
    knapsackDP(weight, profit, W, n)
    table = buildTable(W, profit, weight, t)
    print(table)
    return(table)


def callKruskals(g, numSets): #STAGE 1 DONE
    data, uniqueEdges, mst = kruskals(g, numSets)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"graph_{timestamp}.png"
    filenameMST = f"graphMST_{timestamp}.png"
    pos = build_and_save_graph(g, filename)
    if mst is not None:
        build_and_save_graph(g, filenameMST, mst, pos=pos)
    return data, numSets, uniqueEdges, filename, filenameMST


def callMIS(g):
    data, progress = maximumindependentset(g)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"graph_{timestamp}.png"
    filenameMIS = f"graphMIS_{timestamp}.png"
    arr = [(i, i) for i in range(len(data))]
    pos = build_and_save_graph(g, filename, arr)
    if data is not None:
        build_and_save_graphMIS(g, filenameMIS, data, pos=pos)
    return data, filename, filenameMIS, progress

def callFloydWarshall(g, nodeCount):
    nodeList = set(g.keys())
    nodeListS = sorted(nodeList)
    data, parent = floydwarshall(g)
    return data, parent, nodeListS


def callBellmanFord(g, nodeCount, startingNodeInt):
    startingNodeStr = str(startingNodeInt)
    arr = [(i, 0 if i == startingNodeInt else float('inf')) for i in range(nodeCount)]
    
    data, mst = bellmanford(g, startingNodeInt)
    nodes = [t[1:1+nodeCount] for t in data]

    colors = [[(0, 1), (1, 0), (2, 0), (3, 1), (4, 2)], [(0, 1), (1, 0), (2, 0), (3, 2), (4, 2)], [(0, 2), (1, 1), (2, 1), (3, 2), (4, 2)], [(0, 2), (1, 1), (2, 2), (3, 2), (4, 2)], [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]]
    edges = [[(4, 0), (4, 3)], [], [(0, 1), (0, 2)], [(2, 1)], []]
    filenameIteration, filename, filenameMST = buildStaticGraphsBF(g, data, nodes, nodeCount, mst, arr, colors, edges)
    return data, nodeCount, startingNodeInt, filenameIteration, filename, filenameMST


def callDijkstra(g, nodeCount, startingNodeInt):
    startingNodeStr = str(startingNodeInt)
    arr = [(i, 0 if i == startingNodeInt else float('inf')) for i in range(nodeCount)]
    data, mst = dijkstras(g, startingNodeStr)
    nodes = [(t[2], t[3]) for t in data]
    print("nodes", nodes)
    colors = getDijkNodeColors(nodes, len(data))
    edges = getDijkEdgeColors(data)

    print(colors)
    print(edges)

    filenameIteration, filename, filenameMST = buildStaticGraphs(g, data, nodes, nodeCount, mst, arr, colors, edges)
    return data, nodeCount, startingNodeStr, filename, filenameMST, filenameIteration

def callPrims(g, nodeCOunt):
    g, nodeCount = graphreader('HomePage/samplefiles/prims.txt')
    data, mst = prims(g)
    mstStr = [(str(min(edge)), str(max(edge))) for edge in mst]
    filename = 0
    filenameMST = 0
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"graph_{timestamp}.png"
    filenameMST = f"graphMST_{timestamp}.png"
    pos = build_and_save_graph(g, filename)
    if mstStr is not None:
        build_and_save_graph(g, filenameMST, mstStr, pos=pos)
    return data, nodeCount, filename, filenameMST


def callCountSort(numbers):
    data = countSort(numbers)
    return data


def callQuickSort(numbers):
    original = numbers[:]
    print(numbers)
    left = 0
    right = len(numbers)-1
    data = quicksort(numbers, left, right)
    return data, original


def callQuickSelect(k, numbers):

    left = 0
    right = len(numbers)-1
    data = quickselect(numbers, left, right, k)
    return data



def callMergeSort(numbers):
    original = numbers[:] 
    print("original", )
    test = numbers[::-1]
    print("test",  test)
    data, depth_arrays = mergeSort(numbers)
    sortDepth = sort_by_depth(depth_arrays)
    test = remove_duplicates(sortDepth)
    return data, test



def callKMP(text, pattern):
    data = kmp(text, pattern)
    length = len(pattern)
    fail = compute_failure_function(pattern)
    return data, fail, length, pattern


def callIntervalGreed(intervals):
    selectedtasks = intervalGreed(intervals)
    milTask = to_military_time(selectedtasks)
    milInterval = to_military_time(intervals)
    return milTask, milInterval

def callHuffman(character, frequency):
    original_message = 'NEED TO IMPLEMEENT'
    encoded_message, code_map = huffman_encode(character, frequency)
    return code_map, encoded_message, original_message
    

def callUnionFind(Q):
    data = UnionFind.unionfind(Q)
    return data

def callBWT(string):
    transform = bwt(string)
    return transform

def callTrie(words):
    trie = trieBuild(words)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"trie_{timestamp}.png"
    trie.visualize(filename)
    return trie, filename



def graph_list(request):
    print(request)
    graphs = GraphModel.objects.all()
    return render(request, 'graph_list.html', {'graphs':graphs})

def build_and_save_graph(graph_data, filename, nodeWeights, mst_edges=None,  pos=None):
    directory = 'graphApp/static/graphApp/images'
    G = nx.DiGraph()
    
    for node, edges in graph_data.items():
        for adjacent_node, weight in edges.items():
            G.add_edge(node, adjacent_node, weight=weight)
    
    if pos is None:
        pos = nx.spring_layout(G, seed=42, k = 10) 
    
    plt.figure(figsize=(12, 12))
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor((255/255, 253/255, 250/255, 1.0))
    
    ax.set_axis_off()

    node_color_rgb = ((250/255, 229/255, 185/255, 1.0))
    node_edge_color_rgb = ((232/255, 162/255, 95/255, 1.0))
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_color_rgb, edgecolors= node_edge_color_rgb)
    
    if mst_edges is None:
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=40)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, font_color='black')
    else:
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        filtered_edge_labels = {edge: edge_labels[edge] for edge in mst_edges if edge in edge_labels}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=filtered_edge_labels, font_size=12, label_pos=0.5, font_color='black')
    

    node_weights_dict = dict(nodeWeights)
    node_weights_dict = {str(node): weight for node, weight in node_weights_dict.items()}
    node_labels = {node: str(node_weights_dict.get(str(node), '')) for node in G.nodes()}

    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='black')
    if not os.path.exists(directory):
        os.makedirs(directory)
    ax.set_axis_off()
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    
    return pos



def build_and_save_graphUpload(graph_data, filename):

    directory = 'media/graph/upload'
    G = nx.DiGraph()
    
    # Build the graph
    for node, edges in graph_data.items():
        for adjacent_node, weight in edges.items():
            G.add_edge(node, adjacent_node, weight=weight)
    
 
    pos = nx.spring_layout(G, seed=42) 
    
    # Create the figure and axis
    plt.figure(figsize=(12, 12))
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor((255/255, 253/255, 250/255, 1.0))
    # fig.patch.set_facecolor('blue')
    ax.set_axis_off()
    
    node_color_rgb = (81/255, 40/255, 132/255)
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_color_rgb)
    
    # Draw only the specified edges if mst_edges is provided

    nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, font_color='black')
   
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')
    
    # Ensure directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Save the figure
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    

def extract_value_from_url(full_url):
    parts = full_url.split('=')

    if len(parts) > 1:
        value_after_equal_sign = parts[1]
        return value_after_equal_sign
    else:
        return None  


def sort_by_depth(data: List[Tuple[int, List[int]]]) -> List[Tuple[int, List[int]]]:
    
    # Use a defaultdict with lists to maintain all entries
    grouped = defaultdict(list)
    
    for item in data:
        depth, values = item
        grouped[depth].append(values) 
    
    # Sort depths and prepare the final sorted data
    sorted_depths = sorted(grouped.keys())
    
    sorted_data = []
    for depth in sorted_depths:
        # Append all lists associated with the current depth
        sorted_data.extend((depth, values) for values in grouped[depth])
    
    return sorted_data




def graphIteration(graph_data, filename, nodeColors, edgeColors, nodeWeights, pos=None):
    directory = 'graphApp/static/graphApp/images'

    G = nx.DiGraph()

    # Add nodes and edges to the graph
    for node, edges in graph_data.items():
        for adjacent_node, weight in edges.items():
            G.add_edge(node, adjacent_node, weight=weight)
    
    # Determine node positions if not provided
    if pos is None:
        pos = nx.spring_layout(G, seed=42, k = 10)
    
    # Color mapping
    mapOrange = ((230/255, 136/255, 60/255, 1.0))
    mapTan = ((250/255, 229/255, 185/255, 1.0))
    mapBlue = ((182/255, 223/255, 245/255, 1.0))


    color_map = {0: mapTan, 1: mapOrange, 2: mapBlue}
    
    # Node colors
    node_colors_dict = dict(nodeColors)

    node_colors_dict = {str(node): color_code for node, color_code in node_colors_dict.items()}
    node_color_values = [color_map.get(node_colors_dict.get(str(node), 0), 'grey') for node in G.nodes()]


    # Edge colors
    highlighted_color = 'orange'
    default_color = 'black'
    
    # Initialize all edges to default color
    edge_colors_dict = dict.fromkeys(G.edges(), default_color)


    converted_edge_colors = []
    for edge in edgeColors:
        if isinstance(edge, tuple) and len(edge) == 2:
            converted_edge_colors.append((str(edge[0]), str(edge[1])))
    # Set highlighted color for edges in edgeColors
    for edge in converted_edge_colors:
        if edge in edge_colors_dict:
            edge_colors_dict[edge] = highlighted_color


    # Prepare edge color values for drawing
    edge_color_values = [edge_colors_dict[edge] for edge in G.edges()]

    # Set up the plot
    plt.figure(figsize=(12, 12))
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor((255/255, 253/255, 250/255, 1.0))
    
    ax.set_axis_off()
    
    # Draw nodes
    
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_color_values)
    
    # Draw edges with colors
    nx.draw_networkx_edges(G, pos, edge_color=edge_color_values, arrows=True, arrowstyle='-|>', arrowsize=40)
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, font_color='black')
    
    # Draw node labels
    
    node_weights_dict = dict(nodeWeights)
    node_weights_dict = {str(node): weight for node, weight in node_weights_dict.items()}
    node_labels = {node: str(node_weights_dict.get(str(node), '')) for node in G.nodes()}
    # print(node_labels)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='black')


    
    # Save the figure
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    plt.close(fig)
    
    return pos



def buildStaticGraphs(g, data, nodes, nodeCount, mst, arr, colors, edges):
    filenameIteration = []
    filename = f"graph.png"
    filenameMST = f"graphMST.png"
    print(data)
    fullweights = [t[1] for t in data]
    weights = []

    print("colors", colors)
    print("edges", edges)
    for row in fullweights:
        row_weights = [(j, value) for j, value in enumerate(row)]
        weights.append(row_weights)
   
    for i in range(len(data)):
        filenameIteration.append(f"{i}graph.png")
        graphIteration(g, filenameIteration[i], colors[i], edges[i], weights[i])

    
    pos = build_and_save_graph(g, filename, arr)


    if mst is not None:
        arr = [(i, i) for i in range(nodeCount)]
        build_and_save_graph(g, filenameMST, arr, mst, pos=pos)

    return filenameIteration, filename, filenameMST
    

def buildStaticGraphsBF(g, data, nodes, nodeCount, mst, arr, colors, edges):
        filenameIteration = []
        filename = f"graph.png"
        filenameMST = f"graphMST.png"
        fullweights = [tuple(x for x in t[1:nodeCount]) for t in data]
        weights = []
        
        for row in fullweights:
            row_weights = [(j, value) for j, value in enumerate(row)]
            weights.append(row_weights)
    
        for i in range(len(data)):
            filenameIteration.append(f"{i}graph.png")
            graphIteration(g, filenameIteration[i], colors[i], edges[i], weights[i])

        
        pos = build_and_save_graph(g, filename, arr)


        if mst is not None:
            arr = [(i, i) for i in range(nodeCount)]
            build_and_save_graph(g, filenameMST, arr, mst, pos=pos)

        return filenameIteration, filename, filenameMST


def remove_duplicates(entries):
    # Dictionary to keep track of unique lists and their levels
    entry_dict = {}

    for depth, content in entries:
        # Convert list to tuple for immutability and use as a dictionary key
        content_key = tuple(content)
        if content_key not in entry_dict:
            entry_dict[content_key] = [depth]
        else:
            # Append the depth level to the existing list
            if depth not in entry_dict[content_key]:
                entry_dict[content_key].append(depth)

    # Rebuild the list of unique entries
    unique_entries = []
    for content_key, depths in entry_dict.items():
        for depth in depths:
            unique_entries.append((depth, list(content_key)))

    return unique_entries