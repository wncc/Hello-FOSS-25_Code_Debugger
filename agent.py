"""
Defines the LangChain agent setup for code debugging using Gemini.
"""

from typing import Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from tools.executor import PythonExecutorTool


def create_agent(
    model_name: str = "gemini-1.5-flash",
    temperature: float = 0.0,
    verbose: bool = False,
    max_iterations: Optional[int] = 10
) -> AgentExecutor:
    """
    Create a LangChain agent for debugging Python code using Gemini.
    
    Args:
        model_name: Gemini model to use 
        temperature: Model temperature for creativity (default: 0.0)
        verbose: Whether to print detailed execution logs
        max_iterations: Maximum agent iterations (default: 10)
    
    Returns:
        AgentExecutor: Configured agent ready for debugging
    """
    
    # Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        convert_system_message_to_human=True
    )
    
    # Create the Python executor tool
    executor_tool = PythonExecutorTool()
    
    # Wrap it as a LangChain Tool
    tools = [
        Tool(
            name="Python_Executor",
            func=executor_tool.run,
            description=(
                "Execute Python code safely and return the output. "
                "Input should be valid Python code as a string. "
                "Returns both stdout and stderr output. "
                "Use this to test and verify code fixes."
            )
        )
    ]
    
    # Create the ReAct prompt template
    prompt = PromptTemplate.from_template("""
You are an expert Python debugger. Your task is to identify and fix bugs in Python code.

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Use the following format:

Question: the input question or task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer with the corrected code and explanation

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")
    
    # Create the ReAct agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        max_iterations=max_iterations,
        handle_parsing_errors=True,
        return_intermediate_steps=False
    )
    
    return agent_executor

