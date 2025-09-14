def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    schedule = []
    metrics = {"waiting_time": 0, "turnaround_time": 0, "cpu_utilization": 0}

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        start_time = time
        end_time = start_time + p['burst']
        time = end_time
        waiting_time = start_time - p['arrival']
        turnaround_time = waiting_time + p['burst']
        schedule.append({"pid": p['pid'], "start": start_time, "end": end_time})
        metrics["waiting_time"] += waiting_time
        metrics["turnaround_time"] += turnaround_time

    metrics["waiting_time"] /= len(processes)
    metrics["turnaround_time"] /= len(processes)
    metrics["cpu_utilization"] = (sum(p['burst'] for p in processes) / time) * 100

    return schedule, metrics
