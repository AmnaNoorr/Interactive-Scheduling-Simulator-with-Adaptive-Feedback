def mlfq_preemptive(processes, queue_quantums=None, num_queues=3, boost_interval=100):
    # Auto-generate queue quantums if not provided (exponential: 4, 8, 16...)
    if queue_quantums is None:
        queue_quantums = [2 ** (i + 2) for i in range(num_queues)]
    
    # Initialize process tracking
    for p in processes:
        p['remaining_burst'] = p['burst']
        p['current_queue'] = 0  # Highest priority queue
        p['start_time'] = None  # Track first execution time for response time
    
    queues = [[] for _ in range(num_queues)]
    current_time = 0
    completed = []
    schedule = []
    idle_time = 0

    while True:
        # Priority boost: Move all processes to top queue periodically
        if boost_interval > 0 and current_time % boost_interval == 0:
            for q in queues[1:]:
                while q:
                    p = q.pop(0)
                    p['current_queue'] = 0
                    queues[0].append(p)
        
        # Add newly arrived processes to top queue
        for p in processes:
            if p['arrival'] == current_time and p['remaining_burst'] > 0:
                p['current_queue'] = 0
                queues[0].append(p)
        
        # Find the highest priority non-empty queue
        selected_queue = next((i for i, q in enumerate(queues) if q), None)
        
        if selected_queue is not None:
            process = queues[selected_queue].pop(0)
            
            # Record start time for response time calculation (first run only)
            if process['start_time'] is None:
                process['start_time'] = current_time
            
            # Execute for up to the queue's time quantum
            time_quantum = queue_quantums[selected_queue]
            execution_time = min(time_quantum, process['remaining_burst'])
            
            # Record scheduling
            schedule.append({
                'pid': process['pid'],
                'start': current_time,
                'end': current_time + execution_time,
                'queue': selected_queue
            })
            
            # Update process and time
            process['remaining_burst'] -= execution_time
            current_time += execution_time
            
            # Check for new arrivals during execution
            for p in processes:
                if p['arrival'] < current_time and p['arrival'] >= current_time - execution_time:
                    if p['remaining_burst'] > 0 and p not in queues[p['current_queue']]:
                        p['current_queue'] = 0
                        queues[0].append(p)
            
            # Requeue or mark as completed
            if process['remaining_burst'] == 0:
                process['completion_time'] = current_time
                process['turnaround_time'] = current_time - process['arrival']
                process['waiting_time'] = process['turnaround_time'] - process['burst']
                process['response_time'] = process['start_time'] - process['arrival']
                completed.append(process)
            else:
                # Demote to lower priority queue if quantum expired
                new_queue = min(selected_queue + 1, num_queues - 1)
                process['current_queue'] = new_queue
                queues[new_queue].append(process)
        else:
            # No processes ready - advance time to next arrival
            next_arrival = min((p['arrival'] for p in processes if p['remaining_burst'] > 0), default=current_time)
            idle_time += next_arrival - current_time
            current_time = next_arrival
        
        # Exit when all processes complete
        if all(p['remaining_burst'] == 0 for p in processes):
            break
    
    # Calculate metrics
    total_time = current_time
    cpu_utilization = ((total_time - idle_time) / total_time) * 100 if total_time > 0 else 0
    
    avg_waiting = sum(p['waiting_time'] for p in completed) / len(completed) if completed else 0
    avg_turnaround = sum(p['turnaround_time'] for p in completed) / len(completed) if completed else 0
    avg_response = sum(p['response_time'] for p in completed) / len(completed) if completed else 0
    
    stats = {
        'avg_waiting_time': avg_waiting,
        'avg_turnaround_time': avg_turnaround,
        'avg_response_time': avg_response,
        'cpu_utilization': cpu_utilization,
        'total_time': total_time
    }
    
    return schedule, stats