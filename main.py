from pydantic_ai import Agent
from pydantic_ai_utils.tools import google_search_tool

next_agent = Agent("anthropic:claude-3-5-sonnet-latest", tools=[google_search_tool()])


@next_agent.system_prompt
async def system_prompt():
    return "You are a helpful assistant that orchestrates other AI agents to complete tasks."


result = next_agent.run_sync(
    "Get me the latest news about Utrecht. Always give the source url."
)
print(result.data)
