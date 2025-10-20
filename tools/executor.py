
import subprocess
import sys
import os
import tempfile
import re
from langchain.tools import tool

TIMEOUT = 15  # Increased timeout for compiled languages
MAX_OUTPUT_LENGTH = 5000

# --- Existing Python Tool (No changes needed) ---
@tool
def execute_python_code(code: str) -> str:
    """
    Executes a string of Python code in an isolated subprocess and returns the output.
    This tool is sandboxed and has a timeout.
    """
    # ... (Your existing execute_python_code function remains here)
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
        
        # ... (Rest of the function is the same as you have it)
        if len(stdout) > MAX_OUTPUT_LENGTH:
            stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
        if len(stderr) > MAX_OUTPUT_LENGTH:
            stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"

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

# --- NEW: C++ Execution Tool ---
@tool
def execute_cpp_code(code: str) -> str:
    """
    Compiles and executes a string of C++ code and returns the output.
    Requires g++ to be installed and in the system's PATH.
    """
    with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name
    
    # On Windows, the executable needs a .exe suffix
    exe_suffix = ".exe" if sys.platform == "win32" else ""
    exe_path = src_path.replace(".cpp", exe_suffix)

    try:
        # 1. Compile the code
        compile_process = subprocess.run(
            ["g++", src_path, "-o", exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        if compile_process.returncode != 0:
            return f"--- COMPILATION FAILED ---\n{compile_process.stderr}"

        # 2. Execute the compiled program
        run_process = subprocess.run(
            [exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            output.append(f"--- STDOUT ---\n{run_process.stdout}")
        if run_process.stderr:
            output.append(f"--- STDERR ---\n{run_process.stderr}")

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

# --- NEW: Java Execution Tool ---
@tool
def execute_java_code(code: str) -> str:
    """
    Compiles and executes a string of Java code and returns the output.
    Requires javac and java to be installed and in the system's PATH.
    The code must contain a public class with a main method.
    """
    # Find the public class name to name the file correctly
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
            return f"--- COMPILATION FAILED ---\n{compile_process.stderr}"

        # 2. Execute the compiled program
        run_process = subprocess.run(
            ["java", class_name],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            output.append(f"--- STDOUT ---\n{run_process.stdout}")
        if run_process.stderr:
            output.append(f"--- STDERR ---\n{run_process.stderr}")

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

# --- NEW: JavaScript/Node.js Execution Tool ---
@tool
def execute_javascript_code(code: str) -> str:
    """
    Executes a string of JavaScript code using Node.js and returns the output.
    Requires Node.js to be installed and in the system's PATH.
    """
    with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name

    try:
        # Execute the JavaScript code with Node.js
        run_process = subprocess.run(
            ["node", src_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            stdout = run_process.stdout
            if len(stdout) > MAX_OUTPUT_LENGTH:
                stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
            output.append(f"--- STDOUT ---\n{stdout}")
        
        if run_process.stderr:
            stderr = run_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
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
        # Clean up the temporary file
        if os.path.exists(src_path):
            os.remove(src_path)

# --- NEW: Rust Execution Tool ---
@tool
def execute_rust_code(code: str) -> str:
    """
    Compiles and executes a string of Rust code and returns the output.
    Requires rustc (Rust compiler) to be installed and in the system's PATH.
    """
    with tempfile.NamedTemporaryFile(suffix=".rs", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name
    
    # On Windows, the executable needs a .exe suffix
    exe_suffix = ".exe" if sys.platform == "win32" else ""
    exe_path = src_path.replace(".rs", exe_suffix)

    try:
        # 1. Compile the code
        compile_process = subprocess.run(
            ["rustc", src_path, "-o", exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        if compile_process.returncode != 0:
            return f"--- COMPILATION FAILED ---\n{compile_process.stderr}"

        # 2. Execute the compiled program
        run_process = subprocess.run(
            [exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            stdout = run_process.stdout
            if len(stdout) > MAX_OUTPUT_LENGTH:
                stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
            output.append(f"--- STDOUT ---\n{stdout}")
        
        if run_process.stderr:
            stderr = run_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
            output.append(f"--- STDERR ---\n{stderr}")

        return_code = run_process.returncode
        if return_code != 0:
            output.append(f"--- EXIT CODE: {return_code} ---")

        if not output:
            return "Code compiled and executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: Rust execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: rustc command not found. Please ensure Rust is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        # 3. Clean up the temporary files
        if os.path.exists(src_path):
            os.remove(src_path)
        if os.path.exists(exe_path):
            os.remove(exe_path)

# --- NEW: Ruby Execution Tool ---
@tool
def execute_ruby_code(code: str) -> str:
    """
    Executes a string of Ruby code and returns the output.
    Requires Ruby interpreter to be installed and in the system's PATH.
    """
    with tempfile.NamedTemporaryFile(suffix=".rb", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name

    try:
        # Execute the Ruby code
        run_process = subprocess.run(
            ["ruby", src_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            stdout = run_process.stdout
            if len(stdout) > MAX_OUTPUT_LENGTH:
                stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
            output.append(f"--- STDOUT ---\n{stdout}")
        
        if run_process.stderr:
            stderr = run_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
            output.append(f"--- STDERR ---\n{stderr}")

        return_code = run_process.returncode
        if return_code != 0:
            output.append(f"--- EXIT CODE: {return_code} ---")

        if not output:
            return "Code executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: Ruby execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: ruby command not found. Please ensure Ruby is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        # Clean up the temporary file
        if os.path.exists(src_path):
            os.remove(src_path)

# --- NEW: PHP Execution Tool ---
@tool
def execute_php_code(code: str) -> str:
    """
    Executes a string of PHP code and returns the output.
    Requires PHP interpreter to be installed and in the system's PATH.
    """
    with tempfile.NamedTemporaryFile(suffix=".php", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name

    try:
        # Execute the PHP code
        run_process = subprocess.run(
            ["php", src_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            stdout = run_process.stdout
            if len(stdout) > MAX_OUTPUT_LENGTH:
                stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
            output.append(f"--- STDOUT ---\n{stdout}")
        
        if run_process.stderr:
            stderr = run_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
            output.append(f"--- STDERR ---\n{stderr}")

        return_code = run_process.returncode
        if return_code != 0:
            output.append(f"--- EXIT CODE: {return_code} ---")

        if not output:
            return "Code executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: PHP execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: php command not found. Please ensure PHP is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        # Clean up the temporary file
        if os.path.exists(src_path):
            os.remove(src_path)


@tool
def execute_c_code(code: str) -> str:
    """
    Execute C code by compiling it with gcc and running the resulting executable.
    This tool is specifically for C programming language (not C++).
    
    Args:
        code: A string containing valid C source code
    
    Returns:
        A string containing the output (stdout/stderr) of the code execution,
        or compilation error messages if the code fails to compile.
    """
    # Create a temporary C file
    with tempfile.NamedTemporaryFile(suffix=".c", delete=False, mode='w') as src_file:
        src_file.write(code)
        src_path = src_file.name
    
    # Determine executable path
    exe_path = src_path.replace('.c', '.exe' if os.name == 'nt' else '')
    
    try:
        # 1. Compile the C code using gcc
        compile_process = subprocess.run(
            ['gcc', src_path, '-o', exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        if compile_process.returncode != 0:
            return f"--- COMPILATION FAILED ---\n{compile_process.stderr}"

        # 2. Execute the compiled program
        run_process = subprocess.run(
            [exe_path],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            stdout = run_process.stdout
            if len(stdout) > MAX_OUTPUT_LENGTH:
                stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
            output.append(f"--- STDOUT ---\n{stdout}")
        
        if run_process.stderr:
            stderr = run_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
            output.append(f"--- STDERR ---\n{stderr}")
        
        if run_process.returncode != 0:
            output.append(f"--- EXIT CODE ---\n{run_process.returncode}")
        
        if not output:
            return "Code executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: C compilation or execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: gcc command not found. Please ensure GCC (GNU Compiler Collection) is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        # Clean up temporary files
        if os.path.exists(src_path):
            os.remove(src_path)
        if os.path.exists(exe_path):
            os.remove(exe_path)


@tool
def execute_csharp_code(code: str) -> str:
    """
    Execute C# code by compiling it with dotnet and running the resulting executable.
    This tool is specifically for C# programming language.
    
    Args:
        code: A string containing valid C# source code
    
    Returns:
        A string containing the output (stdout/stderr) of the code execution,
        or compilation error messages if the code fails to compile.
    """
    # Create a temporary directory for the C# project
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp(prefix="csharp_exec_")
    src_path = os.path.join(temp_dir, "Program.cs")
    
    try:
        # Write the C# code to Program.cs
        with open(src_path, 'w') as src_file:
            src_file.write(code)
        
        # Create a minimal .csproj file
        csproj_content = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>disable</Nullable>
  </PropertyGroup>
</Project>"""
        
        csproj_path = os.path.join(temp_dir, "temp.csproj")
        with open(csproj_path, 'w') as csproj_file:
            csproj_file.write(csproj_content)
        
        # 1. Build the C# project using dotnet
        compile_process = subprocess.run(
            ['dotnet', 'build', '--verbosity', 'quiet', '--nologo'],
            cwd=temp_dir,
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        if compile_process.returncode != 0:
            return f"--- COMPILATION FAILED ---\n{compile_process.stderr if compile_process.stderr else compile_process.stdout}"

        # 2. Run the compiled program using dotnet run
        run_process = subprocess.run(
            ['dotnet', 'run', '--no-build', '--verbosity', 'quiet'],
            cwd=temp_dir,
            capture_output=True, text=True, timeout=TIMEOUT
        )
        
        output = []
        if run_process.stdout:
            stdout = run_process.stdout
            if len(stdout) > MAX_OUTPUT_LENGTH:
                stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... (stdout truncated)"
            output.append(f"--- STDOUT ---\n{stdout}")
        
        if run_process.stderr:
            stderr = run_process.stderr
            if len(stderr) > MAX_OUTPUT_LENGTH:
                stderr = stderr[:MAX_OUTPUT_LENGTH] + "\n... (stderr truncated)"
            output.append(f"--- STDERR ---\n{stderr}")
        
        if run_process.returncode != 0:
            output.append(f"--- EXIT CODE ---\n{run_process.returncode}")
        
        if not output:
            return "Code executed successfully with no output."
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Error: C# compilation or execution timed out after {TIMEOUT} seconds."
    except FileNotFoundError:
        return "Error: dotnet command not found. Please ensure the .NET SDK is installed and in your PATH.\nDownload from: https://dotnet.microsoft.com/download"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
