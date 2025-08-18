"""
Implements a safe Python code executor tool for LangChain.
"""

import subprocess
import tempfile
import os
import sys
from typing import Dict, Any
import signal
import platform


class PythonExecutorTool:
    """
    A tool that safely executes Python code in a subprocess.
    """
    
    def __init__(self, timeout: int = 10, max_output_length: int = 10000):
        """
        Initialize the Python executor.
        
        Args:
            timeout: Maximum execution time in seconds (default: 10)
            max_output_length: Maximum output length in characters (default: 10000)
        """
        self.timeout = timeout
        self.max_output_length = max_output_length
    
    def run(self, code: str) -> str:
        """
        Execute Python code safely in a subprocess.
        
        Args:
            code: Python code to execute
            
        Returns:
            String containing execution results (stdout and stderr)
        """
        # Security check: block dangerous operations
        dangerous_patterns = [
            '__import__("os").system',
            'eval(',
            'exec(',
            'compile(',
            '__import__("subprocess")',
            'open(',
            'file(',
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                return f"Error: Potentially dangerous operation detected: {pattern}"
        
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            dir=tempfile.gettempdir()
        ) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name
        
        try:
            # Prepare the subprocess environment
            env = os.environ.copy()
            env['PYTHONDONTWRITEBYTECODE'] = '1'  # Don't create .pyc files
            
            # Run the code in a subprocess
            result = subprocess.run(
                [sys.executable, tmp_file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=env,
                # Use different signal on Windows
                **({'preexec_fn': os.setsid} if platform.system() != 'Windows' else {})
            )
            
            # Combine stdout and stderr
            output_parts = []
            
            if result.stdout:
                stdout = result.stdout[:self.max_output_length]
                if len(result.stdout) > self.max_output_length:
                    stdout += "\n... (output truncated)"
                output_parts.append(f"STDOUT:\n{stdout}")
            
            if result.stderr:
                stderr = result.stderr[:self.max_output_length]
                if len(result.stderr) > self.max_output_length:
                    stderr += "\n... (output truncated)"
                output_parts.append(f"STDERR:\n{stderr}")
            
            if result.returncode != 0:
                output_parts.append(f"Exit Code: {result.returncode}")
            
            if not output_parts:
                output_parts.append("Code executed successfully with no output.")
            
            return "\n".join(output_parts)
            
        except subprocess.TimeoutExpired:
            # Kill the process group on timeout (Unix-like systems)
            if platform.system() != 'Windows':
                try:
                    os.killpg(os.getpgid(result.pid), signal.SIGTERM)
                except:
                    pass
            return f"Error: Code execution timed out after {self.timeout} seconds"
            
        except Exception as e:
            return f"Error executing code: {str(e)}"
            
        finally:
            # Clean up the temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass
    
    def __call__(self, code: str) -> str:
        """Make the tool callable."""
        return self.run(code)

