import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import streamlit as st
import os
from dotenv import load_dotenv
from memory_tool import get_tools, clear_user_memories, MemoryStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage, AIMessage

# --- Configuration and Initialization ---

# Load environment variables (GOOGLE_API_KEY)
load_dotenv()

# Get Google API Key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")
    st.stop()

# Define LLM model for Google Gemini
LLM_MODEL = "gemini-1.5-flash"

# --- Session State Management ---
if "user_id" not in st.session_state:
    st.session_state.user_id = os.urandom(16).hex()
    st.session_state.memory_store = MemoryStore(user_id=st.session_state.user_id)
    print(f"New session started with User ID: {st.session_state.user_id}")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- LangChain Setup ---
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0, google_api_key=GOOGLE_API_KEY)
tools = get_tools(user_id=st.session_state.user_id)
save_user_memory = tools[0]
retrieve_user_memories = tools[1]

prompt_template = """You are a helpful AI assistant. You have access to two tools: `save_user_memory` and `retrieve_user_memories`.
Decide which tool to use based on the user's input.
If the user is providing new information, use `save_user_memory`.
If the user is asking a question, use `retrieve_user_memories`.
If you don't know the answer, just say "I don't know".

User input: {input}
Your decision:"""
prompt = ChatPromptTemplate.from_template(prompt_template)

chain = LLMChain(llm=llm, prompt=prompt)


# --- UI Layout ---

st.set_page_config(
    page_title="AI Memory Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 AI Memory Assistant")
st.markdown("---")

# --- Sidebar for Memory Debugging ---
with st.sidebar:
    st.header("Long-Term Memories (Debug)")
    st.info(f"Current User ID: `{st.session_state.user_id}`")

    if st.button("Clear All Memories for this User"):
        if st.session_state.get('confirm_clear', False):
            clear_user_memories(st.session_state.user_id)
            st.session_state.chat_history = []
            st.session_state.confirm_clear = False
            st.experimental_rerun()
        else:
            st.session_state.confirm_clear = True
            st.warning("Are you sure? This will delete ALL memories for this user. Click again to confirm.")

    if st.session_state.get('confirm_clear', False) and not st.button("Confirm Clear"):
        pass

    st.markdown("---")
    st.subheader("Current Stored Memories:")

    current_memories = st.session_state.memory_store.get_all_memories()
    if current_memories:
        for i, mem in enumerate(current_memories):
            st.markdown(f"**{i+1}.** **Content:** `{mem['content']}`")
            st.markdown(f"   **Context:** `{mem['context']}`")
            st.markdown("---")
    else:
        st.write("No memories stored yet.")

# --- Main Chat Interface ---
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

if prompt := st.chat_input("Type your message here..."):
    st.session_state.chat_history.append(HumanMessage(content=prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                response = chain.run(input=prompt)
                ai_response_content = ""
                if "save_user_memory" in response:
                    save_user_memory.func(content=prompt, context="user preference")
                    ai_response_content = "I've saved that for you."
                elif "retrieve_user_memories" in response:
                    memories = retrieve_user_memories.func(query=prompt)
                    ai_response_content = memories
                else:
                    ai_response_content = response

                st.markdown(ai_response_content)
                st.session_state.chat_history.append(AIMessage(content=ai_response_content))
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.chat_history.append(AIMessage(content="Oops! Something went wrong. Please try again."))

    st.experimental_rerun()