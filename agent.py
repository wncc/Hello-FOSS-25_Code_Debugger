import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

# Import all three execution tools
from tools.executor import execute_python_code, execute_cpp_code, execute_java_code

def create_agent(model_name: str = "gemini-1.5-flash-latest", temperature: float = 0.0, verbose: bool = True):
    """
    Creates and returns a LangChain agent executor for debugging code.
    """
    llm = ChatGoogleGenerativeAI( 
        model=model_name,
        temperature=temperature,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # The agent now has a tool for each language
    tools = [execute_python_code, execute_cpp_code, execute_java_code]

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose, 
        handle_parsing_errors=True,
        max_iterations=10
    )
    return agent_executor 