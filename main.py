import os
import dotenv
import time
import logging
from agent import create_agent, UsageTracker

# Suppress verbose logging from LangChain
logging.getLogger("langchain").setLevel(logging.ERROR)
logging.getLogger("langchain.agents").setLevel(logging.ERROR)
logging.getLogger("langchain.chains").setLevel(logging.ERROR)
logging.getLogger("langchain.callbacks").setLevel(logging.ERROR)


def main():
    """
    Main entry point for the LangChain Multi-Language Code Debugger.
    """
    # Load environment variables
    dotenv.load_dotenv()

    # Check for required API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("🚨 Error: GOOGLE_API_KEY is not set in your .env file.")
        return

    # Welcome message
    print("🚀 Welcome to the LangChain Multi-Language Code Debugger 🚀")
    print("👉 Paste Python, C++, or Java code you want to debug. Type 'EOF' to finish or 'exit' to end the session.")
    print("-" * 70)

    # Initialize agent and usage tracker
    agent_executor = create_agent(model_name="gemini-2.5-flash-lite", verbose=False)
    tracker = UsageTracker()

    while True:
        try:
            # Read multi-line input
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

            # Exit if requested
            if lines and lines[0] == 'exit':
                print("🤖 Goodbye!")
                break

            code_to_debug = "\n".join(lines)
            if not code_to_debug.strip():
                continue  # Skip empty input

            # Build task prompt for agent
            task = f"""
            Please act as an expert code debugger for multiple programming languages.
            Your task is to analyze and debug the code provided below.

            Here is the code:
            
            {code_to_debug}
            

            Follow these steps:
            1.  First, *identify the programming language* of the code (Python, C++, or Java).
            2.  Based on the language, select the appropriate tool (execute_python_code, execute_cpp_code, or execute_java_code) to run the code and confirm the error.
            3.  Analyze the error and explain the root cause.
            4.  Provide the fully corrected code.
            5.  Verify your fix by running the corrected code with the appropriate tool.

            **IMPORTANT RULE**
            When you use an execution tool, the 'Action Input' must be ONLY the raw source code.
            Do NOT wrap the code in markdown backticks like python or .
            """

            print("\n🤖 Agent is analyzing the code...\n")
            start_time = time.time()
            response = agent_executor.invoke({"input": task})
            elapsed = time.time() - start_time

            # Extract output
            output_text = response.get("output", "Sorry, I encountered an issue.")

            # Estimate token usage
            input_tokens = len(task.split())
            output_tokens = len(output_text.split())
            total_tokens = input_tokens + output_tokens

            # Track usage
            req_per_min, tokens_per_min = tracker.record_usage(total_tokens)

            # Display results
            print("\n" + "=" * 70)
            print("✅ Debugging Complete. Here is the agent's final answer:")
            print("=" * 70 + "\n")
            print(output_text)
            print("\n" + "-" * 70)
            print(f"⏱️ Response time: {elapsed:.2f}s | Tokens used: {total_tokens} | "
                  f"Req/min: {req_per_min} | Tokens/min: {tokens_per_min}")

        except KeyboardInterrupt:
            print("\n🤖 Session interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n🚨 An unexpected error occurred: {e}")
            break


if __name__ == "__main__":
    main()
