def priority_preemptive(processes):
    processes = [p.copy() for p in processes]
    processes.sort(key=lambda x: x['arrival'])
    
    time = 0
    schedule = []
    remaining_burst = {p['pid']: p['burst'] for p in processes}
    completed = []
    start_times = {}
    end_times = {}
    
    while len(completed) < len(processes):
        # Get ready processes (arrived and not completed)
        ready = [p for p in processes if p['arrival'] <= time and p['pid'] not in completed and remaining_burst[p['pid']] > 0]
        
        if ready:
            # Select process with highest priority (lowest number)
            ready.sort(key=lambda x: x['priority'])
            current = ready[0]
            pid = current['pid']
            
            # Record start time if not already set
            if pid not in start_times:
                start_times[pid] = time
                current['response'] = time - current['arrival']
            
            # Execute for 1 time unit
            schedule.append({"pid": pid, "start": time, "end": time + 1})
            remaining_burst[pid] -= 1
            
            # Check if process completed
            if remaining_burst[pid] == 0:
                end_times[pid] = time + 1
                completed.append(pid)
                current['turnaround'] = end_times[pid] - current['arrival']
                current['waiting'] = current['turnaround'] - current['burst']
            
            time += 1
        else:
            # CPU idle
            time += 1
    
    # Calculate metrics
    total_waiting = sum(p.get('waiting', 0) for p in processes)
    total_turnaround = sum(p.get('turnaround', 0) for p in processes)
    total_response = sum(p.get('response', 0) for p in processes)
    total_time = max(end_times.values()) if end_times else 0
    
    metrics = {
        "avg_waiting_time": total_waiting / len(processes),
        "avg_turnaround_time": total_turnaround / len(processes),
        "avg_response_time": total_response / len(processes),
        "cpu_utilization": (sum(p['burst'] for p in processes) / total_time * 100) if total_time > 0 else 0
    }
    
    return schedule, metrics