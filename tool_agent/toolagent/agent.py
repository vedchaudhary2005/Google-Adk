from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from tavily import TavilyClient
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))



def get_weather(city: str) -> dict:
    """Returns the current weather for a specified city."""
    # Yahan tu real weather API bhi laga sakta hai, abhi ke liye mock response hai
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

def multiply_numbers(a: float, b: float) -> dict:
    """Multiplies two numbers together and returns the result."""
    result = a * b
    return {
        "status": "success",
        "operation": "multiplication",
        "result": result
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
    model="gemini-3.8-flash",
    description="An assistant that provides information, searches the web, and tells current time.",
    instruction="""
    You are a helpful and intelligent AI assistant.
    You can perform the following tasks:
    1. Answer general questions using your knowledge.
    2. Search the web for current information, latest news, recent updates using Google Search.
    3. Tell the current time in a specified city using the get_current_time tool.

    TOOL USAGE RULES:
    - Use google_search whenever the user asks for latest, current, recent, or web-based information.
    - Use get_current_time whenever the user asks for the current time in a city.
    """,

    tools=[
        get_current_time,
        google_search,
        multiply_numbers,
    ]
)