# LangChain Code Debugger

An intelligent Python code debugger powered by LangChain and OpenAI's GPT models.

## Features

- 🔍 Automatically identifies syntax errors, logic bugs, and runtime issues
- 🛠️ Fixes code and verifies corrections through execution
- 🔒 Safe code execution in isolated subprocesses
- 📝 Detailed debugging explanations
- 🎯 Modular, extensible architecture

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd code_debugger
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

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
├── agent.py             # LangChain agent configuration
├── tools/
│   ├── __init__.py
│   └── executor.py      # Safe Python code executor
├── examples/
│   ├── __init__.py
│   └── buggy_code.py    # Sample buggy code for testing
├── requirements.txt     # Project dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Customization

### Using Different Models

Edit the `create_agent()` call in `main.py`:
```python
agent_executor = create_agent(
    model_name="gpt-3.5-turbo",  # or "gpt-4"
    temperature=0.2,              # Higher for more creative solutions
    verbose=True                  # Set to False for less output
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
- OpenAI API key
- Dependencies listed in requirements.txt

## License

MIT
