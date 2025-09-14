def rr(processes, time_quantum):
    queue = processes[:]
    time = 0
    schedule = []
    metrics = {"waiting_time": 0, "turnaround_time": 0, "cpu_utilization": 0}

    while queue:
        p = queue.pop(0)
        burst_time = min(p['burst'], time_quantum)
        start_time = time
        end_time = start_time + burst_time
        time = end_time
        p['burst'] -= burst_time
        schedule.append({"pid": p['pid'], "start": start_time, "end": end_time})

        if p['burst'] > 0:
            queue.append(p)
        else:
            metrics["waiting_time"] += (start_time - p['arrival'])
            metrics["turnaround_time"] += (end_time - p['arrival'])

    metrics["waiting_time"] /= len(processes)
    metrics["turnaround_time"] /= len(processes)
    metrics["cpu_utilization"] = (sum(p['burst'] for p in processes) / time) * 100

    return schedule, metrics
