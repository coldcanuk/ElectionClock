# quants/tsionhehkwen.py
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# Load environment variables from the .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ElectionClockEnvironment/.env')
load_dotenv(dotenv_path=env_path)
# Ensure the vector store directory exists
vector_store_directory = "quants/vector_store"
os.makedirs(vector_store_directory, exist_ok=True)
# Initialize the ChromaDB client with disk persistence
client = chromadb.PersistentClient(path=vector_store_directory)
# Retrieve the OpenAI key
openai_key = os.getenv("keyOPENAI")
if not openai_key:
    raise ValueError("OpenAI API key not found. Please set 'keyOPENAI' in the environment variables.")

# Use OpenAI's `text-embedding-ada-002` model
embedding_function = OpenAIEmbeddingFunction(api_key=openai_key, model_name="text-embedding-ada-002")

# Retrieve or create the collection
collection = client.get_or_create_collection(
    name="Tsionhehkwen",
    embedding_function=embedding_function
)

# Create a collection for analysis results
analysis_collection = client.get_or_create_collection(
    name="AnalysisResults",
    embedding_function=embedding_function
)

# Function to add documents to the vector store
def add_documents(documents, ids=None, metadatas=None):
    if ids is None:
        ids = [str(i) for i in range(len(documents))]
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

# Function to add chunks to the vector store
def add_chunks_to_vector_store(document, doc_id):
    chunks = document.split("\n")  # Split the document into chunks based on newlines
    add_documents(chunks, ids=[f"{doc_id}_{i}" for i in range(len(chunks))])

# Function to search for documents in the vector store
def search_documents(query, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

# Function to add analysis results
def add_analysis_results(results, ids=None, metadatas=None):
    if ids is None:
        ids = [str(i) for i in range(len(results))]
    analysis_collection.add(
        documents=results,
        ids=ids,
        metadatas=metadatas
    )

# Function to retrieve analysis results
def get_analysis_results(query, n_results=5):
    results = analysis_collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

# Function to list all analysis results
def list_all_analysis_results():
    return analysis_collection.peek()

# Function to delete all analysis results
def delete_all_analysis_results():
    ids_to_delete = analysis_collection.get()["ids"]
    analysis_collection.delete(ids=ids_to_delete)

    # Verify if deletion was successful
    remaining_ids = analysis_collection.get()["ids"]
    if not remaining_ids:
        return "All analysis results deleted successfully."
    else:
        return f"Warning: Some analysis results could not be deleted. Remaining IDs: {remaining_ids}"
