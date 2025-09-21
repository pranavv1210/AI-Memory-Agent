

# AI Memory Agent

**Author:** [pranavv1210](https://github.com/pranavv1210)  


---

## Overview

AI Memory Agent is a conversational AI system with long-term, semantic memory. It uses LangChain, ChromaDB, and Google Gemini (or OpenAI) to remember facts, preferences, and context from user interactions, enabling personalized and coherent conversations over time. The project features a Streamlit web interface for chat and memory visualization.

---

## Features

- **Conversational Agent:** Interacts with users via text chat.
- **Semantic Memory:** Stores and retrieves information based on meaning, not just keywords.
- **User-Scoped Memory:** Each user's memories are isolated by a unique user ID.
- **Memory Visualization:** Sidebar panel shows all stored memories for the current user.
- **Memory Clearing:** Easily reset all memories for a user via the UI.
- **Extensible:** Ready for voice input (Whisper), advanced prompts, and more.

---

## Tech Stack

- **Backend:** Python
- **AI Framework:** LangChain
- **LLM:** Google Gemini (default, free tier) or OpenAI GPT (optional)
- **Vector Database:** ChromaDB
- **Frontend:** Streamlit
- **Environment:** `.env` for API keys

---

## Project Structure

```
memory_agent_project/
├── src/
│   ├── memory_tool.py         # Memory management logic and LangChain tools
│   ├── test_memory_agent.py   # Script to test agent memory functions
│   └── streamlit_app.py       # Streamlit web app
├── docs/
│   ├── ui_design.md           # UI design documentation
│   ├── Evaluation_Plan.md     # Evaluation scenarios and metrics
│   ├── prompts.md             # Agent prompt documentation
│   └── Voice_Integration.md   # Guide for adding voice input
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
└── README.md                  # Project overview and instructions
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/pranavv1210/AI-Memory-Agent.git
cd AI-Memory-Agent/memory_agent_project
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
```
git init
### 3. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```
**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

<<<<<<< HEAD

# AI Memory Agent

**Author:** [pranavv1210](https://github.com/pranavv1210)  
**Contact:** pranavv36@gmail.com

---

## Overview

AI Memory Agent is a conversational AI system with long-term, semantic memory. It uses LangChain, ChromaDB, and Google Gemini (or OpenAI) to remember facts, preferences, and context from user interactions, enabling personalized and coherent conversations over time. The project features a Streamlit web interface for chat and memory visualization.

---

## Features

- **Conversational Agent:** Interacts with users via text chat.
- **Semantic Memory:** Stores and retrieves information based on meaning, not just keywords.
- **User-Scoped Memory:** Each user's memories are isolated by a unique user ID.
- **Memory Visualization:** Sidebar panel shows all stored memories for the current user.
- **Memory Clearing:** Easily reset all memories for a user via the UI.
- **Extensible:** Ready for voice input (Whisper), advanced prompts, and more.

---

## Architecture & Flow

### High-Level Design

1. **User interacts via Streamlit chat UI.**
2. **Agent receives input, parses for important facts or questions.**
3. **If new info is detected:**
  - Agent uses LangChain tool to save memory (stores semantic embedding + metadata in ChromaDB).
4. **If recall is needed:**
  - Agent uses LangChain tool to retrieve relevant memories (semantic search in ChromaDB).
5. **Agent responds, optionally using retrieved memories for context.**
6. **Sidebar updates in real time to show all stored memories for the user.**

### Memory Mechanism Explained

- **Semantic Embeddings:** Text is converted to high-dimensional vectors using Gemini or OpenAI, capturing meaning beyond keywords.
- **ChromaDB Vector Store:** Stores embeddings and metadata, allowing fast semantic search and retrieval.
- **User ID Scoping:** Each memory is tagged with a user ID, so multiple users can have isolated memory banks.
- **LangChain Tools:** Custom tools (`save_user_memory`, `retrieve_user_memories`) let the agent interact with the memory store.

---

## Project Structure

```
memory_agent_project/
├── src/
│   ├── memory_tool.py         # Memory management logic and LangChain tools
│   ├── test_memory_agent.py   # Script to test agent memory functions
│   └── streamlit_app.py       # Streamlit web app
├── docs/
│   ├── ui_design.md           # UI design documentation
│   ├── Evaluation_Plan.md     # Evaluation scenarios and metrics
│   ├── prompts.md             # Agent prompt documentation
│   └── Voice_Integration.md   # Guide for adding voice input
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
└── README.md                  # Project overview and instructions
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/pranavv1210/AI-Memory-Agent.git
cd AI-Memory-Agent/memory_agent_project
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```
**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

=======
>>>>>>> 9c296a2e49b67d26160bd188523f99e3c9fab3e2
```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Copy `.env.example` to `.env` and add your API key(s):

- For Gemini:
  ```
  GOOGLE_API_KEY="your-google-gemini-api-key-here"
  ```
- For OpenAI (optional):
  ```
  OPENAI_API_KEY="your-openai-api-key-here"
  ```

---

## Usage

### 1. Run Core Logic Test

```bash
cd src
python test_memory_agent.py
```
This script demonstrates saving and retrieving user memories.

### 2. Launch the Streamlit App

```bash
cd src
streamlit run streamlit_app.py
```
Interact with the agent, view and clear memories in the sidebar.

---

<<<<<<< HEAD
## UI Walkthrough

1. **Main Chat Area:**
  - Type messages to the agent.
  - See conversation history with clear user/AI labels.
2. **Sidebar (Memory Debug Panel):**
  - View all stored memories for your user ID.
  - Clear all memories for a fresh start.
  - See real-time updates as you interact.

### Example Inputs

- "My name is Alex."
- "I love hiking."
- "What is my name?"
- "Do I enjoy hiking?"
- "Clear all memories" (use sidebar button)

---

## How the Memory Mechanism Works (Deep Dive)

1. **Information Extraction:**
  - The agent parses user input for facts, preferences, or context.
  - Example: "My favorite color is blue." → fact to remember.
2. **Embedding Generation:**
  - Text is converted to a vector using Gemini/OpenAI embeddings.
  - Similar meanings produce similar vectors.
3. **Storage:**
  - Vector and metadata (user ID, context) are stored in ChromaDB.
4. **Retrieval:**
  - When you ask a recall question, the agent embeds your query and searches for semantically similar memories.
  - Example: "Do I like outdoor activities?" matches "I love hiking."
5. **Context Augmentation:**
  - Retrieved memories are fed back to the LLM to generate more informed, personalized responses.
=======
## How the Memory Mechanism Works

1. **Information Extraction:** The agent identifies important facts/preferences from user input.
2. **Embedding Generation:** Converts info into semantic vectors using Gemini or OpenAI embeddings.
3. **Storage:** Embeddings and metadata are stored in ChromaDB, scoped by user ID.
4. **Retrieval:** Queries are embedded and matched to stored memories for semantic recall.
5. **Context Augmentation:** Retrieved memories are used to inform agent responses.
>>>>>>> 9c296a2e49b67d26160bd188523f99e3c9fab3e2

---

## Evaluation & Testing

See `docs/Evaluation_Plan.md` for scenario-based tests and success metrics. Example test cases:
- Teach the agent your name and preferences.
- Ask recall questions ("What is my name?", "Do I like hiking?").
- Clear memories and verify recall fails.

---

## UI Design

See `docs/ui_design.md` for details. The app features:
- Main chat area for conversation
- Sidebar for memory visualization and clearing
- Real-time updates of stored memories

---

## Advanced & Future Work

- **Voice Input:** See `docs/Voice_Integration.md` for adding Whisper-based speech-to-text.
- **Prompt Engineering:** Customize agent behavior via `docs/prompts.md`.
- **Extensibility:** Add new tools, memory types, or LLMs as needed.

---

<<<<<<< HEAD
## Troubleshooting & Best Practices

- **Missing Files in Repo:** Ensure all files are at the repo root before pushing.
- **API Key Issues:** Double-check `.env` for correct keys and spelling.
- **Dependency Errors:** Run `pip install -r requirements.txt` in your activated virtual environment.
- **Streamlit Issues:** Make sure Streamlit is installed and your virtual environment is active.
- **ChromaDB Deprecation Warnings:** Use the latest LangChain/ChromaDB versions and follow migration guides if needed.

---

=======
>>>>>>> 9c296a2e49b67d26160bd188523f99e3c9fab3e2
## Contributing

Pull requests and issues are welcome! Please fork the repo and submit changes via PR.

---

## License

MIT License
