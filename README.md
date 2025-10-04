#  LangChain Multi-Language Code Debugger (Powered by Gemini)

## Project Overview

This is an advanced **AI agent** built on the **LangChain framework** and powered by the **Gemini Large Language Model (LLM)**, designed for seamless integration into the developer's terminal. Its core function is to automate the process of finding and fixing errors across multiple programming languages, specifically **Python, C++, and Java**.

## How It Works

The system operates on a closed-loop "Observe-Reason-Act" agent model:

1.  **Input & Detection:** The user pastes buggy code. The agent first identifies the programming language (Python, C++, or Java).
2.  **Execution & Error Capture:** It uses a set of specialized **LangChain execution tools** (e.g., `execute_cpp_code`) to run the code in an isolated environment. This action captures the precise **stack trace** or error output.
3.  **LLM Analysis:** The captured error output and the original code are fed to the **Gemini LLM** (via the API key). Gemini analyzes the error and the code to diagnose the root cause.
4.  **Fix & Verification:** Gemini generates the **fully corrected code** and an explanation. Crucially, the agent attempts to **verify the fix** by running the corrected code again to confirm successful execution before presenting the final answer to the user.

## Motivation: Terminal-First Debugging
The core motivation is a **terminal-integrated debugger** which can provide **personalized solutions** and explanations to quickly identify code errors, acting as an on-demand tutor for **absolute beginners** (CS101). By automating the debugging loop with an LLM, it minimizes the tiring, time-consuming process for all developers. It can give **personalized results** depending on the prompt, which can significantly reduce time and effort.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AbhishekU05/Hello_FOSS_25_code_debugger.git
cd Hello_FOSS_25_code_debugger
```

2. Install dependencies:
```bash
source foss_venv/bin/activate
pip3 install -r requirements.txt
```

3. Create a .env file for your environment variables
```bash
# Google Gemini API Configuration
GOOGLE_API_KEY=your-gemini-api-key-here

# Optional: Specify model (default is gemini-pro)
# GEMINI_MODEL=gemini-pro

# Optional: Set temperature (default is 0.0)
# TEMPERATURE=0.0
```

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## Usage

Run the debugger:
```bash
python main.py
```

The debugger will:
1. Load a sample buggy code snippet
2. Identify the issues
3. Generate fixes
4. Test the corrected code
5. Display the results

## Project Structure

```
code_debugger/
│
├── main.py              # Entry point
├── agent.py             # LangChain agent configuration with Gemini
├── tools/
│   ├── __init__.py
│   └── executor.py      # Safe Python code executor
├── examples/
│   ├── __init__.py
│   └── buggy_code.py    # Sample buggy code for testing
├── requirements.txt     # Project dependencies (updated for Gemini)
├── .env         # Environment variables template
└── README.md           # This file
```

## Customization

### Using Different Gemini Models

Edit the `create_agent()` call in `main.py`:
```python
agent_executor = create_agent(
    model_name="gemini-pro",         # Available models: gemini-pro, gemini-pro-vision
    temperature=0.2,                 # Higher for more creative solutions
    verbose=True                     # Set to False for less output
)
```

### Adding New Buggy Code Samples

Add new examples to `examples/buggy_code.py`:
```python
BUGGY_CODE_SAMPLES["my_bug"] = '''
def my_function():
    # Your buggy code here
    pass
'''
```

## Security

- Code execution happens in isolated subprocesses
- Dangerous operations are blocked (eval, exec, file operations)
- Execution timeout prevents infinite loops
- Output length is limited to prevent memory issues

## Requirements

- Python 3.8+
- Google Gemini API key
- Dependencies listed in requirements.txt

## License

MIT
