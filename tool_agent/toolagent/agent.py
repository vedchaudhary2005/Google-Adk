import os
import requests
from dotenv import load_dotenv
from tavily import TavilyClient
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# --- 1. TOOLS DEFINITION ---
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
        temp = weather_res.get("current", {}).get("temperature_2m", "N/A")
        
        return {
            "status": "success",
            "city": city,
            "country": country,
            "temperature": f"{temp}°C"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def web_search(query: str) -> dict:
    """Searches the web for latest information using Tavily."""
    try:
        response = tavily_client.search(query=query, max_results=3)
        return {"status": "success", "results": response.get("results", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- 2. AGENT 1: RESEARCH AGENT (Data collect karega) ---
research_agent = LlmAgent(
    name="research_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="An agent responsible for fetching raw weather data and web information.",
    instruction="You are a research specialist. Use get_weather or web_search tools to gather precise data requested by the user. Do not format heavily, just fetch the facts.",
    tools=[get_weather, web_search]
)


# --- 3. AGENT 2: WRITER / FORMATTING AGENT (Data ko polish karega) ---
writer_agent = LlmAgent(
    name="writer_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="An agent responsible for writing a polished, friendly response based on research data.",
    instruction="You are a professional content writer. Take the raw data provided by the research agent and present it in a clean, engaging, and structured format in Hinglish.",
    tools=[] 
)



root_agent = LlmAgent(
    name="root_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="Coordinator agent that manages the sequential research and writing pipeline.",
    instruction="""
    You manage a sequential workflow:
    1. First, delegate the user's query to the `research_agent` to gather accurate data/facts.
    2. Then, pass that raw data to the `writer_agent` to structure and format it nicely for the user.
    """,
    sub_agents=[research_agent, writer_agent]
)



