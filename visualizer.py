import matplotlib.pyplot as plt  
import numpy as np  
import re
import subprocess

from matplotlib.lines import Line2D

def parse_occupied(file_path):  
    occupied = []
    pattern = r"\(occupied x(\d+) y(\d+)\)" 
    
    with open(file_path, 'r') as file:  
        for line in file:
            # Find matches using the regex pattern  
            match = re.match(pattern, line.strip())
            
            if match:  
                x1, y1 = match.groups()
                occupied.append((int(x1), int(y1)))

    return occupied

def parse_sas_plan(file_path):  
    path = {}
    pattern = r"\(move (.*?) x(\d+) y(\d+) x(\d+) y(\d+)\)" 
    
    with open(file_path, 'r') as file:  
        for line in file:
            # Find matches using the regex pattern  
            match = re.match(pattern, line.strip())
            
            if match:  
                piece, x1, y1, x2, y2 = match.groups()
                # Check if the piece is not in the path dictionary
                if piece not in path:
                    path[piece] = []
                 
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # Append only the ending position if the starting position is already in the path
                if not path[piece] or path[piece][-1] != (x1, y1):
                    path[piece].append((x1, y1))
                path[piece].append((x2, y2))
    return path  
  
def plot_board(paths, occupied_positions, board_width, board_height):  
    fig, ax = plt.subplots()  
  
    # Create a grid  
    for x in range(board_width + 1):  
        ax.axhline(x, lw=2, color='k', zorder=5)  
        ax.axvline(x, lw=2, color='k', zorder=5)  
  
    # Mark occupied positions  
    for (x, y) in occupied_positions:  
        ax.add_patch(plt.Rectangle((x-1, y-1), 1, 1, color='red', alpha=0.5))  
  
    # Plot the paths  
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    legend_handles = []
    annotated_positions = {}
    for i, (key, path) in enumerate(paths.items()):
        path_x, path_y = zip(*path)  
        color = colors[i % len(colors)]
        ax.plot(np.array(path_x) - 0.5, np.array(path_y) - 0.5, color + 'o-', linewidth=2, markersize=8, alpha=0.7, label=key)
        legend_handles.append(Line2D([0], [0], color=color, lw=2, label=key, alpha=0.7))
        
        # Annotate each step with its step number and set the color to match the path
        for step_num, (x, y) in enumerate(path):
            pos = (x, y)
            if pos not in annotated_positions:
                annotated_positions[pos] = 0
            else:
                annotated_positions[pos] += 1
            
            offset = annotated_positions[pos] * 10  # Adjust the offset value as needed
            ax.annotate(str(step_num + 1), (x - 0.5, y - 0.5), textcoords="offset points", xytext=(0,10 + offset), ha='center', color=color)
  
    # Mark starting and ending positions  
    for path in paths.values():
        ax.plot(path[0][0] - 0.5, path[0][1] - 0.5, 'go', markersize=10)  
        ax.plot(path[-1][0] - 0.5, path[-1][1] - 0.5, 'ro', markersize=10)  
  
    # Set limits and labels  
    ax.set_xlim(0, board_width)  
    ax.set_ylim(0, board_height)  
    ax.set_xticks(np.arange(board_width))  
    ax.set_yticks(np.arange(board_height))  
    ax.set_xticklabels(np.arange(1, board_width + 1))  
    ax.set_yticklabels(np.arange(1, board_height + 1))  
    ax.set_aspect('equal')  
  
    # Add legend with custom handles
    ax.legend(handles=legend_handles)
    ax.invert_yaxis()
  
    # Show the plot  
    plt.gca().invert_yaxis()  
    plt.show()  

def plot_solution(domain_file, problem_file, board_width, board_height):
    # Run the planner
    subprocess.run(['python', 'C:\\Users\\odind\\source\\ut\\downward\\fast-downward.py', '--alias', 'lama-first', domain_file, problem_file])
    
    # Parse the occupied positions in the problem file
    occupied_positions = parse_occupied(problem_file) 

    # Read the path from the sas_plan file  
    paths = parse_sas_plan('sas_plan')

    # Plot the board with the given path and occupied positions  
    plot_board(paths, occupied_positions, board_width, board_height)

# Define the board size  
board_width = 7  
board_height = 8  


# domain_file = 'single-king-domain.pddl'
# problem_file = 'single-king-problem.pddl'

domain_file = 'single-knight-domain.pddl'
# problem_file = 'single-knight-problem.pddl'
problem_file = 'dual-knights-problem.pddl'

plot_solution(domain_file=domain_file, 
              problem_file=problem_file, 
              board_width=board_width, 
              board_height=board_height)    