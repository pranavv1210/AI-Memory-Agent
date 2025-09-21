import os
from dotenv import load_dotenv
from memory_tool import get_tools, clear_user_memories
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Load environment variables (GOOGLE_API_KEY)
load_dotenv()

# --- Configuration ---
USER_ID = "test_user_001" # A fixed user ID for testing purposes
# Recommended model for Google Gemini for development and free tier:
LLM_MODEL = "gemini-1.5-flash"

# Get Google API Key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")


# --- Initialize LLM ---
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0, google_api_key=GOOGLE_API_KEY)


# --- Test Function ---
def run_agent_test():
    print(f"--- Running Agent Memory Test for User: {USER_ID} ---")
    print(f"--- Using LLM: {LLM_MODEL} ---")

    # 1. Clear previous memories for this user to ensure a clean test run
    print("\n--- Clearing existing memories ---")
    clear_user_memories(USER_ID)
    print("--- Memories cleared ---")

    # Define the tools available to the agent.
    tools = get_tools(user_id=USER_ID)
    save_user_memory = tools[0]
    retrieve_user_memories = tools[1]

    # --- Define Agent Prompt ---
    prompt_template = """You are a helpful AI assistant. You have access to two tools: `save_user_memory` and `retrieve_user_memories`.
    Decide which tool to use based on the user's input.
    If the user is providing new information, use `save_user_memory`.
    If the user is asking a question, use `retrieve_user_memories`.
    If you don't know the answer, just say "I don't know".

    User input: {input}
    Your decision:"""
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # --- Create the LLMChain ---
    chain = LLMChain(llm=llm, prompt=prompt)


    # Scenario 1: Agent learns and saves a memory
    print("\n--- Scenario 1: Agent learns and saves a memory ---")
    user_input_1 = "Hi, my name is Alice and my favorite color is blue."
    print(f"\nUser: {user_input_1}")
    response_1 = chain.run(input=user_input_1)
    print(f"LLM output: {response_1}")
    if "save_user_memory" in response_1:
        save_user_memory.func(content="Alice's favorite color is blue.", context="user preference")
        print("Memory saved.")
    else:
        print("Memory not saved.")


    # Scenario 2: Agent recalls a memory (after some turns or a new session)
    print("\n--- Scenario 2: Agent recalls a memory ---")
    user_input_2 = "What is my favorite color?"
    print(f"\nUser: {user_input_2}")
    response_2 = chain.run(input=user_input_2)
    print(f"LLM output: {response_2}")
    if "retrieve_user_memories" in response_2:
        memories = retrieve_user_memories.func(query="favorite color")
        print(f"Retrieved memories: {memories}")
    else:
        print("Memories not retrieved.")


    # Scenario 3: Agent uses memory in a follow-up
    print("\n--- Scenario 3: Agent uses memory in a follow-up ---")
    user_input_3 = "And what was my name again?"
    print(f"\nUser: {user_input_3}")
    response_3 = chain.run(input=user_input_3)
    print(f"LLM output: {response_3}")
    if "retrieve_user_memories" in response_3:
        memories = retrieve_user_memories.func(query="name")
        print(f"Retrieved memories: {memories}")
    else:
        print("Memories not retrieved.")


if __name__ == "__main__":
    run_agent_test()