"""
Sample buggy code snippets for testing the debugger.
"""

BUGGY_CODE_SAMPLES = {
    "syntax_error": """def add(a, b)
    return a + b

# Test the function
result = add(5, 3)
print(f"5 + 3 = {result}")""",
    
    "indentation_error": """def calculate_factorial(n):
if n == 0:
return 1
else:
    return n * calculate_factorial(n - 1)

print(calculate_factorial(5))""",
    
    "logic_error": """def find_max(numbers):
    max_num = 0
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

# This will fail with negative numbers
test_list = [-5, -2, -8, -1]
print(f"Maximum: {find_max(test_list)}")""",
    
    "type_error": """def divide_numbers(a, b):
    return a / b

# This will cause a type error
result = divide_numbers("10", 2)
print(f"Result: {result}")""",
    
    "name_error": """def greet(name):
    message = f"Hello, {name}!"
    return mesage  # Typo here
    
print(greet("Alice"))""",
    
    "index_error": """def get_third_element(lst):
    return lst[2]

my_list = [1, 2]
print(get_third_element(my_list))""",
    
    "zero_division": """def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

# This will cause ZeroDivisionError
empty_list = []
print(calculate_average(empty_list))"""
}


