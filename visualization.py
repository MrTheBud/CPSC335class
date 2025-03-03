# visualizations.py
# Graph Animation Developer: Alex Islas
# Date: 2-27-25
# Purpose: Generates an animated bar graph demonstrating the step-by-step progression of a sorting algorithm
#          on a user-provided input array, with built-in start, pause/resume, and reset buttons.
# Generate an animated vertical bar graph from a JSONL log file for a specified sorting algorithm,
#    ensuring the final state is sorted for visual appeal with Index on x-axis and Value on y-axis.
#    
#    Parameters:
#    - log_file_path (str): Path to the JSONL log file containing sorting steps.
#    - algo_name (str): Name of the sorting algorithm (e.g., "Bubble Sort", "Merge Sort").

import matplotlib
matplotlib.use('TkAgg')             # Set TkAgg backend for interactive widgets with Tkinter
import matplotlib.pyplot as plt     # Import matplotlib's pyplot module for plotting
from matplotlib.animation import FuncAnimation # Import FuncAnimation for creating animations
from matplotlib.widgets import Button # Import Button for creating interactive buttons
import tkinter as tk                  # Import Tkinter for creating GUI
import json                         # Import JSON for parsing user input
import sys                          # Import sys for exiting the program

def plot_sorting_animation_from_json(log_file_path, algo_name):
    """
    Generate an animated vertical bar graph from a JSONL log file for a specified sorting algorithm,
    ensuring the final state is sorted for visual appeal with Index on x-axis and Value on y-axis.
    
    Parameters:
    - log_file_path (str): Path to the JSONL log file containing sorting steps.
    - algo_name (str): Name of the sorting algorithm (e.g., "Bubble Sort", "Merge Sort").
    """
    # Define mapping of full algorithm names to sorttype keys (case-insensitive)
    algo_map = {
        "bubble sort": "bubble",
        "merge sort": "merge",  # Matches "mergesplit", "mergecombine", etc.
        "quick sort": "quick",
        "radix sort": "radix",
        "linear search algorithm": "linear"
    }
    sorttype = algo_map.get(algo_name.lower(), None)
    if not sorttype:
        print(f"Error: Unknown algorithm '{algo_name}'. Supported: Bubble Sort, Merge Sort, Quick Sort, Radix Sort, Linear Search Algorithm")
        return
    
    # Read JSONL log file line-by-line and filter by sorttype
    states = []
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                data = json.loads(line.strip())  # Parse each JSON line
                for key, value in data.items():
                    # Match sorttype in key (e.g., "00_bubble_3" contains "bubble")
                    if sorttype in key.lower():
                        # Extract step number from key (e.g., "00_bubble_3" -> 00)
                        step_str = key.split('_')[0]
                        try:
                            step = int(step_str)  # Handle negative steps (e.g., "-1_mergesplit")
                        except ValueError:
                            print(f"Warning: Invalid step number in key '{key}'—skipping")
                            continue
                        states.append((step, value))
        # Sort by step number to ensure correct order
        states.sort(key=lambda x: x[0])
        states = [state[1] for state in states]  # Keep only arrays
        # Ensure the final state is sorted for visual appeal
        if states and states[-1] != sorted(states[-1]):
            states.append(sorted(states[-1].copy()))  # Append sorted version if not already sorted
        if not states:
            print(f"No steps found for '{algo_name}' in {log_file_path}")
            return
        print(f"Loaded {len(states)} steps for '{algo_name}' from JSON log file: {log_file_path}")
    except Exception as e:
        print(f"Error loading JSON log file {log_file_path}: {e}")
        return

    # Create a Tkinter root window to manage the event loop
    root = tk.Tk()
    root.withdraw()  # Hide the root window to avoid extra window

    # Create figure and axis for the vertical bar graph
    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size for better visibility
    # Use vertical bars with Index on x-axis and Value on y-axis
    bars = ax.bar(range(len(states[0])), states[0], color='skyblue', edgecolor='black', linewidth=1)
    # Set x-axis ticks to match array indices
    ax.set_xticks(range(len(states[0])))
    ax.set_xlabel("Index", fontsize=14, labelpad=10)           # Restored to Index
    ax.set_ylabel("Value", fontsize=14, labelpad=10)           # Restored to Value
    ax.set_title(f"{algo_name} Process", fontsize=16, pad=15)  # Set graph title
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)         # Grid on y-axis for value readability
    ax.set_ylim(0, max(max(states)) * 1.2)                     # Dynamic range based on all state values
    
    # Animation state variables
    original_arr = states[0].copy()  # Store initial array state
    current_arr = states[0].copy()   # Track current array state
    step_index = 0                   # Track current step in animation
    running = False                  # Flag to indicate if animation is running
    paused = True                    # Flag to indicate if animation is paused
    finished = False                   # Flag to track completion of animation
    generator = None                   # Generator for animation frames
    
    # Generator to yield states from the log
    def state_generator():
        nonlocal step_index, finished
        while step_index < len(states): # Loop through all states
            print(f"Updating to step {step_index}: {states[step_index]}")  # Debug each frame
            yield states[step_index]
            step_index += 1
        finished = True
        print("Animation finished")
    
    # Update function for animation frames
    def update(frame):
        nonlocal current_arr
        if running and not paused:
            current_arr = frame
            for i, val in enumerate(current_arr):  # Update vertical bars with heights
                bars[i].set_height(val)            # Set y-value for vertical bars
        return bars
    
    # Dummy generator to wait for Start
    def dummy_generator():
        while True:
            yield current_arr  # Yield current array indefinitely until Start
    
    # Initialize animation with dummy generator
    anim = FuncAnimation(fig, update, frames=dummy_generator(), save_count=len(states),
                         repeat=False, interval=3000)  # Set animation interval to 3 seconds
    anim.pause()                                       # Start animation in paused state
    
    # Start button
    def start(event):
        nonlocal anim, running, paused, step_index, generator, finished
        print("Start button clicked")
        if not running:
            step_index = 0
            finished = False
            generator = state_generator()
            anim = FuncAnimation(fig, update, frames=generator, save_count=len(states),
                                 repeat=False, interval=3000)
            anim.resume()
            running = True
            paused = False
            pause_button.label.set_text("Pause")
            print(f"Animation started for {algo_name}")
        elif paused and not finished:
            anim.resume()
            paused = False
            pause_button.label.set_text("Pause")
            print(f"Animation resumed for {algo_name}")
        fig.canvas.draw()  # Redraw canvas to reflect changes
    
    # Pause/Resume button 
    def pause_resume(event):
        nonlocal paused, running, finished
        print("Pause/Resume button clicked")
        if not running or finished:
            print("No animation to pause/resume—click Start or reset if finished")
            return
        if paused:
            anim.resume()
            paused = False
            pause_button.label.set_text("Pause")
            print(f"Animation resumed for {algo_name}")
        else:
            anim.pause()
            paused = True
            pause_button.label.set_text("Resume")
            print(f"Animation paused for {algo_name}")
        fig.canvas.draw()  # Redraw canvas to reflect changes
    
    # Reset button 
    def reset(event):
        nonlocal paused, running, step_index, current_arr, anim, generator, finished
        print("Reset button clicked")
        if anim is not None and not finished and hasattr(anim, 'event_source') and anim.event_source is not None:
            anim.pause()  # Only pause if animation is active and not finished
        current_arr = original_arr.copy()
        for i, val in enumerate(original_arr):
            bars[i].set_height(val)  # Update y-value for vertical bars
        step_index = 0
        running = False
        paused = True
        finished = False
        # Stop the current event source if it exists, then reinitialize
        if anim is not None and hasattr(anim, 'event_source') and anim.event_source is not None:
            anim.event_source.stop()
        anim = FuncAnimation(fig, update, frames=dummy_generator(), save_count=len(states),
                             repeat=False, interval=3000)
        anim.pause()
        pause_button.label.set_text("Resume")
        print(f"Animation reset to initial state for {algo_name}")
        fig.canvas.draw()  # Redraw canvas to reflect reset state

    # Define button axes (separate from plot area)
    ax_start = plt.axes([0.60, 0.01, 0.1, 0.05])  # Define position for Start button
    ax_pause = plt.axes([0.71, 0.01, 0.12, 0.05]) # Define position for Pause/Resume button
    ax_reset = plt.axes([0.84, 0.01, 0.1, 0.05])  # Define position for Reset button
    
    # Create buttons
    start_button = Button(ax_start, 'Start')
    pause_button = Button(ax_pause, 'Resume')
    reset_button = Button(ax_reset, 'Reset')
    
    # Connect buttons to callbacks
    start_button.on_clicked(start)
    pause_button.on_clicked(pause_resume)  # Corrected to on_clicked
    reset_button.on_clicked(reset)
    
    # Shutdown function for clean exit
    def on_close(event):
        print("Window closed—shutting down cleanly")
        if anim is not None and hasattr(anim, 'event_source') and anim.event_source is not None:
            anim.event_source.stop()  # Only stop if event_source exists
        plt.close(fig)                # Close the figure
        root.quit()                   # Quit the Tkinter main loop
        root.destroy()                # Destroy the Tkinter root window
    
    # Connect close event and run Tkinter loop
    fig.canvas.mpl_connect('close_event', on_close)
    plt.show()
    root.mainloop()



# ---- TEST CASE GENERATED BY AI ---- #
# TEST CODE
if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) < 3:
        print("Error: Please provide a JSONL log file path and algorithm name as command-line arguments")
        print("Usage: python visualizations.py <log_file.jsonl> <algo_name>")
        print("Supported algorithms: Bubble Sort, Merge Sort, Quick Sort, Radix Sort, Linear Search Algorithm")
        # Create a larger sample JSONL log file for testing bigger arrays
        sample_log = [
            {"00_bubble_0.000010": [64, 34, 25, 12, 22, 11, 90, 5, 87, 45]},
            {"01_bubble_0.000020": [34, 64, 25, 12, 22, 11, 90, 5, 87, 45]},
            {"02_bubble_0.000030": [34, 25, 64, 12, 22, 11, 90, 5, 87, 45]},
            {"03_bubble_0.000040": [25, 34, 64, 12, 22, 11, 90, 5, 87, 45]},
            {"04_bubble_0.000050": [25, 34, 12, 64, 22, 11, 90, 5, 87, 45]},
            {"05_bubble_0.000060": [25, 12, 34, 64, 22, 11, 90, 5, 87, 45]},
            {"06_bubble_0.000070": [12, 25, 34, 64, 22, 11, 90, 5, 87, 45]},
            {"07_bubble_0.000080": [12, 25, 34, 22, 64, 11, 90, 5, 87, 45]},
            {"08_bubble_0.000090": [12, 25, 22, 34, 64, 11, 90, 5, 87, 45]},
            {"09_bubble_0.000100": [12, 22, 25, 34, 64, 11, 90, 5, 87, 45]},
            {"10_bubble_0.000110": [12, 22, 25, 34, 11, 64, 90, 5, 87, 45]},
            {"11_bubble_0.000120": [12, 22, 25, 11, 34, 64, 90, 5, 87, 45]},
            {"12_bubble_0.000130": [12, 11, 22, 25, 34, 64, 90, 5, 87, 45]},
            {"13_bubble_0.000140": [11, 12, 22, 25, 34, 64, 90, 5, 87, 45]},
            {"14_bubble_0.000150": [11, 12, 22, 25, 34, 5, 64, 90, 87, 45]},
            {"15_bubble_0.000160": [11, 12, 22, 25, 5, 34, 64, 90, 87, 45]},
            {"16_bubble_0.000170": [11, 12, 22, 5, 25, 34, 64, 90, 87, 45]},
            {"17_bubble_0.000180": [11, 12, 5, 22, 25, 34, 64, 90, 87, 45]},
            {"18_bubble_0.000190": [5, 11, 12, 22, 25, 34, 64, 90, 87, 45]},
            {"19_bubble_0.000200": [5, 11, 12, 22, 25, 34, 64, 87, 90, 45]},
            {"20_bubble_0.000210": [5, 11, 12, 22, 25, 34, 64, 45, 87, 90]},
            {"21_bubble_0.000220": [5, 11, 12, 22, 25, 34, 45, 64, 87, 90]},
            {"22_bubble_0.000230": [5, 11, 12, 22, 25, 34, 45, 64, 87, 90]}
        ]
        with open('sorting_log.jsonl', 'w') as f:
            for entry in sample_log:
                f.write(json.dumps(entry) + '\n')
        log_file = 'sorting_log.jsonl'
        algo_name = "Bubble Sort"
    else:
        log_file = sys.argv[1]
        algo_name = sys.argv[2]
    
    print("Generating animated bar graph from JSONL log file")
    plot_sorting_animation_from_json(log_file, algo_name)
