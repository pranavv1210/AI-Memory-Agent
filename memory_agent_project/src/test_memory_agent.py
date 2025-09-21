import os
from dotenv import load_dotenv
from memory_tool import get_tools, clear_user_memories
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage

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

    # --- Define Agent Prompt ---
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant with the ability to remember user preferences and facts.
         You have access to two tools: `save_user_memory` and `retrieve_user_memories`.

         **When to use `save_user_memory`:**
         - When the user tells you their name, favorite color, or any other personal preference.
         - When the user gives you a piece of information to remember.

         **When to use `retrieve_user_memories`:**
         - When the user asks a question about their preferences (e.g., \"what is my favorite color?\").
         - When the user asks a question that requires you to recall something they told you before.

         **Example Conversation:**

         User: Hi, my name is Bob.
         AI: (Calls `save_user_memory` with content=\"User's name is Bob\") Got it. I'll remember your name is Bob.

         User: What is my name?
         AI: (Calls `retrieve_user_memories` with query=\"user's name\") Your name is Bob.

         Always address the user by name if you know it from memory.
         Provide concise and helpful responses.
         """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # --- Create the Agent ---
    agent = create_openai_functions_agent(llm, tools, prompt)

    # --- Create Agent Executor ---
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


    chat_history = [] # Stores the ongoing conversation for the agent's context

    # Scenario 1: Agent learns and saves a memory
    print("\n--- Scenario 1: Agent learns and saves a memory ---")
    user_input_1 = "Hi, my name is Alice and my favorite color is blue."
    print(f"\nUser: {user_input_1}")
    response_1 = agent_executor.invoke({"input": user_input_1, "chat_history": chat_history})
    print(f"AI: {response_1['output']}")
    chat_history.extend([HumanMessage(content=user_input_1), AIMessage(content=response_1['output'])])

    # Scenario 2: Agent recalls a memory (after some turns or a new session)
    print("\n--- Scenario 2: Agent recalls a memory ---")
    chat_history_new_session = [] # Simulate starting fresh
    user_input_2 = "What is my favorite color?"
    print(f"\nUser: {user_input_2}")
    response_2 = agent_executor.invoke({"input": user_input_2, "chat_history": chat_history_new_session})
    print(f"AI: {response_2['output']}")
    chat_history_new_session.extend([HumanMessage(content=user_input_2), AIMessage(content=response_2['output'])])

    # Scenario 3: Agent uses memory in a follow-up
    print("\n--- Scenario 3: Agent uses memory in a follow-up ---")
    user_input_3 = "And what was my name again?"
    print(f"\nUser: {user_input_3}")
    response_3 = agent_executor.invoke({"input": user_input_3, "chat_history": chat_history_new_session})
    print(f"AI: {response_3['output']}")
    chat_history_new_session.extend([HumanMessage(content=user_input_3), AIMessage(content=response_3['output'])])

    print("\n--- Agent Memory Test Complete ---")
    print("\nCheck the console output for 'tool_code' blocks to see when memory tools were used.")
    print("You can also inspect the './chroma_db_data' directory for persisted memory data.")


if __name__ == "__main__":
    run_agent_test()