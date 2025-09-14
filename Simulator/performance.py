def calculate_cpu_utilization(processes, total_time):
    total_burst_time = sum(p['burst'] for p in processes)
    return (total_burst_time / total_time) * 100 if total_time else 0

def calculate_average_response_time(processes, schedule):
    response_times = {}

    # Find the first start time of each process
    for entry in schedule:
        pid = entry['pid']
        if pid not in response_times:
            process = next(p for p in processes if p['pid'] == pid)
            response_times[pid] = entry['start'] - process['arrival']

    avg_response_time = sum(response_times.values()) / len(response_times)
    return avg_response_time
