import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# --- CRITICAL TOOL WITH HUMAN APPROVAL ---
def delete_production_database(database_name: str, tool_context: ToolContext) -> dict:
    """Deletes a production database. Requires human approval before executing."""
    
    print(f"\n⚠️ [SECURITY ALERT] Agent wants to delete database: '{database_name}'")
    
    # Human-in-the-loop prompt 
    approval = input("Do you want to approve this action? (yes/no): ").strip().lower()
    
    if approval == "yes":
       
        return {
            "status": "success", 
            "message": f"Database '{database_name}' has been successfully deleted by human consent."
        }
    else:
        
        return {
            "status": "rejected", 
            "message": "Action cancelled by human supervisor."
        }

# --- AGENT SETUP ---
admin_agent = LlmAgent(
    name="admin_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="An administrative agent that manages infrastructure and databases.",
    instruction="You are a system admin assistant. If the user asks to delete a database, use the `delete_production_database` tool.",
    tools=[delete_production_database]
)