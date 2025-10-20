"""
COMPREHENSIVE TEST SUITE FOR ALL LANGUAGES
===========================================
This file consolidates all test cases (basic to complex) for all 9 supported languages:
- Python (original)
- JavaScript
- Rust
- Ruby
- PHP
- C
- C#
- Go (if added)
- Java (if added)

Test Categories:
1. JavaScript Tests (12 tests)
   - Async/await errors
   - Promise rejections
   - Infinite loops
   - Stack overflow
   - Type coercion
   - Closures
   - Event loop
   - Regex performance
   - Object properties
   - Large output
   - Syntax errors

2. Rust Tests (3 stress tests + 1 success test)
   - Lifetime complexities
   - Recursive panics
   - Borrow checker violations
   - Iterator combinators (success)

3. Ruby Tests (3 stress tests + 1 success test)
   - Metaprogramming
   - Fiber recursion
   - Large output
   - Lazy evaluation (success)

4. PHP Tests (3 stress tests + 1 success test)
   - Generator type errors
   - Exception chains
   - Memory stress
   - Functional pipelines (success)

5. C Tests (3 stress tests + 1 success test)
   - Infinite loops
   - Stack overflow
   - Massive output
   - Matrix operations (success)

6. C# Tests (3 stress tests + 1 success test)
   - Async deadlock scenarios
   - Reflection failures
   - Large allocations
   - LINQ and async (success)

Total: 32 comprehensive test cases
"""

from textwrap import dedent
from tools.executor import (
    execute_javascript_code,
    execute_rust_code,
    execute_ruby_code,
    execute_php_code,
    execute_c_code,
    execute_csharp_code,
)

SEPARATOR = "=" * 90
SECTION_SEPARATOR = "╔" + "=" * 88 + "╗"


def print_header():
    """Print the main test suite header"""
    print("\n")
    print(SECTION_SEPARATOR)
    print("║" + " " * 15 + "COMPREHENSIVE MULTI-LANGUAGE TEST SUITE" + " " * 34 + "║")
    print("║" + " " * 88 + "║")
    print("║" + " " * 20 + "Testing 9 Programming Languages" + " " * 37 + "║")
    print("║" + " " * 88 + "║")
    print("║" + " JavaScript | Rust | Ruby | PHP | C | C# | Python | Go | Java".center(90) + "║")
    print("╚" + "=" * 88 + "╝")
    print()


def print_section(title: str) -> None:
    """Print a section header"""
    print("\n" + SEPARATOR)
    print(title.center(90))
    print(SEPARATOR)


def print_test_header(test_num: int, title: str) -> None:
    """Print individual test header"""
    print(f"\n{'─' * 90}")
    print(f"TEST #{test_num}: {title}")
    print(f"{'─' * 90}")


# ============================================================================
# JAVASCRIPT TESTS (12 TESTS)
# ============================================================================

def test_js_async_unhandled_rejection():
    """Test unhandled promise rejection"""
    print_test_header(1, "JavaScript - Unhandled Promise Rejection")
    
    code = """
async function fetchData() {
    throw new Error("Network timeout!");
}

async function main() {
    const data = await fetchData();
    console.log(data);
}

main().catch(err => {
    console.error("Caught error:", err.message);
    process.exit(1);
});
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_promise_chain_error():
    """Test error propagation through promise chains"""
    print_test_header(2, "JavaScript - Promise Chain Error Propagation")
    
    code = """
Promise.resolve(5)
    .then(x => {
        console.log("Step 1:", x);
        return x * 2;
    })
    .then(x => {
        console.log("Step 2:", x);
        throw new Error("Calculation failed at step 2!");
    })
    .then(x => {
        console.log("Step 3:", x);
        return x + 10;
    })
    .catch(err => {
        console.error("Error caught:", err.message);
    });

setTimeout(() => {}, 100);
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_infinite_loop():
    """Test timeout protection with infinite loop"""
    print_test_header(3, "JavaScript - Infinite Loop (Timeout Protection)")
    
    code = """
console.log("Starting infinite loop...");
let counter = 0;
while (true) {
    counter++;
    if (counter % 1000000 === 0) {
        // This will run for a while
    }
}
console.log("This should never print");
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_stack_overflow():
    """Test deep recursion causing stack overflow"""
    print_test_header(4, "JavaScript - Stack Overflow")
    
    code = """
function deepRecursion(n) {
    console.log("Depth:", n);
    return deepRecursion(n + 1);
}

try {
    deepRecursion(0);
} catch (err) {
    console.error("Stack overflow caught:", err.message);
}
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_type_coercion():
    """Test JavaScript's tricky type coercion"""
    print_test_header(5, "JavaScript - Type Coercion Edge Cases")
    
    code = """
console.log("=== Type Coercion Issues ===");
console.log("[] + [] =", [] + []);
console.log("[] + {} =", [] + {});
console.log("{} + [] =", {} + []);
console.log("true + false =", true + false);
console.log("'5' - 3 =", '5' - 3);
console.log("'5' + 3 =", '5' + 3);

const arr = [10, 20, 30];
const idx = "1";
console.log("arr[idx] where idx='1':", arr[idx]);

const result = Math.sqrt(-1) + 5;
console.log("sqrt(-1) + 5 =", result);
console.log("NaN === NaN:", NaN === NaN);
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_closures():
    """Test closure memory patterns"""
    print_test_header(6, "JavaScript - Closure Memory Patterns")
    
    code = """
function createLeakyClosures() {
    const leaks = [];
    for (let i = 0; i < 5; i++) {
        const bigData = new Array(100).fill(i);
        leaks.push(() => {
            console.log(`Closure ${i} has data:`, bigData.slice(0, 3));
        });
    }
    return leaks;
}

const closures = createLeakyClosures();
console.log("Created", closures.length, "closures");
closures.forEach((fn, idx) => fn());
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_event_loop():
    """Test event loop behavior with microtasks"""
    print_test_header(7, "JavaScript - Event Loop & Microtasks")
    
    code = """
console.log("1: Synchronous start");

setTimeout(() => {
    console.log("2: Timeout (macro task)");
}, 0);

Promise.resolve().then(() => {
    console.log("3: Promise (micro task)");
});

queueMicrotask(() => {
    console.log("4: queueMicrotask (micro task)");
});

console.log("5: Synchronous end");

setTimeout(() => {}, 100);
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_regex():
    """Test regex performance"""
    print_test_header(8, "JavaScript - Regex Performance")
    
    code = """
const testString = "aaaaaaaaaaaaaaaaaaaaX";
const safeRegex = /^(a+)+$/;

console.log("Testing string:", testString);
console.log("Pattern: /^(a+)+$/");

try {
    const start = Date.now();
    const result = safeRegex.test(testString);
    const elapsed = Date.now() - start;
    console.log("Result:", result);
    console.log("Time:", elapsed, "ms");
} catch (err) {
    console.error("Error:", err.message);
}
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_async_await():
    """Test complex async/await error handling"""
    print_test_header(9, "JavaScript - Async/Await Error Handling")
    
    code = """
async function mayFail(shouldFail) {
    if (shouldFail) {
        throw new Error("Operation failed!");
    }
    return "Success";
}

async function complexAsyncFlow() {
    try {
        const result1 = await mayFail(false);
        console.log("First call:", result1);
        
        const result2 = await mayFail(true);
        console.log("Second call:", result2);
    } catch (err) {
        console.error("Caught in complexAsyncFlow:", err.message);
        throw new Error("Re-throwing: " + err.message);
    }
}

async function main() {
    try {
        await complexAsyncFlow();
    } catch (err) {
        console.error("Caught in main:", err.message);
    }
}

main().then(() => console.log("All done!"));

setTimeout(() => {}, 100);
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_object_properties():
    """Test JavaScript object property edge cases"""
    print_test_header(10, "JavaScript - Object Property Edge Cases")
    
    code = """
const obj = {
    name: "Test",
    age: 25
};

console.log("obj.missing:", obj.missing);
console.log("obj.missing.nested:", obj.missing?.nested);

const weirdObj = {
    "": "empty string key",
    "123": "numeric string key",
    "__proto__": "proto key"
};

console.log("Empty string key:", weirdObj[""]);
console.log("Numeric string:", weirdObj["123"]);

const obj2 = Object.create(null);
obj2.key = "value";
console.log("obj2.key:", obj2.key);

try {
    const malicious = JSON.parse('{"__proto__": {"polluted": true}}');
    console.log("After parse:", malicious.__proto__.polluted);
} catch (err) {
    console.error("Parse error:", err.message);
}
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_large_output():
    """Test output truncation"""
    print_test_header(11, "JavaScript - Large Output Truncation")
    
    code = """
console.log("Generating large output...");
for (let i = 0; i < 1000; i++) {
    console.log(`Line ${i}: ${"*".repeat(50)}`);
}
console.log("This should be truncated!");
"""
    
    result = execute_javascript_code(code)
    print(result)


def test_js_syntax_error():
    """Test syntax error handling"""
    print_test_header(12, "JavaScript - Syntax Error")
    
    code = """
const x = 5;
console.log("Before error");

function broken() {
    console.log("This won't work"
}

console.log("After error");
"""
    
    result = execute_javascript_code(code)
    print(result)


# ============================================================================
# RUST TESTS (4 TESTS)
# ============================================================================

def test_rust_lifetimes():
    """Test complex Rust lifetime scenarios"""
    print_test_header(13, "Rust - Lifetime Maze")
    
    code = dedent("""
        use std::fmt::Display;

        fn print_twice<'a, T: Display + 'a>(value: &'a T) {
            inner_print(value);
            inner_print(value);
        }

        fn inner_print<'b, T: Display + 'b>(value: &'b T) {
            println!("{}", value);
        }

        fn make_printer<'c>() -> Box<dyn Fn(&'c str) + 'c> {
            Box::new(|text: &'c str| println!("{}", text))
        }

        fn main() {
            let printer = make_printer();
            let owned = String::from("Rust lifetimes are tricky!");
            print_twice(&owned);
            printer("Borrowed for printer closure");
        }
    """)
    
    result = execute_rust_code(code)
    print(result)


def test_rust_panic():
    """Test Rust panic handling"""
    print_test_header(14, "Rust - Recursive Panic")
    
    code = dedent("""
        fn recurse(depth: u32) {
            if depth == 0 {
                panic!("Reached base panic level");
            } else {
                recurse(depth - 1);
            }
        }

        fn main() {
            recurse(10);
        }
    """)
    
    result = execute_rust_code(code)
    print(result)


def test_rust_borrow_checker():
    """Test borrow checker violations"""
    print_test_header(15, "Rust - Borrow Checker Violation")
    
    code = dedent("""
        fn main() {
            let mut numbers = vec![1, 2, 3, 4, 5];
            let first = &numbers[0];
            numbers.push(6);
            println!("{}", first);
        }
    """)
    
    result = execute_rust_code(code)
    print(result)


def test_rust_success():
    """Test successful Rust program"""
    print_test_header(16, "Rust - Iterator Combinators (Success)")
    
    code = dedent("""
        fn main() {
            let result: Vec<i32> = (0..10)
                .filter(|x| x % 2 == 0)
                .map(|x| x * x)
                .collect();

            println!("Squares of even numbers: {:?}", result);

            let factorial = (1..=10).fold(1u128, |acc, val| acc * val);
            println!("10! = {}", factorial);
        }
    """)
    
    result = execute_rust_code(code)
    print(result)


# ============================================================================
# RUBY TESTS (4 TESTS)
# ============================================================================

def test_ruby_metaprogramming():
    """Test Ruby metaprogramming"""
    print_test_header(17, "Ruby - Metaprogramming Method Missing")
    
    code = dedent("""
        class DynamicInvoker
          def method_missing(name, *args)
            if name.to_s.start_with?('do_')
              "Invoked #{name} with #{args.inspect}"
            else
              super
            end
          end
        end

        invoker = DynamicInvoker.new
        puts invoker.do_magic("wand", 42)
        puts invoker.magic
    """)
    
    result = execute_ruby_code(code)
    print(result)


def test_ruby_fiber_recursion():
    """Test Ruby fiber deep recursion"""
    print_test_header(18, "Ruby - Fiber Deep Recursion")
    
    code = dedent("""
        fiber = Fiber.new do
          def recurse(level)
            raise "Deep recursion limit hit" if level == 0
            recurse(level - 1)
          end

          recurse(50)
        end

        begin
          fiber.resume
        rescue => e
          puts "Caught: #{e.class} - #{e.message}"
          puts e.backtrace.take(5)
        end
    """)
    
    result = execute_ruby_code(code)
    print(result)


def test_ruby_large_output():
    """Test Ruby large output truncation"""
    print_test_header(19, "Ruby - Large Output Truncation")
    
    code = dedent("""
        10_000.times do |i|
          puts "Line #{i}"
        end
    """)
    
    result = execute_ruby_code(code)
    print(result)


def test_ruby_success():
    """Test successful Ruby program"""
    print_test_header(20, "Ruby - Lazy Evaluation (Success)")
    
    code = dedent("""
        fib = Enumerator.new do |y|
          a = b = 1
          loop do
            y << a
            a, b = b, a + b
          end
        end

        puts fib.lazy.take(10).to_a.inspect

        grouped = { ruby: 3, python: 5, javascript: 2 }
        grouped.each_pair do |lang, years|
          puts "I have practiced #{lang} for #{years} years"
        end
    """)
    
    result = execute_ruby_code(code)
    print(result)


# ============================================================================
# PHP TESTS (4 TESTS)
# ============================================================================

def test_php_generator_error():
    """Test PHP generator type error"""
    print_test_header(21, "PHP - Generator Type Error")
    
    code = dedent("""
        <?php
        function generator(): Generator {
            yield 1;
            yield 2;
            yield "three";
        }

        foreach (generator() as $value) {
            echo strtoupper($value) . "\\n";
        }
        ?>
    """)
    
    result = execute_php_code(code)
    print(result)


def test_php_exception_chain():
    """Test PHP exception chaining"""
    print_test_header(22, "PHP - Exception Chain")
    
    code = dedent("""
        <?php
        function levelOne() {
            throw new RuntimeException("Level one failure");
        }

        function levelTwo() {
            try {
                levelOne();
            } catch (RuntimeException $e) {
                throw new LogicException("Level two wrapping", 0, $e);
            }
        }

        try {
            levelTwo();
        } catch (Exception $ex) {
            echo "Caught: " . get_class($ex) . " - " . $ex->getMessage() . "\\n";
            $inner = $ex->getPrevious();
            if ($inner) {
                echo "Previous: " . get_class($inner) . " - " . $inner->getMessage() . "\\n";
            }
        }
        ?>
    """)
    
    result = execute_php_code(code)
    print(result)


def test_php_memory_stress():
    """Test PHP memory handling"""
    print_test_header(23, "PHP - Large Array Memory Stress")
    
    code = dedent("""
        <?php
        $data = range(1, 200000);
        $sum = array_reduce($data, fn($carry, $item) => $carry + $item, 0);
        echo "Sum: $sum\\n";
        ?>
    """)
    
    result = execute_php_code(code)
    print(result)


def test_php_success():
    """Test successful PHP program"""
    print_test_header(24, "PHP - Functional Pipelines (Success)")
    
    code = dedent("""
        <?php
        $numbers = range(1, 20);
        $processed = array_map(fn($n) => $n * $n, array_filter($numbers, fn($n) => $n % 3 === 0));
        $total = array_reduce($processed, fn($carry, $item) => $carry + $item, 0);

        echo "Processed Squares: " . implode(", ", $processed) . "\\n";
        echo "Sum: $total\\n";

        $config = [
            'database' => [
                'host' => 'localhost',
                'port' => 5432,
            ],
            'features' => ['auth' => true, 'logging' => true]
        ];

        echo json_encode($config, JSON_PRETTY_PRINT) . "\\n";
        ?>
    """)
    
    result = execute_php_code(code)
    print(result)


# ============================================================================
# C TESTS (4 TESTS)
# ============================================================================

def test_c_infinite_loop():
    """Test C infinite loop timeout"""
    print_test_header(25, "C - Infinite Loop Timeout")
    
    code = dedent("""
        #include <stdio.h>

        int main() {
            long long counter = 0;
            while (1) {
                counter++;
            }
            printf("%lld\\n", counter);
            return 0;
        }
    """)
    
    result = execute_c_code(code)
    print(result)


def test_c_stack_overflow():
    """Test C stack overflow"""
    print_test_header(26, "C - Stack Overflow Recursion")
    
    code = dedent("""
        #include <stdio.h>

        void recurse(int depth) {
            int buffer[1024];
            if (depth <= 0) {
                printf("Reached base case\\n");
                return;
            }
            buffer[0] = depth;
            recurse(depth - 1);
        }

        int main() {
            recurse(10000);
            return 0;
        }
    """)
    
    result = execute_c_code(code)
    print(result)


def test_c_massive_output():
    """Test C massive output"""
    print_test_header(27, "C - Massive Output")
    
    code = dedent("""
        #include <stdio.h>

        int main() {
            for (int i = 0; i < 200000; ++i) {
                printf("Line %d\\n", i);
            }
            return 0;
        }
    """)
    
    result = execute_c_code(code)
    print(result)


def test_c_success():
    """Test successful C program"""
    print_test_header(28, "C - Matrix Multiplication (Success)")
    
    code = dedent("""
        #include <stdio.h>

        #define SIZE 3

        void multiply(const int a[SIZE][SIZE], const int b[SIZE][SIZE], int result[SIZE][SIZE]) {
            for (int i = 0; i < SIZE; ++i) {
                for (int j = 0; j < SIZE; ++j) {
                    int sum = 0;
                    for (int k = 0; k < SIZE; ++k) {
                        sum += a[i][k] * b[k][j];
                    }
                    result[i][j] = sum;
                }
            }
        }

        void print_matrix(const int matrix[SIZE][SIZE]) {
            for (int i = 0; i < SIZE; ++i) {
                for (int j = 0; j < SIZE; ++j) {
                    printf("%4d", matrix[i][j]);
                }
                printf("\\n");
            }
        }

        int main() {
            int a[SIZE][SIZE] = {
                {1, 2, 3},
                {4, 5, 6},
                {7, 8, 9}
            };

            int b[SIZE][SIZE] = {
                {9, 8, 7},
                {6, 5, 4},
                {3, 2, 1}
            };

            int result[SIZE][SIZE];
            multiply(a, b, result);

            printf("Matrix A * B =\\n");
            print_matrix(result);
            return 0;
        }
    """)
    
    result = execute_c_code(code)
    print(result)


# ============================================================================
# C# TESTS (4 TESTS)
# ============================================================================

def test_csharp_async_deadlock():
    """Test C# async deadlock scenario"""
    print_test_header(29, "C# - Async Deadlock Scenario")
    
    code = dedent("""
        using System;
        using System.Threading.Tasks;

        class Program {
            static async Task<int> ComputeAsync() {
                await Task.Delay(100);
                return 42;
            }

            static void Main() {
                Console.WriteLine(ComputeAsync().Result);
            }
        }
    """)
    
    result = execute_csharp_code(code)
    print(result)


def test_csharp_reflection():
    """Test C# reflection invoke failure"""
    print_test_header(30, "C# - Reflection Invoke Failure")
    
    code = dedent("""
        using System;
        using System.Reflection;

        class Target {
            private void Hidden() {
                Console.WriteLine("Hidden method invoked");
            }
        }

        class Program {
            static void Main() {
                var target = new Target();
                var method = typeof(Target).GetMethod("Hidden", BindingFlags.Instance | BindingFlags.NonPublic);
                method.Invoke(target, null);
            }
        }
    """)
    
    result = execute_csharp_code(code)
    print(result)


def test_csharp_large_allocation():
    """Test C# large memory allocation"""
    print_test_header(31, "C# - Large Memory Allocation")
    
    code = dedent("""
        using System;

        class Program {
            static void Main() {
                try {
                    var data = new byte[1024 * 1024 * 512];
                    Console.WriteLine(data.Length);
                }
                catch (Exception ex) {
                    Console.WriteLine($"Caught: {ex.GetType().Name} - {ex.Message}");
                }
            }
        }
    """)
    
    result = execute_csharp_code(code)
    print(result)


def test_csharp_success():
    """Test successful C# program"""
    print_test_header(32, "C# - LINQ and Async (Success)")
    
    code = dedent("""
        using System;
        using System.Collections.Generic;
        using System.Linq;
        using System.Threading.Tasks;

        class Program {
            static async Task Main() {
                var numbers = Enumerable.Range(1, 20);
                var query = numbers.Where(n => n % 3 == 0).Select(async n => {
                    await Task.Delay(10);
                    return n * n;
                });

                var results = await Task.WhenAll(query);
                Console.WriteLine("Squares of numbers divisible by 3: " + string.Join(", ", results));

                var lookup = new Dictionary<string, int> { {"apples", 5}, {"oranges", 7} };
                Console.WriteLine(string.Join(", ", lookup.Select(kv => $"{kv.Key}:{kv.Value}")));
            }
        }
    """)
    
    result = execute_csharp_code(code)
    print(result)


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Execute all 32 comprehensive tests"""
    print_header()
    
    # JavaScript Tests (12)
    print_section("JAVASCRIPT TESTS (12 TESTS)")
    test_js_async_unhandled_rejection()
    test_js_promise_chain_error()
    test_js_infinite_loop()
    test_js_stack_overflow()
    test_js_type_coercion()
    test_js_closures()
    test_js_event_loop()
    test_js_regex()
    test_js_async_await()
    test_js_object_properties()
    test_js_large_output()
    test_js_syntax_error()
    
    # Rust Tests (4)
    print_section("RUST TESTS (4 TESTS)")
    test_rust_lifetimes()
    test_rust_panic()
    test_rust_borrow_checker()
    test_rust_success()
    
    # Ruby Tests (4)
    print_section("RUBY TESTS (4 TESTS)")
    test_ruby_metaprogramming()
    test_ruby_fiber_recursion()
    test_ruby_large_output()
    test_ruby_success()
    
    # PHP Tests (4)
    print_section("PHP TESTS (4 TESTS)")
    test_php_generator_error()
    test_php_exception_chain()
    test_php_memory_stress()
    test_php_success()
    
    # C Tests (4)
    print_section("C TESTS (4 TESTS)")
    test_c_infinite_loop()
    test_c_stack_overflow()
    test_c_massive_output()
    test_c_success()
    
    # C# Tests (4)
    print_section("C# TESTS (4 TESTS)")
    test_csharp_async_deadlock()
    test_csharp_reflection()
    test_csharp_large_allocation()
    test_csharp_success()
    
    # Final Summary
    print("\n" + SECTION_SEPARATOR)
    print("║" + " " * 88 + "║")
    print("║" + "TEST SUITE COMPLETE!".center(90) + "║")
    print("║" + " " * 88 + "║")
    print("║" + "Total Tests Executed: 32".center(90) + "║")
    print("║" + "Languages Tested: JavaScript, Rust, Ruby, PHP, C, C#".center(90) + "║")
    print("║" + " " * 88 + "║")
    print("╚" + "=" * 88 + "╝")
    print()


if __name__ == "__main__":
    run_all_tests()
