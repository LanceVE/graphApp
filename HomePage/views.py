from django.shortcuts import render
from django.conf import settings
from .forms import numbersForm, numbersFormDijk, numbersFormKnapsack, numbersFormLCS, stringFormKMP, huffmanForm, csvForm, GraphForm
from HomePage.algorithms.insertionSort import insertionSort
from HomePage.algorithms.bubbleSort import bubbleSort
from HomePage.algorithms.dijkstras import dijkstras
from HomePage.algorithms.knapsackDP import knapsackDP, buildTable
from HomePage.algorithms.lcs import lcs
from HomePage.algorithms.kruskals import kruskals
from HomePage.algorithms.prims import prims
from HomePage.algorithms.intervalGreed import intervalGreed
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
from HomePage.algorithms.mergesort import mergeSort
from HomePage.algorithms.MIS import maximumindependentset
from HomePage.algorithms.quickstuff import quicksort, quickselect
from HomePage.algorithms.maxincreaseDP import maxincrease
from HomePage.helper.csvreader import graphreader, graphreaderNeg, readKnapSack, read2LineText, readIntervals, readHuffman, readNumbers, readQueue, readBWT, readWords, readSelectNumbers
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
    return render(request, "new_home.html", {'form':form, 'formCSV':formCSV, 'formDijk':formDijk, 'formKnapsack': formKnapsack, 'formLCS': formLCS,'formKMP':formKMP, 'formHuffman':formHuffman , } ) 

#Interemediate Page
def upload_graph(request):
    if request.method == 'POST':
        form = GraphForm(request.POST, request.FILES)
        full_url = request.get_full_path()
        algo = extract_value_from_url(full_url)
        displayImage = False
        updateText = False
        if algo in ['Dijkstra','Kruskal', 'Bellmanford', 'FloydWarshall', 'Prims', 'MaxIndependentSet']:
            displayImage = True
            updateText = True
        if algo in ['Knapsack','KMP', 'Huffman', 'InsertionSort', 'BubbleSort', 'UnionFind', 'Trie', 'Rabinkarp', 'FisherYate', 'CountSort', 'MergeSort']:
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
       
            filepath = build_and_save_graphUpload(graph, filename)
            filepath = os.path.join(settings.MEDIA_URL, 'graph/upload/', filename)
            return render(request, 'upload_graph.html', {
                'form': GraphForm(), 
                'readGraph': graph, 
                'numNodes': numNodes,
                'filepath': filepath,
                'filename': filename,
                'filenameNoTxt': filenameNoTxt,
                'algo': algo,
                'displayImage': displayImage,
                'updateText': updateText
            })
       
    else:
        form = GraphForm()
    return render(request, 'upload_graph.html', {'form': form})

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
            is_sort = True
            is_sorted = False
            if numbers == sorted(numbers):
                is_sorted = True
            elif numbers == sorted(numbers, reverse=True):
                is_sorted = True
            if is_sorted == True:
                return render(request, 'processing.html', {'is_sorted': True})
            return render(request, 'processing.html', {'data':data, 'is_sort':is_sort, 'is_sorted':False})
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
    
            return render(request, 'processing.html', {'data':data, 'is_sort':is_sort, 'is_sorted':False})
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
        elif 'FisherYatesPreset' in request.POST:
            numbers = readNumbers('HomePage/samplefiles/fisheryates.txt')
            n = len(numbers)
            data = callFisherYates(numbers, n)
            is_FisherYate = True
            full_Randomized = data[-1]
            return render(request, 'processing.html', {'data':data, 'is_FisherYate':is_FisherYate,  'data':data, 'numbers': numbers, 'n':n, 'full_Randomized':full_Randomized})
        elif 'FisherYatesNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            numbers = readNumbers('media/graph/upload/' + filenametxt)
            n = len(numbers)
            data = callFisherYates(numbers, n)
            full_Randomized = data[-1]
            is_FisherYate = True
            return render(request, 'processing.html', {'data':data, 'is_FisherYate':is_FisherYate,  'data':data, 'numbers': numbers, 'n':n, 'full_Randomized':full_Randomized })
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
            return render(request, 'processing.html', {'data':data, 'is_MergeSort':is_MergeSort, 'is_sorted':False, 'sortDepth':sortDepth})
        elif 'MergeNotPreset' in request.POST:
            print("Inside MergeSortNotPreset")
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
            
            return render(request, 'processing.html', {'data':data, 'is_MergeSort':is_MergeSort, 'is_sorted':False, 'sortDepth':sortDepth})       
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
            g, nodeCount = graphreader('HomePage/samplefiles/dijkstra2.txt')
            data, nodeCount, startingNode, filename, filename2, filenameIteration = callDijkstra(g, nodeCount)
            filenameState = [filename] + filenameIteration
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
            return render(request, 'processing.html', {'data':data, 'nodeCount':nodeCount, 'vertexArr':vertexArr, 'startNode':vStartNode, 'is_DijkInteractive': is_DijkInteractive, 'image':filename, 'imagemst':filename2, 'filenameState':filenameState})
        elif 'DijkstraInteractiveNotPreset' in request.POST:
            filename = request.POST.get('filenameNoTxt')
            filenametxt = filename + '.txt'
            g, nodeCount = graphreader('media/graph/upload/' + filenametxt)
            data, nodeCount, startingNode, filename, filename2, filenameIteration = callDijkstra(g, nodeCount)
            filenameState = [filename] + filenameIteration
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
            return render(request, 'processing.html', {'data':data, 'nodeCount':nodeCount, 'vertexArr':vertexArr, 'startNode':vStartNode, 'is_DijkInteractive': is_DijkInteractive, 'image':filename, 'imagemst':filename2, 'filenameState':filenameState})

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
    pos = build_and_save_graph(g, filename)
    if data is not None:
        build_and_save_graphMIS(g, filenameMIS, data, pos=pos)
    return data, filename, filenameMIS, progress

def callFloydWarshall(g, nodeCount):
    nodeList = set(g.keys())
    nodeListS = sorted(nodeList)
    data, parent = floydwarshall(g)
    return data, parent, nodeListS


def callBellmanFord(g, nodeCount):
    startNode = '0'
    data = bellmanford(g, startNode)
    return data, nodeCount, startNode


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



def callDijkstra(g, nodeCount):
    startingNode = '0'
    data, mst = dijkstras(g, startingNode)

    timestampstart = datetime.datetime.now().timestamp() 
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"graph_{timestamp}.png"
    filenameMST = f"graphMST_{timestamp}.png"
    filenameIteration = []
    nodes = [(t[2], t[3]) for t in data]

    colors = getColors(nodes, len(data))

    for i in range(len(data)):
        filenameIteration.append(f"{i}graph_{timestamp}.png")
        graphIteration(g, filenameIteration[i], colors[i])

    
    pos = build_and_save_graph(g, filename)




    if mst is not None:
        build_and_save_graph(g, filenameMST, mst, pos=pos)
    

    timestampend = datetime.datetime.now().timestamp() 

    timestampNet = timestampend - timestampstart

    print(timestampNet)
    return data, nodeCount, startingNode, filename, filenameMST, filenameIteration



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
    data, depth_arrays = mergeSort(numbers)
    sortDepth = sort_by_depth(depth_arrays)
    return data, sortDepth



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

def build_and_save_graph(graph_data, filename, mst_edges=None, pos=None):
    directory = 'graphApp/static/graphApp/images'
    G = nx.DiGraph()
    
    for node, edges in graph_data.items():
        for adjacent_node, weight in edges.items():
            G.add_edge(node, adjacent_node, weight=weight)
    
    if pos is None:
        pos = nx.spring_layout(G, seed=42) 
    
    plt.figure(figsize=(12, 12))
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor((255/255, 253/255, 250/255, 1.0))
    
    ax.set_axis_off()
    
    
    node_color_rgb = (81/255, 40/255, 132/255)
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_color_rgb)
    
    if mst_edges is None:
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, font_color='black')
    else:
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        filtered_edge_labels = {edge: edge_labels[edge] for edge in mst_edges if edge in edge_labels}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=filtered_edge_labels, font_size=12, label_pos=0.5, font_color='black')
    
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    ax.set_axis_off()
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    
    return pos


def build_and_save_graphMIS(graph_data, filename, highlight_nodes=None,  pos=None,):
    directory = 'graphApp/static/graphApp/images'
    G = nx.DiGraph()
    

    for node, edges in graph_data.items():
        for adjacent_node, weight in edges.items():
            G.add_edge(node, adjacent_node, weight=weight)
    
    if pos is None:
        pos = nx.spring_layout(G, seed=42) 
    
    plt.figure(figsize=(12, 12))
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor((255/255, 253/255, 250/255, 1.0))
    
    ax.set_axis_off()
    
    node_color_rgb = (81/255, 40/255, 132/255) 
    highlight_color_rgb = (255/255, 0/255, 0/255)  
    
    node_colors = [highlight_color_rgb if node in highlight_nodes else node_color_rgb for node in G.nodes()]
    

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)
    

    nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, font_color='black')
    
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
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
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_color_rgb)
    
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
    grouped = defaultdict(set)
    
    for item in data:
        depth, values = item
        grouped[depth].add(tuple(values)) 
    
    sorted_depths = sorted(grouped.keys())
    
    sorted_data = []
    for depth in sorted_depths:
        sorted_data.extend((depth, list(values)) for values in grouped[depth])
    
    return sorted_data



def to_military_time(time_tuples):
    def convert_to_military(time):
        return f"{time:02d}:00"

    military_time_tuples = [(convert_to_military(start), convert_to_military(end)) for start, end in time_tuples]
    
    return military_time_tuples



def getColors(nodes, n):
    colors = []
    for entry in nodes: 
        arr = [0] * n
        first_list, second_list = entry 
        for num in first_list:
            index = int(num)
            if 0 <= index < n:
                arr[index] = 1
        
       
        for num in second_list:
            index = int(num)
            if 0 <= index < n and arr[index] == 0:
                arr[index] = 2
        
        colors.append(arr)
    return colors


import networkx as nx
import matplotlib.pyplot as plt
import os

def graphIteration(graph_data, filename, colors, pos=None):
    directory = 'graphApp/static/graphApp/images'
    G = nx.DiGraph()

    for node, edges in graph_data.items():
        for adjacent_node, weight in edges.items():
            G.add_edge(node, adjacent_node, weight=weight)
    
    if pos is None:
        pos = nx.spring_layout(G, seed=42)
    
    nodes = list(G.nodes())
    sorted_nodes = sorted(nodes) 
    
    node_colors_dict = {node: colors[i] for i, node in enumerate(sorted_nodes)}
    

    print("Node colors:")
    for node in sorted_nodes:
        print(f"Node: {node}, Assigned Color Index: {node_colors_dict[node]}")
    
    nx.set_node_attributes(G, node_colors_dict, 'color')
    
    color_map = {0: 'white', 1: 'red', 2: 'black'}
    
    
    node_color_values = [color_map[G.nodes[node]['color']] for node in sorted_nodes]
    
    plt.figure(figsize=(12, 12))
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor((255/255, 253/255, 250/255, 1.0))
    
    ax.set_axis_off() #border
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_color_values)

    print("\nNode positions and colors:")
    for node in sorted_nodes:
        print(f"Node: {node}, Position: {pos[node]}, Color: {node_color_values[sorted_nodes.index(node)]}")
    
    nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, font_color='black')
   
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='white')

    
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    
    return pos


def rearrange(top, bottom):

    bottomInt = [int(x) for x in bottom]
    pos = [-1] * len(bottom)

    for i in range(len(top)):
        # print(top[i])
        pos[bottomInt[i]] = top[i]
        # print(bottomInt[i])

    return pos 