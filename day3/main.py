import re
import sys

def solve_part1(input_text):
    # Regular expression to match valid mul(X,Y) patterns
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    
    # Find all valid matches
    matches = re.finditer(pattern, input_text)
    
    total = 0
    for match in matches:
        # Extract the numbers from each match
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        # Multiply and add to total
        result = num1 * num2
        total += result
        
    return total

def solve_part2(input_text):
    # Regular expressions for all instruction types
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'
    
    # Combine patterns and use regex to find all instructions with their positions
    combined_pattern = f'({mul_pattern})|({do_pattern})|({dont_pattern})'
    matches = list(re.finditer(combined_pattern, input_text))
    
    # Process instructions in order
    enabled = True  # mul instructions are enabled by default
    total = 0
    
    for match in matches:
        full_match = match.group(0)
        
        if full_match == "do()":
            enabled = True
        elif full_match == "don't()":
            enabled = False
        else:  # it's a mul instruction
            if enabled:
                # Extract numbers from mul instruction
                nums = re.match(mul_pattern, full_match)
                num1 = int(nums.group(1))
                num2 = int(nums.group(2))
                result = num1 * num2
                total += result
    
    return total

def main():
    # Get input filename from command line argument, default to 'input.txt'
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    
    # Read input from file
    with open(input_file, 'r') as file:
        input_text = file.read().strip()

    # Calculate and print results for both parts
    part1_result = solve_part1(input_text)
    part2_result = solve_part2(input_text)
    
    print(f"Part 1: The sum of all multiplication results is: {part1_result}")
    print(f"Part 2: The sum of all enabled multiplication results is: {part2_result}")

if __name__ == "__main__":
    main() 