import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

def draw_gantt_chart(schedule, title="Gantt Chart", mlfq=False):
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')

    # Keep order and map colors
    pids = list(dict.fromkeys(entry["pid"] for entry in schedule))
    colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
    color_map = {pid: colors[i % len(colors)] for i, pid in enumerate(pids)}

    pid_y_pos = {pid: i+1 for i, pid in enumerate(pids)}

    # If MLFQ is enabled, divide processes into queues
    if mlfq:
        queue_levels = sorted(set(entry['queue'] for entry in schedule))  # Get unique queue levels
        queue_color_map = {queue: mcolors.TABLEAU_COLORS.get(f'C{i}', 'gray') for i, queue in enumerate(queue_levels)}

    for entry in schedule:
        start = entry["start"]
        duration = entry["end"] - start
        pid = entry["pid"]
        color = color_map[pid]
        y = pid_y_pos[pid]

        if mlfq:
            queue_level = entry.get("queue", 0)  # Default queue level is 0 (top level)
            color = queue_color_map.get(queue_level, 'gray')  # Use color for queue level

        ax.broken_barh([(start, duration)], (y, 0.8), facecolors=color, edgecolor='white', linewidth=1.5)
        ax.text(start + duration/2, y + 0.4, f"P{pid}", ha='center', va='center', color='white', fontsize=10, fontweight='bold')

    ax.set_xlabel("Time", color='white', fontsize=12)
    ax.set_ylabel("Processes", color='white', fontsize=12)

    ax.set_yticks(list(pid_y_pos.values()))
    ax.set_yticklabels([f"P{pid}" for pid in pids], color='white', fontsize=10)
    ax.set_xticks(range(0, max(entry["end"] for entry in schedule) + 2))
    ax.set_xlim(0, max(entry["end"] for entry in schedule) + 1)

    ax.grid(True, axis='x', color='gray', linestyle='--', alpha=0.5)
    ax.tick_params(colors='white')
    ax.set_title(f"{title}", color='white', fontsize=16, fontweight='bold')

    #  Add a Legend
    patches = [mpatches.Patch(color=color_map[pid], label=f"P{pid}") for pid in pids]
    
    if mlfq:
        # Adding a legend for MLFQ queue levels
        queue_patches = [mpatches.Patch(color=color, label=f"Queue {queue}") for queue, color in queue_color_map.items()]
        patches.extend(queue_patches)

    ax.legend(handles=patches, loc='upper right', frameon=False, labelcolor='white', fontsize=10)

    plt.tight_layout()
    plt.show()
