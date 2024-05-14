# quants/tsionhehkwen.py
import os
import sys
from dotenv import load_dotenv
from loguru import logger
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# Load environment variables from the .env file
env_path = os.getenv('HOME') + "/web/ElectionClockEnvironment/.env"
load_dotenv(dotenv_path=env_path)

# Determine if the application is running in debug mode based on environment variable
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin tsionhehkwen")
logger.debug("Debug mode on")

# Ensure the vector store directory exists
vector_store_directory = "quants/vector_store"
os.makedirs(vector_store_directory, exist_ok=True)

# Initialize the ChromaDB client with disk persistence
client = chromadb.PersistentClient(path=vector_store_directory)

# Retrieve the OpenAI key
openai_key = os.getenv("keyOPENAI")
if not openai_key:
    logger.error("OpenAI API key not found. Please set 'keyOPENAI' in the environment variables.")
    raise ValueError("OpenAI API key not found. Please set 'keyOPENAI' in the environment variables.")

# Use OpenAI's `text-embedding-ada-002` model
try:
    logger.info("Use OpenAI's `text-embedding-ada-002` model")
    embedding_function = OpenAIEmbeddingFunction(api_key=openai_key, model_name="text-embedding-ada-002")
    logger.info("Successfully successed!")
except Exception as e:
    logger.error(f"We failed our embedding thing: {e}")

# Retrieve or create the collection
try:
    logger.info("Retrieve or create the collection")
    collection = client.get_or_create_collection(
        name="Tsionhehkwen",
        embedding_function=embedding_function
    )
except Exception as e:
    logger.error(f"We failed to retrieve or create the collection:  {e}")

# Create a collection for analysis results
try:
    logger.info("Create a collection for analysis results")
    analysis_collection = client.get_or_create_collection(
        name="AnalysisResults",
        embedding_function=embedding_function
    )
except Exception as e:
    logger.error(f"Failed to Create a collection for analysis results:  {e}")

# Function to add documents to the vector store
def add_documents(documents, ids=None, metadatas=None):
    logger.debug(f"Begin function add_documents with documents: {documents}")
    if ids is None:
        ids = [str(i) for i in range(len(documents))]
    try:
        logger.info(f"Adding {len(documents)} documents to the vector store.")
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        logger.info("Documents added successfully.")
    except Exception as e:
        logger.error(f"Error in add_documents: {e}")

# Function to add chunks to the vector store
def add_chunks_to_vector_store(document, doc_id):
    logger.debug(f"Adding chunks to vector store for doc_id: {doc_id}")
    chunks = [document[i:i+2000] for i in range(0, len(document), 2000)]
    ids = [f"{doc_id}_{i+1}" for i in range(len(chunks))]
    add_documents(chunks, ids=ids)

# Function to search for documents in the vector store
#def search_documents(query, n_results=5):
#    try:
#        logger.debug(f"Searching for query: {query} with n_results: {n_results}")
#        results = collection.query(
#            query_texts=[query],
#            n_results=n_results
#        )
#        logger.debug(f"Search results: {results}")
#        return results
#    except Exception as e:
#        logger.error(f"Error in search_documents: {e}")
#        return {}
def search_documents(query, n_results=None):
    try:
        results = []
        page = 0
        page_size = 10  # Define a reasonable page size for pagination

        while True:
            logger.debug(f"Searching for query: {query} with n_results: {n_results} at page: {page}")
            current_results = collection.query(
                query_texts=[query],
                n_results=n_results if n_results is not None else page_size,
                offset=page * page_size
            )
            if not current_results['documents']:
                break  # Break if no more documents are returned
            results.extend(current_results['documents'])
            if n_results is not None and len(results) >= n_results:
                results = results[:n_results]  # Limit results if n_results is specified
                break
            if n_results is None:
                page += 1  # Only increment page if fetching all documents

        logger.debug(f"Total documents fetched: {len(results)}")
        return {'documents': results}
    except Exception as e:
        logger.error(f"Error in search_documents: {e}")
        return {'documents': []}









# Function to add analysis results
def add_analysis_results(results, ids=None, metadatas=None):
    if ids is None:
        ids = [str(i) for i in range(len(results))]
    logger.debug(f"adding add_analysis_results results: {results}")
    analysis_collection.add(
        documents=results,
        ids=ids,
        metadatas=metadatas
    )

# Function to retrieve analysis results
def get_analysis_results(query, n_results=5):
    try:
        logger.debug(f"Fetching analysis results for query: {query} with n_results: {n_results}")
        results = analysis_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        logger.debug(f"Analysis results: {results}")
        return results
    except Exception as e:
        logger.error(f"Error in get_analysis_results: {e}")
        return {}

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
