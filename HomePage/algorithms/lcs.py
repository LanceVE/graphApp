
def lcs(Y, X):
    m = len(X)
    n = len(Y)
    table = [[(0, 'Null')]*(n+3) for _ in range(m+3)]
    for j in range(2, n + 3):
        table[1][j] = (j - 2)
        table[j][1] = (j - 2)

    for j in range(3, n + 3):
        table[0][j] = Y[j-3]
        table[j][0] = X[j-3]
    for i in range(3):
        table[0][i] = ''
        if i < 2:
            table[1][i] = ''
            if i < 1:
                    table[2][i] = ''
    for i in range(2, m+3):
        for j in range(2, n+3):
            if i >= 3 and j >= 3:
                if X[i-3] == Y[j-3]:
                    table[i][j] = (table[i-1][j-1][0]+1, 'D')
                else:
                    if table[i-1][j][0] >= table[i][j-1][0]:
                        table[i][j] = (table[i-1][j][0], 'U')
                    else:
                        table[i][j] = (table[i][j-1][0], 'L')
 
    LCS = reconstruct_lcs(table, X)
 
    return table, LCS



def reconstruct_lcs(table, X):
    lcs_sequence = []
    m = len(X)
    n = len(table[0]) - 3  
    
    i, j = m + 2, n + 2 
    while i > 2 and j > 2:
        if table[i][j][1] == 'D':
            lcs_sequence.append(X[i - 3])
            i -= 1
            j -= 1
        elif table[i][j][1] == 'U':
            i -= 1
        else:  
            j -= 1
    
    return ''.join(reversed(lcs_sequence))
