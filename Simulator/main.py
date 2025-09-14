from fcfs import fcfs
from sjf import sjf
from preemptive_sjf import sjf_preemptive
from rr import rr
from priority import priority_scheduling
from priority1 import priority_preemptive
from mlfq import mlfq_preemptive
from gantt_chart import draw_gantt_chart


def run_and_display(name, func, processes):
    print(f"\nRunning {name} Scheduling:")
    schedule, metrics = func(processes)
    for item in schedule:
        print(item)
    print("\nMetrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.2f}")
    draw_gantt_chart(schedule, name)

def get_process_input(require_priority=False):
    processes = []
    used_pids = set()
    num = int(input("Enter number of processes: "))

    for _ in range(num):
        while True:
            try:
                pid = int(input("Enter PID (unique integer): "))
                if pid in used_pids:
                    print("Duplicate PID not allowed.")
                    continue
                arrival = int(input(f"Enter arrival time for P{pid}: "))
                burst = int(input(f"Enter burst time for P{pid}: "))
                process = {'pid': pid, 'arrival': arrival, 'burst': burst}
                if require_priority:
                    priority = int(input(f"Enter priority for P{pid} (0 = highest): "))
                    process['priority'] = priority
                processes.append(process)
                used_pids.add(pid)
                break
            except ValueError:
                print("Please enter valid integers.")
    return processes

# Global variable to store processes
processes = []

# Function to handle the UI behavior
def main_ui():
    global processes
    
    # Loop until the user decides to exit
    while True:
        print("\nChoose an option:")
        print("1. Add processes")
        print("2. Run a selected algorithm")
        print("3. Clear processes")
        print("4. Exit")

        choice = input("Enter choice (1, 2, 3, or 4): ")

        if choice == '1':
            # Allow the user to add processes
            new_processes = get_process_input()  # Get new processes
            processes.extend(new_processes)  # Append new processes to the global list
        elif choice == '2':
            # Ensure processes are entered before selecting algorithm
            if not processes:
                print("No processes entered. Please add processes first.")
                continue
            
            print("\nSelect Scheduling Algorithm:")
            print("1. FCFS")
            print("2. SJF (Non-Preemptive)")
            print("3. SJF (Preemptive)")
            print("4. Round Robin")
            print("5. Priority Scheduling (Non-Preemptive)")
            print("6. Priority Scheduling (Preemptive)")
            print("7. MLFQ (Non-Preemptive)")
            print("8. MLFQ (Preemptive)")

            algo_choice = input("Enter choice (1-8): ")

            if algo_choice == '1':
                run_and_display("FCFS", fcfs, processes)
            elif algo_choice == '2':
                run_and_display("SJF", sjf, processes)
            elif algo_choice == '3':
                run_and_display("Preemptive SJF", sjf_preemptive, processes)
            elif algo_choice == '4':
                tq = int(input("Enter time quantum for Round Robin: "))
                run_and_display("Round Robin", lambda p: rr(p, tq), processes)
            elif algo_choice == '5':
                priority_processes = get_process_input(require_priority=True)
                run_and_display("Priority Scheduling (Non-Preemptive)", priority_scheduling, priority_processes)
            elif algo_choice == '6':
                priority_processes = get_process_input(require_priority=True)
                run_and_display("Priority Scheduling (Preemptive)", priority_preemptive, priority_processes)
            elif algo_choice == '7':
                mlfq_processes = get_process_input(require_priority=True)
                run_and_display("MLFQ (Preemptive)", mlfq_preemptive, mlfq_processes)
            else:
                print("Invalid choice.")
        elif choice == '3':
            # Clear processes when selected
            print("Clearing all processes.")
            processes.clear()  # Reset processes list
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

# Run the UI
if __name__ == "__main__":
    main_ui()
