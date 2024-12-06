import sys
from collections import defaultdict

def read_input(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def find_start(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '^':
                return x, y
    return None

def get_next_position(x, y, direction):
    if direction == 0:  # Up
        return x, y - 1
    elif direction == 1:  # Right
        return x + 1, y
    elif direction == 2:  # Down
        return x, y + 1
    else:  # Left
        return x - 1, y

def is_valid_position(x, y, grid):
    return (0 <= y < len(grid) and 
            0 <= x < len(grid[0]))

def simulate_guard_with_obstacle(grid, obstacle_pos=None):
    visited = set()
    # Use a dict to track position+direction combinations and when we first saw them
    position_history = {}
    x, y = find_start(grid)
    direction = 0  # 0: up, 1: right, 2: down, 3: left
    steps = 0
    max_steps = len(grid) * len(grid[0]) * 4  # Maximum possible unique states
    
    visited.add((x, y))
    position_history[(x, y, direction)] = steps
    
    while steps < max_steps:  # Add a maximum step limit
        steps += 1
        next_x, next_y = get_next_position(x, y, direction)
        
        # Check if guard is leaving the area
        if not is_valid_position(next_x, next_y, grid):
            return visited, False
            
        # Check for obstacles including the new one
        hits_obstacle = (grid[next_y][next_x] == '#' or 
                        (obstacle_pos and (next_x, next_y) == obstacle_pos))
            
        if hits_obstacle:
            direction = (direction + 1) % 4
        else:
            x, y = next_x, next_y
            visited.add((x, y))
            
            # Check for loops using position+direction state
            state = (x, y, direction)
            if state in position_history:
                return visited, True
            position_history[state] = steps
                
    return visited, False  # Exceeded maximum steps

def find_loop_positions(grid):
    base_visited, _ = simulate_guard_with_obstacle(grid)
    loop_positions = set()
    
    # Get potential positions
    potential_positions = set()
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    
    # Only check positions adjacent to the original path
    for x, y in base_visited:
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (is_valid_position(new_x, new_y, grid) and 
                grid[new_y][new_x] != '#' and 
                grid[new_y][new_x] != '^'):
                potential_positions.add((new_x, new_y))
    
    # Try placing an obstacle at each potential position
    for x, y in potential_positions:
        _, creates_loop = simulate_guard_with_obstacle(grid, (x, y))
        if creates_loop:
            loop_positions.add((x, y))
    
    return loop_positions

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)
        
    filename = sys.argv[1]
    grid = read_input(filename)
    
    # Part 1
    visited, _ = simulate_guard_with_obstacle(grid)
    print(f"Part 1: The guard will visit {len(visited)} distinct positions.")
    
    # Part 2
    loop_positions = find_loop_positions(grid)
    print(f"Part 2: There are {len(loop_positions)} positions where an obstacle would create a loop.")

if __name__ == "__main__":
    main() 