def sjf(processes):
    processes = [p.copy() for p in processes]
    processes.sort(key=lambda x: (x['arrival'], x['burst']))
    time = 0
    schedule = []
    total_waiting = 0
    total_turnaround = 0
    
    while processes:
        ready = [p for p in processes if p['arrival'] <= time]
        if ready:
            ready.sort(key=lambda x: x['burst'])
            current = ready[0]
            start = time
            end = start + current['burst']
            
            schedule.append({"pid": current['pid'], "start": start, "end": end})
            total_waiting += start - current['arrival']
            total_turnaround += end - current['arrival']
            
            time = end
            processes.remove(current)
        else:
            time = min(p['arrival'] for p in processes)
    
    metrics = {
        'avg_waiting_time': total_waiting / len(schedule) if schedule else 0,
        'avg_turnaround_time': total_turnaround / len(schedule) if schedule else 0,
        'cpu_utilization': (sum(p['end']-p['start'] for p in schedule) / time * 100) if schedule else 0
    }
    
    return schedule, metrics