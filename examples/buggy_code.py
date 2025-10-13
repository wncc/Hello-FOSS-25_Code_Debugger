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
print(calculate_average(empty_list))""",
    
    # JavaScript/Node.js Examples
    "js_syntax_error": """function add(a, b) {
    return a + b
}

// Missing closing brace
console.log(add(5, 3));""",
    
    "js_reference_error": """function greet(name) {
    let message = "Hello, " + name + "!";
    return messge;  // Typo here
}

console.log(greet("Alice"));""",
    
    "js_type_error": """function divide(a, b) {
    return a / b;
}

// Calling with wrong number of arguments
let result = divide(10);
console.log("Result: " + result);""",
    
    "js_undefined_error": """let person = {
    name: "John",
    age: 30
};

// Accessing non-existent property method
console.log(person.address.city);""",
    
    "js_async_error": """function fetchData() {
    setTimeout(() => {
        return "Data loaded";
    }, 1000);
}

// This won't work as expected
let data = fetchData();
console.log(data);""",
    
    "js_array_error": """function getThirdElement(arr) {
    return arr[2];
}

let myArray = [1, 2];
console.log(getThirdElement(myArray));""",
    
    # Rust Examples
    "rust_borrow_error": """fn main() {
    let s1 = String::from("hello");
    let s2 = s1;
    println!("{}", s1); // Error: value borrowed after move
}""",
    
    "rust_index_error": """fn main() {
    let v = vec![1, 2, 3];
    let third = v[5]; // Index out of bounds
    println!("The third element is {}", third);
}""",
    
    "rust_type_mismatch": """fn add_numbers(a: i32, b: i32) -> i32 {
    return a + b;
}

fn main() {
    let result = add_numbers(5, "10"); // Type mismatch
    println!("Result: {}", result);
}""",
    
    "rust_lifetime_error": """fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let result = longest("hello", "world");
    println!("Longest: {}", result);
}""",
    
    "rust_missing_semicolon": """fn main() {
    let x = 5
    let y = 10;
    println!("{}", x + y);
}""",
    
    # Ruby Examples
    "ruby_undefined_variable": """def greet(name)
  message = "Hello, #{name}!"
  puts messge  # Typo
end

greet("World")""",
    
    "ruby_no_method_error": """class Person
  def initialize(name)
    @name = name
  end
end

person = Person.new("Alice")
puts person.name  # Method not defined""",
    
    "ruby_division_by_zero": """def calculate_average(numbers)
  total = numbers.sum
  total / numbers.length
end

puts calculate_average([])""",
    
    "ruby_type_error": """def add(a, b)
  a + b
end

result = add(5, nil)  # Can't add nil
puts result""",
    
    "ruby_syntax_error": """def print_numbers
  [1, 2, 3].each do |num|
    puts num
  # Missing 'end' for the block
end

print_numbers""",
    
    # PHP Examples
    "php_undefined_variable": """<?php
function greet($name) {
    $message = "Hello, $name!";
    echo $messge;  // Typo
}

greet("World");
?>""",
    
    "php_array_index_error": """<?php
$fruits = array("apple", "banana");
echo $fruits[5];  // Index out of bounds
?>""",
    
    "php_type_error": """<?php
function divide($a, $b) {
    return $a / $b;
}

echo divide(10, "zero");  // Type error
?>""",
    
    "php_syntax_error": """<?php
function printNumbers() {
    $numbers = [1, 2, 3];
    foreach ($numbers as $num) {
        echo $num;
    // Missing closing brace
}

printNumbers();
?>""",
    
    "php_call_undefined_function": """<?php
function calculateSum($a, $b) {
    return $a + $b;
}

$result = calculateProduct(5, 10);  // Function doesn't exist
echo $result;
?>""",

    # === C Examples ===
    "c_segmentation_fault": """#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    printf("%d\\n", arr[10]);  // Array index out of bounds
    return 0;
}""",

    "c_uninitialized_variable": """#include <stdio.h>

int main() {
    int x;  // Uninitialized variable
    printf("Value: %d\\n", x);  // Undefined behavior
    return 0;
}""",

    "c_null_pointer_dereference": """#include <stdio.h>

int main() {
    int *ptr = NULL;
    printf("%d\\n", *ptr);  // Dereferencing NULL pointer
    return 0;
}""",

    "c_missing_return_type": """#include <stdio.h>

main() {  // Missing return type
    printf("Hello World\\n");
    return 0;
}""",

    "c_format_string_mismatch": """#include <stdio.h>

int main() {
    int num = 42;
    printf("Number: %s\\n", num);  // Wrong format specifier
    return 0;
}""",

    # === C# Examples ===
    "csharp_null_reference": """using System;

class Program {
    static void Main() {
        string text = null;
        Console.WriteLine(text.Length);  // NullReferenceException
    }
}""",

    "csharp_index_out_of_range": """using System;

class Program {
    static void Main() {
        int[] numbers = {1, 2, 3};
        Console.WriteLine(numbers[5]);  // IndexOutOfRangeException
    }
}""",

    "csharp_divide_by_zero": """using System;

class Program {
    static void Main() {
        int a = 10;
        int b = 0;
        int result = a / b;  // DivideByZeroException
        Console.WriteLine(result);
    }
}""",

    "csharp_invalid_cast": """using System;

class Program {
    static void Main() {
        object obj = "Hello";
        int number = (int)obj;  // InvalidCastException
        Console.WriteLine(number);
    }
}""",

    "csharp_missing_semicolon": """using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello World")  // Missing semicolon
    }
}"""
}


