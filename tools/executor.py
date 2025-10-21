import subprocess
import sys
import os
import tempfile
import re
from langchain.tools import tool

TIMEOUT = 15  # Increased timeout for compiled languages
MAX_OUTPUT_LENGTH = 5000  # Prevent overly long outputs

# --- Existing Python Tool ---
@tool
def execute_python_code(code: str) -> str:
    """
    Executes a string of Python code in an isolated subprocess and returns the output.
    This tool is sandboxed and has a timeout.
    """
    process = None
    try:
        process = subprocess.Popen(
            [sys.executable, "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid if sys.platform != "win32" else None,
        )
        stdout, stderr = process.communicate(input="", timeout=TIMEOUT)
        
        # --- Added truncation here ---
        if len(stdout) > MAX_OUTPUT_LENGTH:
            stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
        if len(stderr) > MAX_OUTPUT_LENGTH:
            stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
        # -----------------------------

        output = []
        if stdout:
            output.append(f"--- STDOUT ---\n{stdout}")
        if stderr:
            output.append(f"--- STDERR ---\n{stderr}")
        
        return_code = process.returncode
        if return_code != 0:
            output.append(f"--- EXIT CODE: {return_code} ---")
        
        if not output:
            return "Code executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        if process:
            try:
                if sys.platform != "win32":
                    os.killpg(os.getpgid(process.pid), 15)
                else:
                    process.kill()
                process.communicate()
            except ProcessLookupError:
                pass
        return f"Error: Code execution timed out after {TIMEOUT} seconds and was terminated."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


# --- C++ Execution Tool ---
@tool
def execute_cpp_code(code: str) -> str:
    """
    Compiles and executes a string of C++ code and returns the output.
    Requires g++ to be installed and in the system's PATH.
    """
    with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name
    
    exe_suffix = ".exe" if sys.platform == "win32" else ""
    exe_path = src_path.replace(".cpp", exe_suffix)

    try:
        # 1. Compile the code
        compile_process = subprocess.run(
            ["g++", src_path, "-o", exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        if compile_process.returncode != 0:
            # --- Added truncation here ---
            stderr = compile_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
            # -----------------------------
            return f"--- COMPILATION FAILED ---\n{stderr}"

        # 2. Execute the compiled program
        run_process = subprocess.run(
            [exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        # --- Added truncation here ---
        stdout = run_process.stdout
        stderr = run_process.stderr
        if len(stdout) > MAX_OUTPUT_LENGTH:
            stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
        if len(stderr) > MAX_OUTPUT_LENGTH:
            stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
        # -----------------------------

        output = []
        if stdout:
            output.append(f"--- STDOUT ---\n{stdout}")
        if stderr:
            output.append(f"--- STDERR ---\n{stderr}")

        return_code = run_process.returncode
        if return_code != 0:
             output.append(f"--- EXIT CODE: {return_code} ---")

        if not output:
            return "Code compiled and executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: C++ execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: g++ command not found. Please ensure g++ is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        # 3. Clean up the temporary files
        if os.path.exists(src_path):
            os.remove(src_path)
        if os.path.exists(exe_path):
            os.remove(exe_path)


# --- Java Execution Tool ---
@tool
def execute_java_code(code: str) -> str:
    """
    Compiles and executes a string of Java code and returns the output.
    Requires javac and java to be installed and in the system's PATH.
    The code must contain a public class with a main method.
    """
    match = re.search(r'public\s+class\s+(\w+)', code)
    if not match:
        return "Error: No public class found in the Java code. A public class is required."
    
    class_name = match.group(1)
    src_path = f"{class_name}.java"
    
    with open(src_path, "w") as src_file:
        src_file.write(code)

    try:
        # 1. Compile the code
        compile_process = subprocess.run(
            ["javac", src_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        if compile_process.returncode != 0:
            # --- Added truncation here ---
            stderr = compile_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
            # -----------------------------
            return f"--- COMPILATION FAILED ---\n{stderr}"

        # 2. Execute the compiled program
        run_process = subprocess.run(
            ["java", class_name],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        # --- Added truncation here ---
        stdout = run_process.stdout
        stderr = run_process.stderr
        if len(stdout) > MAX_OUTPUT_LENGTH:
            stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
        if len(stderr) > MAX_OUTPUT_LENGTH:
            stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
        # -----------------------------

        output = []
        if stdout:
            output.append(f"--- STDOUT ---\n{stdout}")
        if stderr:
            output.append(f"--- STDERR ---\n{stderr}")

        return_code = run_process.returncode
        if return_code != 0:
             output.append(f"--- EXIT CODE: {return_code} ---")

        if not output:
            return "Code compiled and executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: Java execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: javac or java command not found. Please ensure the JDK is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        # 3. Clean up the temporary files
        if os.path.exists(src_path):
            os.remove(src_path)
        class_file = f"{class_name}.class"
        if os.path.exists(class_file):
            os.remove(class_file)

        # --- Javascript Execution Tool ---    
@tool
def execute_javascript_code(code: str) -> str:
    """
    Executes a string of JavaScript code using Node.js in an isolated subprocess.
    Requires node to be installed and in the system's PATH.
    """
    TIMEOUT = 15
    MAX_OUTPUT_LENGTH = 5000
    
    import tempfile
    import subprocess
    import sys
    import os

    with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name

    try:
        run_process = subprocess.run(
            ["node", src_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        stdout = run_process.stdout
        stderr = run_process.stderr
        
        if len(stdout) > MAX_OUTPUT_LENGTH:
            stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
        if len(stderr) > MAX_OUTPUT_LENGTH:
            stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
        
        output = []
        if stdout:
            output.append(f"--- STDOUT ---\n{stdout}")
        if stderr:
            output.append(f"--- STDERR ---\n{stderr}")

        return_code = run_process.returncode
        if return_code != 0:
            output.append(f"--- EXIT CODE: {return_code} ---")
        
        if not output:
            return "Code executed successfully with no output."

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: JavaScript execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: node command not found. Please ensure Node.js is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        if os.path.exists(src_path):
            os.remove(src_path)
