import sys
from collections import Counter

def calculate_distance(left_list, right_list):
    # Sort both lists to pair smallest with smallest, etc.
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    
    total_distance = 0
    # Calculate distance between each pair
    for left, right in zip(left_sorted, right_sorted):
        distance = abs(left - right)
        total_distance += distance
    
    return total_distance

def calculate_similarity(left_list, right_list):
    # Count occurrences of numbers in right list
    right_counts = Counter(right_list)
    
    total_similarity = 0
    # For each number in left list, multiply by its count in right list
    for num in left_list:
        total_similarity += num * right_counts[num]
    
    return total_similarity

def parse_input(input_text):
    left_list = []
    right_list = []
    
    for line in input_text.strip().split('\n'):
        # Split each line into left and right numbers
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)
    
    return left_list, right_list

def solve_part1(left_list, right_list):
    return calculate_distance(left_list, right_list)

def solve_part2(left_list, right_list):
    return calculate_similarity(left_list, right_list)

def main():
    # Get input filename from command line argument, default to 'input.txt'
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    
    # Read input from file
    try:
        with open(input_file, 'r') as file:
            input_text = file.read()
        
        # Parse the input
        left_list, right_list = parse_input(input_text)
        
        # Calculate and print results for both parts
        distance = solve_part1(left_list, right_list)
        similarity = solve_part2(left_list, right_list)
        
        print(f"Part 1 - Total distance between lists: {distance}")
        print(f"Part 2 - Similarity score: {similarity}")
    except FileNotFoundError:
        print(f"Error: {input_file} not found!")
        exit(1)

if __name__ == "__main__":
    main() 