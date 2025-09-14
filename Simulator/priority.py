def priority_scheduling(processes):
    proc = [p.copy() for p in processes]  # Work on a copy
    proc.sort(key=lambda x: (x['arrival'], x.get('priority', 0)))
    time = 0
    schedule = []
    total_burst_time = 0
    metrics = {"waiting_time": 0, "turnaround_time": 0, "cpu_utilization": 0}

    while proc:
        ready_processes = [p for p in proc if p['arrival'] <= time]
        if ready_processes:
            ready_processes.sort(key=lambda x: x['priority'])
            p = ready_processes[0]
            start_time = time
            end_time = start_time + p['burst']
            time = end_time
            waiting_time = start_time - p['arrival']
            turnaround_time = waiting_time + p['burst']
            total_burst_time += p['burst']
            schedule.append({"pid": p['pid'], "start": start_time, "end": end_time})
            metrics["waiting_time"] += waiting_time
            metrics["turnaround_time"] += turnaround_time
            proc.remove(p)
        else:
            time += 1  # Idle time

    n = len(schedule)
    metrics["waiting_time"] /= n
    metrics["turnaround_time"] /= n
    metrics["cpu_utilization"] = (total_burst_time / time) * 100 if time else 0

    return schedule, metrics
