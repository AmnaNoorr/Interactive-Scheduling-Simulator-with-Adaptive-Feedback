# Interactive Scheduling Simulator with Adaptive Feedback

An educational CPU scheduling simulator built in Python that helps users compare classical scheduling strategies through interactive process input, execution summaries, and Gantt chart visualization.

The project provides both a graphical interface and a console-based workflow for experimenting with process scheduling behavior. It is suitable for operating systems coursework, lab demonstrations, and algorithm comparison exercises.

## Features

- Interactive process entry with validation for PID, arrival time, burst time, and priority where required.
- Support for multiple CPU scheduling algorithms in one simulator.
- Graphical user interface built with Tkinter.
- Gantt chart visualization using Matplotlib.
- Performance summaries including waiting time, turnaround time, response time, and CPU utilization when available.
- Algorithm-specific controls for preemptive execution, Round Robin quantum, and Multi-Level Feedback Queue settings.

## Supported Algorithms

The simulator currently includes:

- First Come First Serve (FCFS)
- Shortest Job First (SJF, non-preemptive)
- Shortest Remaining Time First / Preemptive SJF
- Round Robin (RR)
- Priority Scheduling (non-preemptive)
- Priority Scheduling (preemptive)
- Multi-Level Feedback Queue (MLFQ, preemptive)

## Tech Stack

- Python 3
- Tkinter for the desktop interface
- Matplotlib for Gantt chart rendering

## Project Structure

```text
Simulator/
├── fcfs.py              # FCFS scheduler
├── gantt_chart.py       # Gantt chart visualization
├── gui.py               # Tkinter GUI entry point
├── main.py              # Console-based runner
├── mlfq.py              # Preemptive MLFQ implementation
├── performance.py       # Shared performance helpers
├── preemptive_sjf.py    # Preemptive SJF implementation
├── priority.py          # Non-preemptive priority scheduling
├── priority1.py         # Preemptive priority scheduling
├── rr.py                # Round Robin scheduler
└── sjf.py               # Non-preemptive SJF scheduler
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AmnaNoorr/Interactive-Scheduling-Simulator-with-Adaptive-Feedback.git
cd Interactive-Scheduling-Simulator-with-Adaptive-Feedback
```

### 2. Install dependencies

Matplotlib is required for visualization. Tkinter is included with many Python distributions, but on some Linux systems it must be installed separately.

```bash
pip install matplotlib
```

If Tkinter is missing on Ubuntu or Debian-based systems:

```bash
sudo apt install python3-tk
```

## Running the Project

### GUI Mode

Launch the desktop simulator from the `Simulator` directory:

```bash
cd Simulator
python3 gui.py
```

The GUI allows you to:

- Add processes one by one.
- Choose a scheduling algorithm.
- Toggle preemptive execution when applicable.
- Enter a Round Robin time quantum.
- Configure queue time quantums for MLFQ.
- Run the simulation and inspect a Gantt chart and summary metrics.

### Console Mode

The repository also includes a terminal-based runner:

```bash
cd Simulator
python3 main.py
```

The console version supports:

- Adding processes interactively.
- Running a selected scheduling algorithm.
- Clearing the current process list.
- Viewing printed scheduling output and metrics.

## Input Model

Each process is represented with the following attributes:

- `pid`: Unique process identifier
- `arrival`: Arrival time
- `burst`: CPU burst time
- `priority`: Priority value for priority-based and MLFQ runs

## Reported Metrics

Depending on the selected algorithm, the simulator reports some or all of the following:

- Average waiting time
- Average turnaround time
- Average response time
- CPU utilization
- Total execution time

## How the Simulator Helps Learning

This project is useful for understanding how scheduler design affects:

- Process wait time and completion time
- Responsiveness under preemptive policies
- Fairness tradeoffs in time-sliced scheduling
- Queue behavior in feedback-based scheduling
- Overall CPU utilization patterns

## Notes

- The GUI is the primary interactive experience and includes algorithm-specific controls not available in a single unified console flow.
- Gantt chart rendering opens through Matplotlib, so a desktop-capable Python environment is recommended.
- The codebase is structured as individual algorithm modules, which makes it straightforward to extend with additional schedulers or metric calculations.

## Future Improvements

Potential next enhancements include:

- Exporting results to CSV or JSON
- Adding a requirements file for faster setup
- Including automated tests for scheduling correctness
- Showing per-process metrics in the GUI
- Adding sample workloads and benchmark presets
