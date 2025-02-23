# visualization.py
# Graph Dev: Alex Islas
# Date: 2-22-2025
# Description: Generates a animation graph demonstrating the step-by-step progression of
#               a sorting algorithm from user input array. Support for start, pause and reset.
#
# Line 40: interval = 3000 = 3 seconds. Adjust this value to change the animation speed.

import matplotlib.pyplot as plt  # For creating graphs
from matplotlib.animation import FuncAnimation # For animating graphs

# --- Animated bar graph demonstrating the step-by-step progression --- 
def plot_sorting_animation(algo_name, algo_func, arr):
    plt.ion() # Turn on interactive mode (vscode does not like running the animation)

    fig, ax = plt.subplots(figsize = (10, 6)) # Create a new figure

    # Plot bars with initial array values
    bars = ax.bar(range(len(arr)), arr, color = 'skyblue', edgecolor = 'black', linewidth = 1)

    ax.set_xlabel("Index", fontsize = 14, labelpad = 10) # X-axis label
    ax.set_ylabel("Value", fontsize = 14, labelpad = 10) # Y-axis label
    ax.set_title(f"{algo_name} Sorting Process", fontsize = 16, pad = 15) # Title with algorithm name

    ax.grid(True, axis = 'y', linestyle = '--', alpha = 0.7) # Show grid lines for better readability
    ax.set_ylim(0, max(arr) * 1.2) # Set y-axis limits to prevent cutoff

    def update(frame):                    # Function to update the graph at each frame
        for bar, val in zip(bars, frame): # Update bar height to the current frame value
            bar.set_height(val)           # Update bar height to the current frame value
        fig.canvas.draw()
        fig.canvas.flush_events()
        return bars                       # Return the bars to be redrawn by Matplotlib

    # Create a generator which will be calling the sorting algortihms
    generator = algo_func(arr.copy()) # Copy preserves the origional array

    # Create the animation
    # interval: 3000 is 3 seconds
    anim = FuncAnimation(fig, update, frames = generator, repeat = False, interval = 3000, blit = True)
    return fig, anim  # Return the figure and animations objects




### ------- TESTS, GENERATED BY AN AI FOR TESING -------- ###
# --- Test Case ---
if __name__ == "__main__":
    def mock_bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    yield arr

    test_arr = [5, 3, 8, 1, 9]
    test_algo_name = ["Bubble Sort"]

    print("Generating animated bar graph for", test_algo_name)
    fig, anim = plot_sorting_animation(test_algo_name, mock_bubble_sort, test_arr)

    if fig:
        plt.figure(fig.number)
        plt.show(block=True) # Change block to true to keep the plot open until you close it
    else:
        print("Animation generation failed.")

    print("Test case completed. Animation should run until finished or window closed!")
