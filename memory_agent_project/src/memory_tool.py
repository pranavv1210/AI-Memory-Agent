import os
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from typing import List, Dict
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool, Tool

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get Google API Key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")

class MemoryStore:
    """Manages storing and retrieving memories for the AI agent."""
    def __init__(self, user_id: str, collection_name: str = "user_memories"):
        """
        Initializes the MemoryStore for a specific user.
        Args:
            user_id (str): The unique identifier for the user.
            collection_name (str): The name of the ChromaDB collection to use.
                                   This helps organize memories if you have multiple types.
        """
        self.user_id = user_id
        self.embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004", google_api_key=GOOGLE_API_KEY)
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory="./chroma_db_data"
        )
        os.makedirs("./chroma_db_data", exist_ok=True)
        print(f"MemoryStore initialized for user: {user_id} using collection: {collection_name}")


    def save_memory(self, content: str, context: str = "") -> None:
        """
        Saves a piece of information as a memory for the current user.
        Args:
            content (str): The main information to be stored.
            context (str): Additional context related to the memory.
        """
        doc = Document(page_content=content, metadata={"user_id": self.user_id, "context": context})
        print(f"Saving memory for user {self.user_id}: '{content}' (Context: '{context}')")
        self.vector_store.add_documents([doc])
        self.vector_store.persist()
        print("Memory saved and persisted.")

    def retrieve_memories(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """
        Retrieves relevant memories based on a query for the current user.
        Args:
            query (str): The query string to search for relevant memories.
            k (int): The number of top relevant memories to retrieve.
        Returns:
            List[Dict[str, str]]: A list of dictionaries, each representing a retrieved memory.
        """
        print(f"Retrieving memories for user {self.user_id} with query: '{query}'")
        results = self.vector_store.similarity_search(query, k=k, filter={"user_id": self.user_id})

        memories = []
        for doc in results:
            memories.append({
                "content": doc.page_content,
                "context": doc.metadata.get("context", "No context provided.")
            })
        print(f"Retrieved {len(memories)} memories.")
        return memories

    def get_all_memories(self) -> List[Dict[str, str]]:
        """
        Retrieves all memories for the current user. Useful for debugging/visualization.
        Returns:
            List[Dict[str, str]]: A list of dictionaries, each representing a retrieved memory.
        """
        print(f"Retrieving all memories for user {self.user_id} for debugging.")
        all_docs = self.vector_store.get(where={"user_id": self.user_id}, include=['documents', 'metadatas'])

        memories = []
        if all_docs and all_docs.get('documents') and all_docs.get('metadatas'):
            for i in range(len(all_docs['documents'])):
                memories.append({
                    "content": all_docs['documents'][i],
                    "context": all_docs['metadatas'][i].get("context", "No context provided.")
                })
        print(f"Retrieved {len(memories)} total memories for display.")
        return memories

class SaveMemorySchema(BaseModel):
    content: str = Field(..., description="The information to be stored.")
    context: str = Field("", description="Additional context related to the memory.")

class MemoryTools:
    def __init__(self, user_id: str):
        self.memory_store = MemoryStore(user_id=user_id)

    def save_user_memory(self, content: str, context: str = "") -> str:
        """
        Saves a significant piece of information or user preference to the long-term memory for a specific user.
        """
        try:
            self.memory_store.save_memory(content=content, context=context)
            return f"Memory '{content}' saved successfully."
        except Exception as e:
            return f"Failed to save memory: {e}"

    def retrieve_user_memories(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """
        Retrieves relevant memories from the long-term memory for a specific user based on a query.
        """
        try:
            memories = self.memory_store.retrieve_memories(query=query, k=k)
            if memories:
                formatted_memories = "\n".join([
                    f"- Content: {m['content']} (Context: {m['context']})" for m in memories
                ])
                return f"Retrieved memories:\n{formatted_memories}"
            else:
                return f"No relevant memories found for query '{query}'."
        except Exception as e:
            return f"Failed to retrieve memories: {e}"

def get_tools(user_id: str):
    memory_tools = MemoryTools(user_id)
    tools = [
        StructuredTool.from_function(
            func=memory_tools.save_user_memory,
            name="save_user_memory",
            description="Saves a significant piece of information or user preference to the long-term memory for a specific user.",
            args_schema=SaveMemorySchema,
        ),
        Tool(
            name="retrieve_user_memories",
            func=memory_tools.retrieve_user_memories,
            description="Retrieves relevant memories from the long-term memory for a specific user based on a query.",
        ),
    ]
    return tools

def clear_user_memories(user_id: str, collection_name: str = "user_memories"):
    """
    Clears all memories for a specific user from the ChromaDB collection.
    WARNING: This will permanently delete all memories for the specified user.
    """
    print(f"Attempting to clear memories for user: {user_id} from collection: {collection_name}")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004", google_api_key=GOOGLE_API_KEY)
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory="./chroma_db_data"
        )
        vector_store.delete_collection()
        Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory="./chroma_db_data"
        )
        print(f"All memories for user {user_id} in collection {collection_name} have been cleared.")
    except Exception as e:
        print(f"Error clearing memories: {e}")
