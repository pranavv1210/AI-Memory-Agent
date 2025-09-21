
Evaluation Plan for AI Memory Agent
Evaluating an AI agent with long-term memory is crucial to ensure it's effectively learning and recalling information. Unlike simple chatbots, memory agents require testing not just for immediate responses, but for their ability to maintain context and personalize interactions over time.

## 1. Why Evaluate Memory?

* **Accuracy of Recall:** Does the agent retrieve the *correct* memory when prompted?
* **Relevance:** Are the saved memories truly important and useful for future interactions?
* **Persistence:** Does the agent remember information across simulated sessions (i.e., after the app is restarted or the chat history is cleared, but the `user_id` remains the same)?
* **Efficiency:** Is the agent saving too much irrelevant information, or missing key facts?
* **Contextual Understanding:** Can the agent apply retrieved memories in new, related contexts?

## 2. Evaluation Approach

We will use a qualitative, scenario-based evaluation for this project. This involves providing specific sequences of prompts and observing the agent's behavior and the contents of its memory bank.

## 3. Test Cases & Expected Outcomes

Each test case will involve a sequence of user inputs designed to:
* **Induce Memory Saving:** Get the agent to identify and store a new piece of information.
* **Test Immediate Recall:** Check if the agent remembers the information right after saving.
* **Test Delayed Recall:** Check if the agent remembers the information after a few unrelated turns or in a new session (by clearing `st.session_state.chat_history` but keeping `user_id`).
* **Test Semantic Recall:** Check if the agent can retrieve a memory even if the query is phrased differently.

---

**Test Case 1: Remembering User Name & Preference**

* **Setup:** Start with cleared memories (use the "Clear All Memories" button).
* **User Input Sequence:**
	1.  "Hi, my name is Alex."
	2.  "I love hiking in the mountains."
	3.  "What did I tell you my name was?"
	4.  "Do I enjoy outdoor activities?" (Testing semantic recall)
* **Expected Memory Saves (in Sidebar):**
	* `content: "User's name is Alex."`
	* `content: "User loves hiking in the mountains."`
* **Expected AI Responses:**
	1.  Acknowledges name.
	2.  Acknowledges preference.
	3.  "Your name is Alex." (Or similar, directly recalling)
	4.  "Yes, you love hiking in the mountains." (Or similar, using semantic recall)

---

**Test Case 2: Remembering a Specific Fact**

* **Setup:** Start with cleared memories.
* **User Input Sequence:**
	1.  "My birthday is on July 20th."
	2.  "Okay, let's talk about the weather today."
	3.  "What's the date of my birthday?"
* **Expected Memory Saves:**
	* `content: "User's birthday is on July 20th."`
* **Expected AI Responses:**
	1.  Acknowledges birthday.
	2.  Responds about weather.
	3.  "Your birthday is on July 20th."

---

**Test Case 3: Handling Ambiguous/Non-Memorable Input**

* **Setup:** Start with cleared memories.
* **User Input Sequence:**
	1.  "The sky is blue." (Fact that might not need to be memorized)
	2.  "I feel alright today." (Subjective, probably not a memory)
	3.  "Do you remember anything special about me?"
* **Expected Memory Saves:** *Preferably no new memories, or only very generic ones if the LLM interprets "special" differently.* The key is that it *doesn't* save "sky is blue" or "feel alright."
* **Expected AI Responses:**
	1.  Acknowledges sky color.
	2.  Responds appropriately to feeling.
	3.  "Based on our conversation, I don't have any specific special memories saved about you yet. Is there anything you'd like me to remember?"

---

## 4. Metrics for Success (Qualitative)

* **Memory Capture Rate:** For important facts/preferences, does the agent *consistently* save them?
* **Memory Recall Accuracy:** When asked to recall, does the agent retrieve the *exact* or *semantically correct* information?
* **Memory Quality:** Are the saved memories concise and useful, or are they verbose and irrelevant? (Check the sidebar).
* **Conversation Flow:** Does the agent's use of memory lead to a more natural and personalized conversation?

## 5. Iterative Improvement

After running these tests:
* **Review `st.session_state.chat_history`:** See the full conversation.
* **Review Streamlit Sidebar:** Inspect the actual memories saved in ChromaDB.
* **Review Agent `verbose=True` output:** Look at the terminal where Streamlit is running to see *why* the agent chose to use (or not use) a tool and its reasoning process. This is critical for debugging agent behavior.

Based on the observations, you can fine-tune:
* The system prompt for the agent (in `streamlit_app.py` or a dedicated `prompts.py` file) to better guide when it should use the `save_user_memory` tool.
* The `content` and `context` passed to `save_user_memory` by the agent.

This evaluation plan provides a structured way to assess and improve the core memory mechanism of your AI agent.
