def  maxincrease(arr):
    n = len(arr)
    dp = [1] * n
    max_len = 1

    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
        max_len = max(max_len, dp[i])
    
    mis = []
    current_len = max_len
    for i in range(n-1, -1, -1):
        if dp[i] == current_len:
            mis.append(arr[i])
            current_len -= 1
    mis.reverse()

    return max_len, mis
