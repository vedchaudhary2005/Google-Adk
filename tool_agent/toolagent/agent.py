
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
        model="groq/openai/gpt-oss-20b"
    ),

    description="An assistant that provides information, searches the web, and tells current time.",

    instruction="""
    You are a helpful assistant.

    Whenever the user asks for the current time in a city,
    call the get_current_time tool.

    Use the tool result to answer the user.
    """,

    tools=[get_current_time,
           google_search,
           ]
)
