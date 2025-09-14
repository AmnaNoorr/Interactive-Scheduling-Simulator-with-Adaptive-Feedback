def sjf_preemptive(processes):
    processes = [p.copy() for p in processes]
    processes.sort(key=lambda x: x['arrival'])
    
    time = 0
    schedule = []
    remaining_burst = {p['pid']: p['burst'] for p in processes}
    completion_time = {p['pid']: 0 for p in processes}
    first_run = {p['pid']: -1 for p in processes}
    completed = set()
    
    while len(completed) < len(processes):
        ready = [p for p in processes 
                if p['arrival'] <= time 
                and p['pid'] not in completed 
                and remaining_burst[p['pid']] > 0]
        
        if ready:
            ready.sort(key=lambda x: remaining_burst[x['pid']])
            current = ready[0]
            
            if first_run[current['pid']] == -1:
                first_run[current['pid']] = time
                
            schedule.append({"pid": current['pid'], "start": time, "end": time + 1})
            remaining_burst[current['pid']] -= 1
            time += 1
            
            if remaining_burst[current['pid']] == 0:
                completed.add(current['pid'])
                completion_time[current['pid']] = time
        else:
            time += 1
    
    # Calculate metrics
    total_waiting = 0
    total_turnaround = 0
    total_response = 0
    
    for p in processes:
        ct = completion_time[p['pid']]
        at = p['arrival']
        bt = p['burst']
        fr = first_run[p['pid']]
        
        total_turnaround += ct - at
        total_waiting += (ct - at) - bt
        total_response += fr - at
    
    metrics = {
        'avg_waiting_time': total_waiting / len(processes),
        'avg_turnaround_time': total_turnaround / len(processes),
        'avg_response_time': total_response / len(processes),
        'cpu_utilization': (sum(p['burst'] for p in processes) / time) * 100
    }
    
    return schedule, metrics