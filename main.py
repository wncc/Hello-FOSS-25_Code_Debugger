import os 
import dotenv 
from agent import create_agent, UsageTracker
import time
 
def main():
    """
    Main entry point for the Code Debugger.
    """
    dotenv.load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"): 
        print("🚨 Error: GOOGLE_API_KEY is not set in your .env file.")
        return

    print("🚀 Welcome to the LangChain Multi-Language Code Debugger 🚀")
    print("👉 Paste Python, C, C++, Java, JavaScript, Rust, Ruby, PHP, or C# code you want to debug.")
    print("   When you're done, type 'EOF' on a new line. Type 'exit' to end the session.")
    print("-" * 70)

    agent_executor = create_agent(model_name="gemini-2.5-flash-lite", verbose=True)
    tracker = UsageTracker()

    while True:
        try:
            print("\nPlease paste your code now (type 'EOF' on a new line to finish):")
            
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'EOF':
                    break
                if line.strip().lower() == 'exit':
                    lines = ['exit']
                    break
                lines.append(line)
            
            if lines and lines[0] == 'exit':
                print("🤖 Goodbye!")
                break

            code_to_debug = "\n".join(lines)

            if not code_to_debug.strip():
                continue

            # --- THIS IS THE UPDATED PROMPT ---
            task = f"""
            Please act as an expert code debugger for multiple programming languages.
            Your task is to analyze and debug the code provided below.

            Here is the code:
            
            {code_to_debug}
            

            Follow these steps:
            1.  First, *identify the programming language* of the code (Python, C, C++, Java, JavaScript, Rust, Ruby, PHP, or C#).
            2.  Based on the language, select the appropriate tool:
                - execute_python_code for Python
                - execute_c_code for C
                - execute_cpp_code for C++
                - execute_java_code for Java
                - execute_javascript_code for JavaScript/Node.js
                - execute_rust_code for Rust
                - execute_ruby_code for Ruby
                - execute_php_code for PHP
                - execute_csharp_code for C#
            3.  Run the code with the selected tool to confirm the error.
            4.  Analyze the error and explain the root cause.
            5.  Provide the fully corrected code.
            6.  Verify your fix by running the corrected code with the appropriate tool.

            **IMPORTANT RULE**
            When you use an execution tool, the 'Action Input' must be ONLY the raw source code.
            Do NOT wrap the code in markdown backticks like python or .
            """

            print("\n🤖 Agent is analyzing the code...\n")
            
            start = time.time()
            response = agent_executor.invoke({"input": task})
            end = time.time()
            elapsed = end - start

            print("\n" + "="*70)
            print("✅ Debugging Complete. Here is the agent's final answer:")
            print("="*70 + "\n")
            print(f"{response.get('output', 'Sorry, I encountered an issue.')}")
            print("\n" + "-"*70)
            
            input_tokens = len(task.split())
            output_text = response.get("output", "")
            output_tokens = len(output_text.split())
            total_tokens = input_tokens + output_tokens

            req_per_min, tokens_per_min = tracker.record_usage(total_tokens)

            print("\n" + "="*70)
            print("✅ Debugging Complete. Here is the agent's final answer:")
            print("="*70 + "\n")
            print(output_text)
            print("\n" + "-"*70)
            print(f"⏱️ Response time: {elapsed:.2f}s | Tokens used: {total_tokens} | Req/min: {req_per_min} | Tokens/min: {tokens_per_min}")
            

        except KeyboardInterrupt:
            print("\n🤖 Session interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n🚨 An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()