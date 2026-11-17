from google.adk.agents.llm_agent import LlmAgent
from pydantic import BaseModel, Field
from datetime import date

# 1. Pydantic schema define kiya output ke contract ke liye
class TodoItem(BaseModel):
    task: str = Field(description="Task name")
    due_date: date = Field(description="Due date in YYYY-MM-DD format")
    priority: str = Field(description="Priority of the task: low, medium, or high")

# 2. LlmAgent setup kiya schema aur instructions ke sath
root_agent = LlmAgent(
    name="todo_agent",
    model="gemini-3.8-flash",  # Stable model version for production
    instruction='''Generate todo items matching the requested schema.
    Make sure the format is strictly followed.
    Below are the fields you need to generate:
    1. task: Task name
    2. due_date: Due date in YYYY-MM-DD format
    3. priority: Priority of the task (low/medium/high)
    ''',
    output_schema=TodoItem,
    output_key="todo"
)

# 3. Agent ko run karne ka example
if __name__ == "__main__":
    try:
        # Prompt dekar agent execute kar rahe hain
        response = root_agent.run("Create high-priority task to call client today")
        print("Agent Response:", response)
        
        # Accessing nested output fields directly
        print(f"Task: {response['todo']['task']}")
        print(f"Due Date: {response['todo']['due_date']}")
        print(f"Priority: {response['todo']['priority']}")
        
    except Exception as e:
        print("Error aa gaya:", e)