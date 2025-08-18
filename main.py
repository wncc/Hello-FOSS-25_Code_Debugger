# code_debugger/main.py
"""
Entry point for the LangChain-based code debugger.
Demonstrates fixing and running buggy Python code using an AI agent.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agent import create_agent
from examples.buggy_code import BUGGY_CODE_SAMPLES

# Load environment variables
load_dotenv()


def main():
    """Main function to run the code debugger."""
    
    # Verify OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it using: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    print("🔧 LangChain Code Debugger")
    print("=" * 50)
    
    # Create the debugging agent
    print("\n📦 Initializing agent...")
    agent_executor = create_agent(verbose=True)
    
    # Select a buggy code sample to debug
    buggy_code = BUGGY_CODE_SAMPLES["syntax_error"]
    
    print("\n🐛 Original buggy code:")
    print("-" * 30)
    print(buggy_code)
    print("-" * 30)
    
    # Create the debugging prompt
    prompt = f"""
    I have the following Python code that contains bugs:
    
    ```python
    {buggy_code}
    ```
    
    Please:
    1. Identify what's wrong with this code
    2. Fix the bugs
    3. Test the fixed code by running it with sample inputs
    4. Verify the output is correct
    
    Use the Python Executor tool to test your fixes.
    """
    
    print("\n🤖 Agent is debugging the code...")
    print("=" * 50)
    
    try:
        # Run the agent
        result = agent_executor.invoke({"input": prompt})
        
        print("\n✅ Debugging complete!")
        print("=" * 50)
        print("\n📝 Final Result:")
        print(result["output"])
        
    except Exception as e:
        print(f"\n❌ Error during debugging: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


