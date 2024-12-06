import sys
from typing import List, Set, Tuple, Dict
from collections import defaultdict, deque

def parse_input(input_text: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    # Split input into rules and updates sections
    rules_text, updates_text = input_text.strip().split('\n\n')
    
    # Parse rules
    rules = []
    for line in rules_text.strip().split('\n'):
        before, after = map(int, line.split('|'))
        rules.append((before, after))
    
    # Parse updates
    updates = []
    for line in updates_text.strip().split('\n'):
        update = list(map(int, line.split(',')))
        updates.append(update)
    
    return rules, updates

def is_valid_order(update: List[int], rules: List[Tuple[int, int]]) -> bool:
    # Create a set of numbers in this update for quick lookup
    update_numbers = set(update)
    
    # Create a position map for quick index lookups
    positions = {num: i for i, num in enumerate(update)}
    
    # Check each applicable rule
    for before, after in rules:
        # Skip rules that don't apply to this update
        if before not in update_numbers or after not in update_numbers:
            continue
            
        # If the rule applies, check if the order is correct
        if positions[before] >= positions[after]:
            return False
    
    return True

def get_middle_number(update: List[int]) -> int:
    return update[len(update) // 2]

def sort_update(update: List[int], rules: List[Tuple[int, int]]) -> List[int]:
    # Create a graph of dependencies
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    nodes = set(update)
    
    # Build the graph using only applicable rules
    for before, after in rules:
        if before in nodes and after in nodes:
            graph[before].add(after)
            in_degree[after] += 1
            # Ensure both nodes are in in_degree dict
            if before not in in_degree:
                in_degree[before] = 0

    # Topological sort using Kahn's algorithm
    result = []
    queue = deque([node for node in nodes if in_degree[node] == 0])
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result

def main():
    # Get input filename from command line argument, default to 'input.txt'
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    
    with open(input_file, 'r') as file:
        input_text = file.read()

    # Parse input
    rules, updates = parse_input(input_text)
    
    # Part 1: Find valid updates and sum their middle numbers
    total_part1 = 0
    for update in updates:
        if is_valid_order(update, rules):
            middle = get_middle_number(update)
            total_part1 += middle
    
    print(f"Part 1 - Sum of middle numbers from valid updates: {total_part1}")
    
    # Part 2: Sort invalid updates and sum their middle numbers
    total_part2 = 0
    for update in updates:
        if not is_valid_order(update, rules):
            sorted_update = sort_update(update, rules)
            middle = get_middle_number(sorted_update)
            total_part2 += middle
    
    print(f"Part 2 - Sum of middle numbers from sorted invalid updates: {total_part2}")

if __name__ == "__main__":
    main() 