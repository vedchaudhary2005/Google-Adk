import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# --- 1. CODE WRITER AGENT ---
writer_agent = LlmAgent(
    name="writer_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="Writes code based on requests.",
    instruction="You are a skilled programmer. Write clean and efficient Python code based on the user's request."
)

# --- 2. CODE REVIEWER AGENT ---
reviewer_agent = LlmAgent(
    name="reviewer_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="Reviews code for bugs or formatting issues.",
    instruction="Review the code written by the writer agent. If it looks correct and meets the requirements, approve it."
)

# --- 3. LOOP AGENT ---
# Yeh loop writer aur reviewer ke beech mein iterations chalayega (max 3 baar)
refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[writer_agent, reviewer_agent],
    max_iterations=3 
)

# --- 4. ROOT AGENT ---
root_agent = LlmAgent(
    name="root_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description="Coordinator managing the loop.",
    instruction="Delegate the user's coding task to the `refinement_loop` for writing and reviewing.",
    sub_agents=[refinement_loop]
)