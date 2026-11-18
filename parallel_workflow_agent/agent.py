
import os
import requests
from dotenv import load_dotenv
from tavily import TavilyClient
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# --- TOOLS ---
def get_weather(city: str) -> dict:
    """Returns the current weather for a specified city."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url).json()
        if not geo_res.get("results"):
            return {"status": "error", "message": f"City '{city}' not found."}
            
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
        temp = requests.get(weather_url).json().get("current", {}).get("temperature_2m", "N/A")
        return {"status": "success", "city": city, "temperature": f"{temp}°C"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def web_search(query: str) -> dict:
    """Searches the web for latest information using Tavily."""
    try:
        response = tavily_client.search(query=query, max_results=3)
        return {"status": "success", "results": response.get("results", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- AGENT 1: WEATHER SPECIALIST ---
weather_agent = LlmAgent(
    name="weather_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="Specialist agent that only fetches weather data.",
    instruction="Use the get_weather tool to find temperature and weather conditions.",
    tools=[get_weather]
)

# --- AGENT 2: NEWS SPECIALIST ---
news_agent = LlmAgent(
    name="news_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="Specialist agent that only searches web news.",
    instruction="Use the web_search tool to find latest news and updates.",
    tools=[web_search]
)

# --- ROOT COORDINATOR (PARALLEL EXECUTION) ---
root_agent = LlmAgent(
    name="root_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="Coordinator that delegates tasks to multiple agents in parallel.",
    instruction="""
    You manage a parallel workflow. When the user asks for multiple independent things (like weather of a city AND news of something else), 
    delegate the weather task to `weather_agent` and the news/search task to `news_agent` simultaneously.
    Combine their outputs and present them together to the user.
    """,
    sub_agents=[weather_agent, news_agent]
)