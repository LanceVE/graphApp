def knapsackDP(wt, val, W, n):
    from ..views import t
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                t[i][w] = 0
            elif wt[i - 1] <= w:
                t[i][w] = max(val[i - 1] + t[i - 1][w - wt[i - 1]], t[i - 1][w])
            else:
                t[i][w] = t[i - 1][w]
    return t[n][W]

def buildTable(n, val, wt, t):
    table = [[-1] * (n + 4) for _ in range(len(val) + 2)]
    table[0][0] = 'pi-1'
    table[0][1] = 'wi-1'
    table[0][2] = ''
    table[1][0] = ''
    table[1][1] = ''
    
    #row 1
    for i in range(n + 1):
        table[0][i + 3] = i

    #row 2
    for i in range (n + 1):
        table[1][i + 3] = 0

    #coulmn 1
    for i in range(2, len(val) + 2):
        table[i][0] = val[i - 2]

    #column 2
    for i in range(2, len(val) + 2):
        table[i][1] = wt[i - 2]
    
    #column 3
    for i in range(1, len(val) + 2):
        table[i][2] = 0

    print(t)
    for i in range(2, len(val) + 2):
        for j in range (3, len(table[0])):
            table[i][j] = t[i - 1][j - 3]

    for row in table:
         print(row)
    
    return table




