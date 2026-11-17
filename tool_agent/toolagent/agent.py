
from dotenv import load_dotenv
from pathlib import Path
from google.adk.tools import google_search
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


load_dotenv()


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""

    return {
        "status": "success",
        "city": city,
        "time": "10:30 PM"
    }


root_agent = LlmAgent(
    name="root_agent",

    model=LiteLlm(
        model="gemini/gemini-2.0-flash"
    ),

    description="An assistant that provides information, searches the web, and tells current time.",

    instruction="""
     You are a helpful and intelligent AI assistant.

    You can perform the following tasks:

    1. Answer general questions using your knowledge.
    2. Search the web for current information, latest news,
       recent updates, and facts using Google Search.
    3. Tell the current time in a specified city using
       the get_current_time tool.

    TOOL USAGE RULES:

    - Use google_search whenever the user asks for latest,
      current, recent, or web-based information.
    - Use get_current_time whenever the user asks for
      the current time in a city.
    - For general questions, answer directly using your knowledge.
    - Never claim to have searched the web if you did not
      use the Google Search tool.
    - Always use tool results accurately.
    - If a tool fails, explain that clearly.
    """,

    tools=[get_current_time,
           google_search,
           ]
)
