from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from tavily import TavilyClient
from google.adk.tools import load_memory
import os
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))






def get_weather(city: str) -> dict:
    """Returns the current weather for a specified city."""
   
    return {
        "status": "success",
        "city": city,
        "temperature": "28°C",
        "condition": "Sunny / Clear"
    }

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": "10:30 PM"
    }

def web_search(query: str) -> dict:
    """Searches the web for latest information, recent updates, and facts using Tavily."""
    try:
        response = tavily_client.search(query=query, max_results=3)
        return {
            "status": "success",
            "results": response.get("results", [])
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


root_agent = LlmAgent(
    name="root_agent",
    model=LiteLlm(
        model="groq/openai/gpt-oss-20b" 
    ),

    description="An assistant that provides weather, time, does math, and searches the web using Tavily.",

    instruction="""
    You are a helpful and intelligent AI assistant powered by Groq.
    You have access to multiple tools:
    1. web_search: Use whenever the user asks for latest, current, recent, or web-based information.
    2. get_current_time: Use whenever the user asks for the current time in a city.
    3. get_weather: Use whenever the user asks about the weather or temperature in a city.
    4. multiply_numbers: Use when multiplication is requested.
    5. load_memory: Retrieve relevant information from previous conversations.
    Always select the appropriate tool based on user queries.
    """,

    tools=[
        get_current_time,
        get_weather,
        multiply_numbers,
        web_search,
        load_memory,
    ]
)