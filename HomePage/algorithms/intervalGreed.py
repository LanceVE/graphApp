def intervalGreed(intervals):
    intervals.sort(key=lambda x: x[1])
    
    max_tasks = []
    last_end_time = float('-inf')
    
    for interval in intervals:
        start, end = interval
        if start >= last_end_time:
            last_end_time = end
            max_tasks.append(interval)
    
    return max_tasks