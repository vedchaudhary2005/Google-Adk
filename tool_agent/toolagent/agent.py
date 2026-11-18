from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent
from tavily import TavilyClient
from google.adk.tools import load_memory
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import requests
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))






def get_weather(city: str) -> dict:
    """Returns the current weather and temperature for any specified city in the world."""
    try:
       
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url).json()
        
        if not geo_res.get("results"):
            return {"status": "error", "message": f"City '{city}' not found."}
            
        location = geo_res["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        country = location.get("country", "")
        
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
        weather_res = requests.get(weather_url).json()
        
        current = weather_res.get("current", {})
        temp = current.get("temperature_2m", "N/A")
        
        return {
            "status": "success",
            "city": city,
            "country": country,
            "temperature": f"{temp}°C",
            "condition": "Clear / Live Data"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_current_time(city: str) -> dict:
    """Returns the exact current local time in any specified city using timezone lookup and Python datetime."""
    try:
       
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url).json()
        
        if not geo_res.get("results"):
            return {"status": "error", "message": f"City '{city}' not found."}
            
        location = geo_res["results"][0]
        timezone_str = location.get("timezone", "UTC")
        country = location.get("country", "")
        
        
        current_time = datetime.now(ZoneInfo(timezone_str)).strftime("%I:%M %p") 
        current_date = datetime.now(ZoneInfo(timezone_str)).strftime("%Y-%m-%d")
        
        return {
            "status": "success",
            "city": city,
            "country": country,
            "timezone": timezone_str,
            "date": current_date,
            "time": current_time
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

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
        web_search,
        load_memory,
    ]
)