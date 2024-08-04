def kmp(text, pattern):
    n = len(text)
    m = len(pattern)
    f = compute_failure_function(pattern)
    j = 0
    matches = []
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = f[j - 1]
        if text[i] == pattern[j]:
            if j == m - 1:
                matches.append(i - m + 1)
                j = f[j]
            else:
                j += 1

    return matches

def compute_failure_function(pattern):
    m = len(pattern)
    f = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = f[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        f[i] = j

    return f