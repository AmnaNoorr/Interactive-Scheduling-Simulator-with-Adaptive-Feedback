import tkinter as tk
from tkinter import ttk, messagebox
from fcfs import fcfs
from sjf import sjf
from preemptive_sjf import sjf_preemptive
from rr import rr
from priority import priority_scheduling
from priority1 import priority_preemptive
from mlfq import mlfq_preemptive  # Only import preemptive MLFQ
from gantt_chart import draw_gantt_chart

processes = []

def validate_process(process):
    """Validate process fields"""
    required_fields = ['pid', 'arrival', 'burst']
    for field in required_fields:
        if field not in process:
            raise ValueError(f"Missing required field: {field}")
        if field == 'pid':
            if not process[field]:
                raise ValueError("PID cannot be empty")
        else:
            if not isinstance(process[field], (int, float)) or process[field] < 0:
                raise ValueError(f"Invalid value for {field}: {process[field]}")
    return True

def add_process():
    try:
        pid = entry_pid.get().strip()
        arrival = int(entry_arrival.get())
        burst = int(entry_burst.get())
        
        if not pid:
            raise ValueError("PID cannot be empty")
        
        if any(str(p['pid']) == str(pid) for p in processes):
            raise ValueError(f"Process with PID '{pid}' already exists")

        process = {'pid': pid, 'arrival': arrival, 'burst': burst}

        algo = algorithm_var.get()
        if algo in ["Priority Scheduling", "Priority Preemptive", "MLFQ"]:
            priority = entry_priority.get()
            if not priority:
                raise ValueError("Priority is required for this algorithm")
            process['priority'] = int(priority)

        validate_process(process)
        processes.append(process)
        
        process_info = f"PID={pid}, Arrival={arrival}, Burst={burst}"
        if 'priority' in process:
            process_info += f", Priority={process['priority']}"
        process_listbox.insert(tk.END, process_info)

        entry_pid.delete(0, tk.END)
        entry_arrival.delete(0, tk.END)
        entry_burst.delete(0, tk.END)
        entry_priority.delete(0, tk.END)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def clear_processes():
    processes.clear()
    process_listbox.delete(0, tk.END)

def toggle_controls(*args):
    algo = algorithm_var.get()
    
    # Clear fields when switching algorithms
    entry_priority.delete(0, tk.END)
    entry_tq.delete(0, tk.END)
    for entry in tq_entries:
        entry.delete(0, tk.END)
    
    # Show/hide priority field
    if algo in ["Priority Scheduling", "Priority Preemptive", "MLFQ"]:
        label_priority.grid()
        entry_priority.grid()
    else:
        label_priority.grid_remove()
        entry_priority.grid_remove()
    
    # Show/hide time quantum field
    if algo == "RR":
        label_tq.grid()
        entry_tq.grid()
        mlfq_frame.grid_remove()
    elif algo == "MLFQ":
        label_tq.grid_remove()
        entry_tq.grid_remove()
        mlfq_frame.grid()
        # Force preemptive for MLFQ
        preemptive_var.set(True)
        preemptive_check.config(state=tk.DISABLED)
    else:
        label_tq.grid_remove()
        entry_tq.grid_remove()
        mlfq_frame.grid_remove()
    
    # Enable/disable preemptive checkbox
    if algo in ["FCFS", "RR", "MLFQ"]:
        preemptive_check.config(state=tk.DISABLED)
        if algo != "MLFQ":
            preemptive_var.set(False)
    else:
        preemptive_check.config(state=tk.NORMAL)

def run_simulation():
    if not processes:
        messagebox.showerror("Error", "No processes added")
        return

    try:
        # Validate all processes before running
        for process in processes:
            validate_process(process)
            
        algo = algorithm_var.get()
        is_preemptive = preemptive_var.get()

        if algo == "FCFS":
            result, summary = fcfs(processes.copy())
        elif algo == "SJF":
            if is_preemptive:
                result, summary = sjf_preemptive(processes.copy())
            else:
                result, summary = sjf(processes.copy())
        elif algo == "RR":
            tq = entry_tq.get()
            if not tq:
                raise ValueError("Time quantum is required for RR")
            tq = int(tq)
            if tq <= 0:
                raise ValueError("Time quantum must be positive")
            result, summary = rr(processes.copy(), tq)
        elif algo == "Priority Scheduling":
            result, summary = priority_scheduling(processes.copy())
        elif algo == "Priority Preemptive":
            result, summary = priority_preemptive(processes.copy())
        elif algo == "MLFQ":
            queues = []
            for entry in tq_entries:
                q = entry.get()
                if q:
                    try:
                        quantum = int(q)
                        if quantum <= 0:
                            raise ValueError("Time quantum must be positive")
                        queues.append(quantum)
                    except ValueError:
                        raise ValueError("Invalid time quantum value")
            
            if not queues:
                raise ValueError("Enter at least one Time Quantum for MLFQ")
            
            # Always use preemptive MLFQ
            result, summary = mlfq_preemptive(processes.copy(), queues)
        else:
            raise ValueError("Unknown algorithm selected")

        draw_gantt_chart(result)
        show_summary(summary)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_summary(summary):
    summary_window = tk.Toplevel(root)
    summary_window.title("Simulation Summary")
    
    text = tk.Text(summary_window, wrap=tk.WORD, width=50, height=10)
    text.pack(padx=10, pady=10)
    
    summary_text = (f"Algorithm: {algorithm_var.get()}\n"
                   f"Preemptive: {preemptive_var.get()}\n\n"
                   f"Average Waiting Time: {summary['avg_waiting_time']:.2f}\n"
                   f"Average Turnaround Time: {summary['avg_turnaround_time']:.2f}\n")
    
    if 'avg_response_time' in summary:
        summary_text += f"Average Response Time: {summary['avg_response_time']:.2f}\n"
    if 'cpu_utilization' in summary:
        summary_text += f"CPU Utilization: {summary['cpu_utilization']:.2f}%"
    
    text.insert(tk.END, summary_text)
    text.config(state=tk.DISABLED)
    
    close_button = ttk.Button(summary_window, text="Close", command=summary_window.destroy)
    close_button.pack(pady=5)

# GUI Setup
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("900x650")

# Main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Input frame
input_frame = ttk.LabelFrame(main_frame, text="Process Input", padding="10")
input_frame.pack(fill=tk.X, pady=5)

# Process input fields
ttk.Label(input_frame, text="PID:").grid(row=0, column=0, padx=5)
entry_pid = ttk.Entry(input_frame, width=15)
entry_pid.grid(row=0, column=1, padx=5)

ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=2, padx=5)
entry_arrival = ttk.Entry(input_frame, width=15)
entry_arrival.grid(row=0, column=3, padx=5)

ttk.Label(input_frame, text="Burst Time:").grid(row=0, column=4, padx=5)
entry_burst = ttk.Entry(input_frame, width=15)
entry_burst.grid(row=0, column=5, padx=5)

label_priority = ttk.Label(input_frame, text="Priority:")
label_priority.grid(row=0, column=6, padx=5)
entry_priority = ttk.Entry(input_frame, width=15)
entry_priority.grid(row=0, column=7, padx=5)
label_priority.grid_remove()
entry_priority.grid_remove()

# Buttons
button_frame = ttk.Frame(input_frame)
button_frame.grid(row=1, column=0, columnspan=8, pady=10)

btn_add = ttk.Button(button_frame, text="Add Process", command=add_process)
btn_add.pack(side=tk.LEFT, padx=5)

btn_clear = ttk.Button(button_frame, text="Clear All", command=clear_processes)
btn_clear.pack(side=tk.LEFT, padx=5)

# Algorithm selection frame
algo_frame = ttk.LabelFrame(main_frame, text="Algorithm Settings", padding="10")
algo_frame.pack(fill=tk.X, pady=5)

ttk.Label(algo_frame, text="Algorithm:").grid(row=0, column=0, padx=5)
algorithm_var = tk.StringVar()
algorithm_menu = ttk.Combobox(algo_frame, textvariable=algorithm_var, state="readonly",
                             values=["FCFS", "SJF", "RR", "Priority Scheduling", "Priority Preemptive", "MLFQ"])
algorithm_menu.grid(row=0, column=1, padx=5)
algorithm_var.set("FCFS")
algorithm_var.trace_add("write", toggle_controls)

# Time quantum input (for RR)
label_tq = ttk.Label(algo_frame, text="Time Quantum:")
entry_tq = ttk.Entry(algo_frame, width=15)
label_tq.grid(row=0, column=2, padx=5)
entry_tq.grid(row=0, column=3, padx=5)
label_tq.grid_remove()
entry_tq.grid_remove()

# Preemptive checkbox
preemptive_var = tk.BooleanVar()
preemptive_check = ttk.Checkbutton(algo_frame, text="Preemptive", variable=preemptive_var)
preemptive_check.grid(row=0, column=4, padx=5)

# MLFQ settings frame
mlfq_frame = ttk.Frame(algo_frame)
mlfq_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky=tk.W)
mlfq_frame.grid_remove()

mlfq_labels = ["High Priority Queue TQ:", "Medium Priority Queue TQ:", "Low Priority Queue TQ:"]
tq_entries = []
for i, label_text in enumerate(mlfq_labels):
    ttk.Label(mlfq_frame, text=label_text).grid(row=0, column=i*2, padx=5)
    tq_entry = ttk.Entry(mlfq_frame, width=10)
    tq_entry.grid(row=0, column=i*2+1, padx=5)
    tq_entries.append(tq_entry)

# Run button
btn_run = ttk.Button(algo_frame, text="Run Simulation", command=run_simulation)
btn_run.grid(row=2, column=0, columnspan=5, pady=10)

# Process listbox
list_frame = ttk.LabelFrame(main_frame, text="Process List", padding="10")
list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

process_listbox = tk.Listbox(list_frame)
process_listbox.pack(fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(process_listbox)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
process_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=process_listbox.yview)

# Initialize controls
toggle_controls()

root.mainloop()