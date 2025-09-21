
Agent Prompts Documentation
This document outlines the system prompt used to guide the behavior of the LangChain AI agent. The prompt is crucial for defining the agent's persona, its capabilities (especially tool usage), and its interaction style.

## 1. Current System Prompt

The primary system prompt for the `create_openai_functions_agent` is defined within `src/streamlit_app.py` (and also in `src/test_memory_agent.py` for testing purposes).

```python
prompt = ChatPromptTemplate.from_messages([
	("system", """You are a helpful AI assistant with the ability to remember user preferences and facts.\n     You have access to tools to save and retrieve memories.\n     When you learn something important about the user (e.g., their name, favorite things, important facts), use the 'save_user_memory' tool.\n     When the user asks a question that might require recalling past information, use the 'retrieve_user_memories' tool.\n     Always address the user by name if you know it from memory.\n     Provide concise and helpful responses.\n     """),
	MessagesPlaceholder(variable_name="chat_history"),
	("user", "{input}"),
	MessagesPlaceholder(variable_name="agent_scratchpad"),
])
```

## 2. Purpose and Explanation of the Prompt

This system prompt serves several key purposes:

* **Defines Agent Persona:** "You are a helpful AI assistant..." establishes a friendly and assistive tone.
* **States Core Capability:** "...with the ability to remember user preferences and facts." directly informs the LLM that memory is a core function.
* **Explicit Tool Instructions:**
	* `"You have access to tools to save and retrieve memories."`: Informs the LLM that tools are available for memory management.
	* `"When you learn something important about the user (e.g., their name, favorite things, important facts), use the 'save_user_memory' tool."`: This is a critical instruction for **when** to use the saving tool. It provides examples of what constitutes "important information." This part is key to controlling the *quality* and *frequency* of memory saving.
	* `"When the user asks a question that might require recalling past information, use the 'retrieve_user_memories' tool."`: This guides the LLM on **when** to use the retrieval tool, linking it to the need for past context.
* **Interaction Guidelines:**
	* `"Always address the user by name if you know it from memory."`: Encourages personalized responses. This leverages the retrieval tool's output.
	* `"Provide concise and helpful responses."`: Guides the output format and verbosity.
* **Placeholders (LangChain Specific):**
	* `MessagesPlaceholder(variable_name="chat_history")`: This is where LangChain will inject the preceding turns of the conversation, allowing the LLM to maintain short-term context.
	* `MessagesPlaceholder(variable_name="agent_scratchpad")`: This is where LangChain injects the agent's thoughts, tool calls, and tool outputs, enabling the LLM to reason and see the results of its actions.

## 3. Customization and Experimentation

This prompt can be customized to change the agent's behavior:

* **Memory Saving Criteria:** Experiment with what defines "important" information. For example, you could add:
	* `"...only save facts that are explicitly stated as preferences or critical biographical details."`
	* `"...ask for confirmation before saving a memory if unsure of its importance."`
* **Retrieval Guidance:** You could refine when it should retrieve:
	* `"...only retrieve memories if the current conversation topic is directly related to a past preference."`
* **Persona Adjustment:** Change the opening sentence to make the agent more formal, informal, empathetic, etc.
* **Response Style:** Adjust "concise and helpful" to "creative and humorous" or "detailed and factual."

Regularly reviewing and refining the prompt is a key part of iterating on the agent's intelligence and effectiveness.
