

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

## How the Memory Mechanism Works

1. **Information Extraction:** The agent identifies important facts/preferences from user input.
2. **Embedding Generation:** Converts info into semantic vectors using Gemini or OpenAI embeddings.
3. **Storage:** Embeddings and metadata are stored in ChromaDB, scoped by user ID.
4. **Retrieval:** Queries are embedded and matched to stored memories for semantic recall.
5. **Context Augmentation:** Retrieved memories are used to inform agent responses.

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

## Contributing

Pull requests and issues are welcome! Please fork the repo and submit changes via PR.

---

## License

MIT License
