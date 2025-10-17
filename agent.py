import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

import time
from collections import deque

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

class UsageTracker:
    def __init__(self, req_limit_per_day = 50, req_limit_per_min = 15, token_limit_per_min = 250_000):
        self.req_limit_per_day = req_limit_per_day
        self.req_limit_per_min = req_limit_per_min
        self.token_limit_per_min = token_limit_per_min

        self.last_day = time.strftime("%Y-%m-%d")
        self.req_timestamps = deque()
        self.token_timestamps = deque()
        self.daily_requests = 0

    def record_usage(self, tokens_used):
        now = time.time()
        
        # Check date changes
        today = time.strftime("%Y-%m-%d")
        if today != self.last_day :
            self.daily_requests = 0
            self.last_day = today
            print("🔄Daily usage reset")

        # Record request timestamp
        self.req_timestamps.append(now)
        self.daily_requests += 1

        # Record tokens
        self.token_timestamps.append((now, tokens_used))

        # Cleanup old entries (older than 60s)
        while self.req_timestamps and now - self.req_timestamps[0] > 60:
            self.req_timestamps.popleft()

        while self.token_timestamps and now - self.token_timestamps[0][0] > 60:
            self.token_timestamps.popleft()

        # Compute current usage
        req_per_min = len(self.req_timestamps)
        tokens_per_min = sum(t for _, t in self.token_timestamps)

        # Warnings
        if req_per_min > self.req_limit_per_min * 0.8:
            print(f"⚠️ Approaching rate limit: {req_per_min}/{self.req_limit_per_min} req/min")

        if self.daily_requests > self.req_limit_per_day * 0.8:
            print(f"⚠️ Approaching daily limit: {self.daily_requests}/{self.req_limit_per_day} req/day")

        if tokens_per_min > self.token_limit_per_min * 0.8:
            print(f"⚠️ Approaching token limit: {tokens_per_min}/{self.token_limit_per_min} tokens/min")

        # Hard stops (optional)
        if req_per_min > self.req_limit_per_min:
            raise RuntimeError("🚫 API rate limit (requests/min) exceeded!")

        if self.daily_requests > self.req_limit_per_day:
            raise RuntimeError("🚫 Daily API request limit exceeded!")

        if tokens_per_min > self.token_limit_per_min:
            raise RuntimeError("🚫 Token usage limit exceeded!")

        return req_per_min, tokens_per_min
        
