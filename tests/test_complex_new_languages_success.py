"""
Execute complex but correct programs for the five newly added languages:
- Rust
- Ruby
- PHP
- C
- C#

Each snippet exercises non-trivial language features while remaining error-free.
We simply print the executor outputs so it is easy to inspect the behavior.
"""

from textwrap import dedent

from tools.executor import (
    execute_rust_code,
    execute_ruby_code,
    execute_php_code,
    execute_c_code,
    execute_csharp_code,
)

SEPARATOR = "=" * 90

def print_section(title: str) -> None:
    print("\n" + SEPARATOR)
    print(title)
    print(SEPARATOR)


def run_test(label: str, executor, code: str) -> None:
    print(f"\n[TEST] {label}")
    print("-" * 90)
    try:
        result = executor(code)
    except Exception as exc:
        result = f"Python exception surfaced: {exc}"
    print(result)


# ============================================================================
# Rust
# ============================================================================
print_section("RUST CORRECT PROGRAM")

run_test(
    "Rust - Iterator Combinators",
    execute_rust_code,
    dedent(
        """
        fn main() {
            let result: Vec<i32> = (0..10)
                .filter(|x| x % 2 == 0)
                .map(|x| x * x)
                .collect();

            println!("Squares of even numbers: {:?}", result);

            let factorial = (1..=10).fold(1u128, |acc, val| acc * val);
            println!("10! = {}", factorial);
        }
        """
    ),
)

# ============================================================================
# Ruby
# ============================================================================
print_section("RUBY CORRECT PROGRAM")

run_test(
    "Ruby - Enumerator with Lazy Evaluation",
    execute_ruby_code,
    dedent(
        """
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
        """
    ),
)

# ============================================================================
# PHP
# ============================================================================
print_section("PHP CORRECT PROGRAM")

run_test(
    "PHP - Functional Pipelines",
    execute_php_code,
    dedent(
        """
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
        """
    ),
)

# ============================================================================
# C
# ============================================================================
print_section("C CORRECT PROGRAM")

run_test(
    "C - Matrix Multiplication",
    execute_c_code,
    dedent(
        """
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
        """
    ),
)

# ============================================================================
# C#
# ============================================================================
print_section("C# CORRECT PROGRAM")

run_test(
    "C# - LINQ and Async",
    execute_csharp_code,
    dedent(
        """
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
        """
    ),
)

print("\n" + SEPARATOR)
print("Successful program execution sweep complete!")
print(SEPARATOR + "\n")
