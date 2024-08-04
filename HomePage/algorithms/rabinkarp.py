def search(txt, pat, q):
    patternFound = []
    M = len(pat)
    N = len(txt)
    if M > N:
        return  

    d = 256 
    h = 1
    p = 0   
    t = 0    
    j = 0   

    for i in range(M-1):
        h = (h * d) % q

    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

    for i in range(N - M + 1):
        if p == t:
            for j in range(M):
                if txt[i + j] != pat[j]:
                    break
            else:
                j += 1

            if j == M:
                print("Pattern found at index " + str(i))
                patternFound.append(i)

        if i < N - M:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
            if t < 0:
                t = t + q

    return patternFound