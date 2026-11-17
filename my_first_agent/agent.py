import time
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from datetime import date

class TodoItem(BaseModel):
    task: str = Field(description="Task name")
    due_date: date = Field(description="YYYY-MM-DD format")
    priority: str = Field(description="low/medium/high")

root_agent = LlmAgent(
    name="todo_agent",
    model="gemini-2.0-flash",  # Flash model use kar raha hai toh stable wala try kar
    instruction='''Generate todo items in exact JSON format.
    Make sure the format is strictly followed.
    ''',
    output_schema=TodoItem,
    output_key="todo"
)

# Retry logic for 503 Overloaded Error
max_retries = 3
delay = 2

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt + 1}...")
        todo = root_agent.run("Create high-priority task to call client today")
        print("Success:", todo)
        break
    except Exception as e:
        if "503" in str(e) or "Service Unavailable" in str(e):
            print(f"Server busy hai (503). {delay} seconds baad dobara try kar rahe hain...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff (2s -> 4s -> 8s)
        else:
            raise e  koi aur error hoga toh seedha raise kar dega