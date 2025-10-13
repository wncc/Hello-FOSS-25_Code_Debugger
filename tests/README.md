# Test Suite for Multi-Language Code Debugger

This directory contains comprehensive test suites for validating the implementation of all supported languages in the Code Debugger.

## Test Files Overview

### 1. `test_complex_new_languages.py`
**Purpose**: Stress testing for the 5 newly implemented languages (Rust, Ruby, PHP, C, C#)

**Tests Included**: 15 complex error scenarios (3 per language)

**Rust Tests** (3 tests):
- **Lifetime Maze**: Tests complex lifetime and borrow checker errors
- **Recursive Panic**: Tests deep recursion causing panic
- **Mutable/Immutable Borrow Clash**: Tests simultaneous mutable and immutable borrows

**Ruby Tests** (3 tests):
- **Metaprogramming Method Missing**: Tests dynamic method invocation errors
- **Fiber Deep Recursion**: Tests fiber-based recursion limits
- **Large Output Truncation**: Tests output limit handling (20,000 lines)

**PHP Tests** (3 tests):
- **Generator Type Error**: Tests type errors in generator functions
- **Exception Chain**: Tests nested exception handling
- **Large Array Memory**: Tests memory stress with 100,000 element array

**C Tests** (3 tests):
- **Infinite Loop**: Tests timeout protection (15-second limit)
- **Stack Overflow**: Tests deep recursion causing stack overflow
- **Massive Output**: Tests output truncation with 50,000 lines

**C# Tests** (3 tests):
- **Async Deadlock**: Tests Task.Result deadlock scenario
- **Reflection Invoke Failure**: Tests reflection API errors
- **Large Allocation**: Tests memory allocation stress (10 million integers)

**How to Run**:
```bash
cd C:\Users\sayan\Hello-FOSS-25_Code_Debugger
python tests\test_complex_new_languages.py
```

**Expected Results**: All tests should demonstrate proper error handling, timeout protection, and output truncation.

---

### 2. `test_complex_new_languages_success.py`
**Purpose**: Validation testing with correct, working programs for all 5 new languages

**Tests Included**: 5 successful programs (1 per language)

**Rust Test**:
- **Iterator Combinators**: Demonstrates filter, map, and fold operations
- **Expected Output**: Squares of even numbers and factorial calculation

**Ruby Test**:
- **Enumerator with Lazy Evaluation**: Demonstrates Fibonacci sequence and lazy evaluation
- **Expected Output**: First 10 Fibonacci numbers and formatted experience data

**PHP Test**:
- **Functional Pipelines**: Demonstrates array operations and JSON processing
- **Expected Output**: Filtered/mapped array results and formatted JSON

**C Test**:
- **Matrix Multiplication**: Implements 3x3 matrix multiplication
- **Expected Output**: Correctly multiplied matrix result

**C# Test**:
- **LINQ and Async**: Demonstrates LINQ queries and async/await patterns
- **Expected Output**: Filtered numbers and grouped data

**How to Run**:
```bash
cd C:\Users\sayan\Hello-FOSS-25_Code_Debugger
python tests\test_complex_new_languages_success.py
```

**Expected Results**: All tests should execute successfully with exit code 0 and produce correct output.

---

### 3. `test_complex_js.py`
**Purpose**: Comprehensive testing of JavaScript/Node.js implementation

**Tests Included**: 12 complex JavaScript scenarios

**Test Categories**:

1. **Async/Await & Promises** (3 tests):
   - Unhandled promise rejection
   - Promise chain error propagation
   - Complex async/await error handling

2. **Performance & Limits** (4 tests):
   - Infinite loop (timeout test)
   - Stack overflow (deep recursion)
   - Large output truncation
   - Regex catastrophic backtracking

3. **JavaScript Quirks** (3 tests):
   - Type coercion bugs
   - Closure memory patterns
   - Object property edge cases

4. **Event Loop** (1 test):
   - Event loop and microtask ordering

5. **Syntax Errors** (1 test):
   - Syntax error detection

**How to Run**:
```bash
cd C:\Users\sayan\Hello-FOSS-25_Code_Debugger
python tests\test_complex_js.py
```

**Expected Results**: All 12 tests should pass, demonstrating proper error handling, timeout protection, event loop behavior, and JavaScript-specific features.

---

## Prerequisites

### Required Language Installations:

1. **Node.js** (v22.19.0+): For JavaScript tests
   ```bash
   node --version
   ```

2. **Rust** (1.90.0+): For Rust tests
   ```bash
   rustc --version
   ```

3. **Ruby** (3.4.7+): For Ruby tests
   ```bash
   ruby --version
   ```

4. **PHP** (8.4.13+): For PHP tests
   ```bash
   php --version
   ```

5. **.NET SDK** (9.0.305+): For C# tests
   ```bash
   dotnet --version
   ```

6. **GCC** (MinGW): For C tests
   ```bash
   gcc --version
   ```

### Installation Guide:
Refer to `INSTALLATION_GUIDE.md` in the root directory for detailed installation instructions.

---

## Running All Tests

To run all test suites sequentially:

```bash
# From project root
python tests\test_complex_new_languages.py
python tests\test_complex_new_languages_success.py
python tests\test_complex_js.py
```

Or create a test runner script to execute all tests at once.

---

## Test Configuration

All tests use the following executor configuration:
- **Timeout**: 15 seconds per execution
- **Max Output Length**: 5000 characters
- **Temp File Cleanup**: Automatic

These settings are defined in `tools/executor.py`.

---

## Expected Test Durations

| Test Suite | Duration | Notes |
|------------|----------|-------|
| test_complex_new_languages.py | ~3-5 minutes | Includes timeout tests (15s each) |
| test_complex_new_languages_success.py | ~30-60 seconds | Quick validation tests |
| test_complex_js.py | ~30-45 seconds | JavaScript-specific tests |

**Total Runtime**: ~5-7 minutes for complete test suite

---

## Test Results Documentation

After running tests, results are documented in:
- `JAVASCRIPT_TEST_RESULTS.md` - Detailed JavaScript test analysis

---

## Troubleshooting

### Common Issues:

1. **"command not found" errors**
   - **Cause**: Language compiler/interpreter not installed
   - **Solution**: Install missing language (see INSTALLATION_GUIDE.md)

2. **Timeout errors**
   - **Cause**: Expected behavior for infinite loop tests
   - **Solution**: Verify timeout is exactly 15 seconds

3. **Output truncation**
   - **Cause**: Expected behavior for large output tests
   - **Solution**: Verify truncation occurs at 5000 characters

4. **Import errors**
   - **Cause**: Running from wrong directory
   - **Solution**: Always run from project root directory

---

## Contributing

When adding new language support:

1. Add stress tests to `test_complex_new_languages.py`
2. Add success validation to `test_complex_new_languages_success.py`
3. Update this README with new test descriptions
4. Ensure all tests pass before submitting PR

---

## Test Coverage

Current language coverage:
- ✅ Python (original implementation)
- ✅ C++ (original implementation)
- ✅ Java (original implementation)
- ✅ JavaScript/Node.js (12 complex tests)
- ✅ Rust (3 stress tests + 1 success test)
- ✅ Ruby (3 stress tests + 1 success test)
- ✅ PHP (3 stress tests + 1 success test)
- ✅ C (3 stress tests + 1 success test)
- ✅ C# (3 stress tests + 1 success test)

**Total**: 9 languages, 30+ test scenarios
