# basic_calculator.py
# CCCS 106 - Week 1 Lab Exercise
# Simple Interactive Calculator

import math

print("=" * 40)
print("BASIC CALCULATOR")
print("=" * 40)

# Get user input
print("Enter two numbers for calculation:")
try:
    num1 = float(input("First number: "))
    num2 = float(input("Second number: "))
    
    # Perform basic calculations
    addition = num1 + num2
    subtraction = num1 - num2
    multiplication = num1 * num2
    
    # Handle division by zero
    if num2 != 0:
        division = num1 / num2
    else:
        division = "Cannot divide by zero"
    
    # Power operation
    power = num1 ** num2
    
    # Square root operations
    if num1 >= 0:
        sqrt_num1 = math.sqrt(num1)
    else:
        sqrt_num1 = "Cannot calculate square root of negative number"
    
    if num2 >= 0:
        sqrt_num2 = math.sqrt(num2)
    else:
        sqrt_num2 = "Cannot calculate square root of negative number"
    
    # Factorial operations (only for non-negative integers)
    def calculate_factorial(n):
        if n < 0:
            return "Cannot calculate factorial of negative number"
        elif n != int(n):
            return "Cannot calculate factorial of decimal number"
        else:
            return math.factorial(int(n))
    
    factorial_num1 = calculate_factorial(num1)
    factorial_num2 = calculate_factorial(num2)
    
    # Display results
    print("\n" + "=" * 40)
    print("BASIC OPERATIONS:")
    print("=" * 40)
    print(f"{num1} + {num2} = {addition}")
    print(f"{num1} - {num2} = {subtraction}")
    print(f"{num1} * {num2} = {multiplication}")
    print(f"{num1} / {num2} = {division}")
    
    print("\n" + "=" * 40)
    print("ADVANCED OPERATIONS:")
    print("=" * 40)
    print(f"{num1} ^ {num2} = {power}")
    print(f"√{num1} = {sqrt_num1}")
    print(f"√{num2} = {sqrt_num2}")
    print(f"{num1}! = {factorial_num1}")
    print(f"{num2}! = {factorial_num2}")
    
    # Additional information
    print("\n" + "=" * 40)
    print("ADDITIONAL INFO:")
    print("=" * 40)
    print(f"Larger number: {max(num1, num2)}")
    print(f"Smaller number: {min(num1, num2)}")
    
except ValueError:
    print("Error: Please enter valid numbers only!")
except Exception as e:
    print(f"An error occurred: {e}")

print("\nThank you for using Basic Calculator!")