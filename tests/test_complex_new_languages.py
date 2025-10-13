"""
Complex stress tests for newly added language executors:
- Rust
- Ruby
- PHP
- C
- C#

Each test attempts to push the executor toward edge cases such as:
  * Deep recursion
  * Complex language features (lifetimes, metaprogramming, etc.)
  * Compilation failures with multi-line diagnostics
  * Runtime crashes (segmentation faults, panics)
  * Large output truncation handling

Running this script prints the captured output from every executor call so
we can manually inspect whether the tooling behaves correctly under stress.
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
    except Exception as exc:  # Catch unexpected Python-side failures
        result = f"Python exception surfaced: {exc}"
    print(result)


# ============================================================================
# Rust Tests
# ============================================================================
print_section("RUST COMPLEX TESTS")

run_test(
    "Rust - Lifetime Maze",
    execute_rust_code,
    dedent(
        """
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
        """
    ),
)

run_test(
    "Rust - Recursive Panic",
    execute_rust_code,
    dedent(
        """
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
        """
    ),
)

run_test(
    "Rust - Mutable/Immutable Borrow Clash",
    execute_rust_code,
    dedent(
        """
        fn main() {
            let mut numbers = vec![1, 2, 3, 4, 5];
            let first = &numbers[0];
            numbers.push(6); // Mutable borrow while immutable borrow active
            println!("{}", first);
        }
        """
    ),
)

# ============================================================================
# Ruby Tests
# ============================================================================
print_section("RUBY COMPLEX TESTS")

run_test(
    "Ruby - Metaprogramming Method Missing",
    execute_ruby_code,
    dedent(
        """
        class DynamicInvoker
          def method_missing(name, *args)
            if name.to_s.start_with?('do_')
              "Invoked #{name} with \\#{args.inspect}"
            else
              super
            end
          end
        end

        invoker = DynamicInvoker.new
        puts invoker.do_magic("wand", 42)
        puts invoker.magic  # Should raise NoMethodError
        """
    ),
)

run_test(
    "Ruby - Fiber Deep Recursion",
    execute_ruby_code,
    dedent(
        """
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
        """
    ),
)

run_test(
    "Ruby - Large Output Truncation",
    execute_ruby_code,
    dedent(
        """
        10_000.times do |i|
          puts "Line \\#{i}"
        end
        """
    ),
)

# ============================================================================
# PHP Tests
# ============================================================================
print_section("PHP COMPLEX TESTS")

run_test(
    "PHP - Generator Type Error",
    execute_php_code,
    dedent(
        """
        <?php
        function generator(): Generator {
            yield 1;
            yield 2;
            yield "three"; // Violates strict typing expectation
        }

        foreach (generator() as $value) {
            echo strtoupper($value) . "\n";
        }
        ?>
        """
    ),
)

run_test(
    "PHP - Exception Chain",
    execute_php_code,
    dedent(
        """
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
            echo "Caught: " . get_class($ex) . " - " . $ex->getMessage() . "\n";
            $inner = $ex->getPrevious();
            if ($inner) {
                echo "Previous: " . get_class($inner) . " - " . $inner->getMessage() . "\n";
            }
        }
        ?>
        """
    ),
)

run_test(
    "PHP - Large Array Memory Stress",
    execute_php_code,
    dedent(
        """
        <?php
        $data = range(1, 200000);
        $sum = array_reduce($data, fn($carry, $item) => $carry + $item, 0);
        echo "Sum: $sum\n";
        ?>
        """
    ),
)

# ============================================================================
# C Tests
# ============================================================================
print_section("C COMPLEX TESTS")

run_test(
    "C - Infinite Loop Timeout",
    execute_c_code,
    dedent(
        """
        #include <stdio.h>

        int main() {
            long long counter = 0;
            while (1) {
                counter++;
            }
            printf("%lld\\n", counter);
            return 0;
        }
        """
    ),
)

run_test(
    "C - Stack Overflow Recursion",
    execute_c_code,
    dedent(
        """
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
        """
    ),
)

run_test(
    "C - Massive Output",
    execute_c_code,
    dedent(
        """
        #include <stdio.h>

        int main() {
            for (int i = 0; i < 200000; ++i) {
                printf("Line %d\\n", i);
            }
            return 0;
        }
        """
    ),
)

# ============================================================================
# C# Tests
# ============================================================================
print_section("C# COMPLEX TESTS")

run_test(
    "C# - Async Deadlock Scenario",
    execute_csharp_code,
    dedent(
        """
        using System;
        using System.Threading.Tasks;

        class Program {
            static async Task<int> ComputeAsync() {
                await Task.Delay(100);
                return 42;
            }

            static void Main() {
                // Intentional deadlock-prone pattern
                Console.WriteLine(ComputeAsync().Result);
            }
        }
        """
    ),
)

run_test(
    "C# - Reflection Invoke Failure",
    execute_csharp_code,
    dedent(
        """
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
        """
    ),
)

run_test(
    "C# - Large Allocation",
    execute_csharp_code,
    dedent(
        """
        using System;

        class Program {
            static void Main() {
                try {
                    var data = new byte[1024 * 1024 * 512]; // 512 MB
                    Console.WriteLine(data.Length);
                }
                catch (Exception ex) {
                    Console.WriteLine($"Caught: {ex.GetType().Name} - {ex.Message}");
                }
            }
        }
        """
    ),
)

print("\n" + SEPARATOR)
print("Complex executor test sweep complete!")
print(SEPARATOR + "\n")
