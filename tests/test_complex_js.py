"""
Complex JavaScript Test Suite
Tests the JavaScript executor with challenging edge cases including:
- Async/await errors
- Promise rejections
- Infinite loops (timeout test)
- Stack overflow
- Memory stress
- Complex error chains
"""

from tools.executor import execute_javascript_code

def test_js_async_unhandled_rejection():
    """Test unhandled promise rejection"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 1: Unhandled Promise Rejection")
    print("="*90)
    
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
    print()


def test_js_promise_chain_error():
    """Test error propagation through promise chains"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 2: Promise Chain Error Propagation")
    print("="*90)
    
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
        console.log("Step 3:", x); // Should not reach here
        return x + 10;
    })
    .catch(err => {
        console.error("Error caught:", err.message);
    });

// Keep process alive to see the output
setTimeout(() => {}, 100);
"""
    
    result = execute_javascript_code(code)
    print(result)
    print()


def test_js_infinite_loop():
    """Test timeout protection with infinite loop"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 3: Infinite Loop (Timeout Test)")
    print("="*90)
    
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
    print()


def test_js_stack_overflow():
    """Test deep recursion causing stack overflow"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 4: Stack Overflow")
    print("="*90)
    
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
    print()


def test_js_type_coercion_bugs():
    """Test JavaScript's tricky type coercion"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 5: Type Coercion Bugs")
    print("="*90)
    
    code = """
console.log("=== Type Coercion Issues ===");
console.log("[] + [] =", [] + []);
console.log("[] + {} =", [] + {});
console.log("{} + [] =", {} + []);
console.log("true + false =", true + false);
console.log("'5' - 3 =", '5' - 3);
console.log("'5' + 3 =", '5' + 3);

// Common bug: array indexing with string
const arr = [10, 20, 30];
const idx = "1";
console.log("arr[idx] where idx='1':", arr[idx]);

// NaN propagation
const result = Math.sqrt(-1) + 5;
console.log("sqrt(-1) + 5 =", result);
console.log("NaN === NaN:", NaN === NaN);
"""
    
    result = execute_javascript_code(code)
    print(result)
    print()


def test_js_closure_memory_leak():
    """Test closure memory patterns"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 6: Closure Memory Pattern")
    print("="*90)
    
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
    print()


def test_js_event_loop_microtasks():
    """Test event loop behavior with microtasks"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 7: Event Loop & Microtasks")
    print("="*90)
    
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

// Wait for async tasks
setTimeout(() => {}, 100);
"""
    
    result = execute_javascript_code(code)
    print(result)
    print()


def test_js_regex_catastrophic_backtracking():
    """Test regex performance issue"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 8: Regex with Potential Backtracking")
    print("="*90)
    
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
    print()


def test_js_async_await_error_handling():
    """Test complex async/await error handling"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 9: Async/Await Error Handling")
    print("="*90)
    
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
        console.log("Second call:", result2); // Won't reach here
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

// Keep process alive
setTimeout(() => {}, 100);
"""
    
    result = execute_javascript_code(code)
    print(result)
    print()


def test_js_object_property_pitfalls():
    """Test JavaScript object property edge cases"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 10: Object Property Edge Cases")
    print("="*90)
    
    code = """
const obj = {
    name: "Test",
    age: 25
};

// Accessing non-existent property
console.log("obj.missing:", obj.missing);
console.log("obj.missing.nested:", obj.missing?.nested); // Safe navigation

// Property name issues
const weirdObj = {
    "": "empty string key",
    "123": "numeric string key",
    "__proto__": "proto key"
};

console.log("Empty string key:", weirdObj[""]);
console.log("Numeric string:", weirdObj["123"]);

// hasOwnProperty issues
const obj2 = Object.create(null);
obj2.key = "value";
console.log("obj2.key:", obj2.key);

// Prototype pollution attempt (should be safe)
try {
    const malicious = JSON.parse('{"__proto__": {"polluted": true}}');
    console.log("After parse:", malicious.__proto__.polluted);
} catch (err) {
    console.error("Parse error:", err.message);
}
"""
    
    result = execute_javascript_code(code)
    print(result)
    print()


def test_js_large_output():
    """Test output truncation with large data"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 11: Large Output (Truncation Test)")
    print("="*90)
    
    code = """
console.log("Generating large output...");
for (let i = 0; i < 1000; i++) {
    console.log(`Line ${i}: ${"*".repeat(50)}`);
}
console.log("This should be truncated!");
"""
    
    result = execute_javascript_code(code)
    print(result)
    print()


def test_js_syntax_error():
    """Test syntax error handling"""
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST 12: Syntax Error")
    print("="*90)
    
    code = """
const x = 5;
console.log("Before error");

// Syntax error: missing closing brace
function broken() {
    console.log("This won't work"
}

console.log("After error");
"""
    
    result = execute_javascript_code(code)
    print(result)
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*88 + "╗")
    print("║" + " "*20 + "COMPREHENSIVE JAVASCRIPT COMPLEX TEST SUITE" + " "*25 + "║")
    print("╚" + "="*88 + "╝")
    
    test_js_async_unhandled_rejection()
    test_js_promise_chain_error()
    test_js_infinite_loop()
    test_js_stack_overflow()
    test_js_type_coercion_bugs()
    test_js_closure_memory_leak()
    test_js_event_loop_microtasks()
    test_js_regex_catastrophic_backtracking()
    test_js_async_await_error_handling()
    test_js_object_property_pitfalls()
    test_js_large_output()
    test_js_syntax_error()
    
    print("\n" + "="*90)
    print("JAVASCRIPT COMPLEX TEST SUITE COMPLETE!")
    print("="*90)
