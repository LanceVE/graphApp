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


def to_military_time(time_tuples):
    def convert_to_military(time):
        return f"{time:02d}:00"

    military_time_tuples = [(convert_to_military(start), convert_to_military(end)) for start, end in time_tuples]
    
    return military_time_tuples