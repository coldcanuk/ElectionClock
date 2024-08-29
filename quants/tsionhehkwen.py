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

# Determine if the application is running in debug mode
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger for console output
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin tsionhehkwen")
logger.debug("Debug mode on")

# Ensure the vector store directory exists
vector_store_directory = "quants/vector_store"
os.makedirs(vector_store_directory, exist_ok=True)

# Initialize the ChromaDB client with disk persistence
client = chromadb.PersistentClient(path=vector_store_directory)

# Retrieve the OpenAI API key
openai_key = os.getenv("keyOPENAI")
if not openai_key:
    logger.error("OpenAI API key not found. Please set 'keyOPENAI' in the environment variables.")
    raise ValueError("OpenAI API key not found. Please set 'keyOPENAI' in the environment variables.")

# Initialize the embedding function using OpenAI's `text-embedding-ada-002` model
try:
    logger.info("Use OpenAI's `text-embedding-ada-002` model")
    embedding_function = OpenAIEmbeddingFunction(api_key=openai_key, model_name="text-embedding-ada-002")
    logger.info("Successfully initialized embedding function.")
except Exception as e:
    logger.error(f"Failed to initialize embedding function: {e}")

# Retrieve or create the main document collection in the vector store
try:
    logger.info("Retrieve or create the collection")
    collection = client.get_or_create_collection(
        name="Tsionhehkwen",
        embedding_function=embedding_function
    )
except Exception as e:
    logger.error(f"Failed to retrieve or create the collection: {e}")

# Retrieve or create the collection for analysis results
try:
    logger.info("Create a collection for analysis results")
    analysis_collection = client.get_or_create_collection(
        name="AnalysisResults",
        embedding_function=embedding_function
    )
except Exception as e:
    logger.error(f"Failed to create a collection for analysis results: {e}")

# Function to add documents to the vector store
def add_documents(documents, ids=None, metadatas=None):
    """
    Adds documents to the vector store.
    :param documents: List of documents (text) to be added.
    :param ids: List of IDs corresponding to the documents.
    :param metadatas: Metadata for each document (optional).
    """
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

# Function to split a document into chunks and add them to the vector store
def add_chunks_to_vector_store(document, doc_id):
    """
    Splits a document into chunks and adds them to the vector store.
    :param document: The full text of the document to be chunked.
    :param doc_id: The base ID for each chunk.
    """
    logger.debug(f"Adding chunks to vector store for doc_id: {doc_id}")
    chunks = [document[i:i+2000] for i in range(0, len(document), 2000)]
    ids = [f"{doc_id}_{i+1}" for i in range(len(chunks))]
    add_documents(chunks, ids=ids)

# Function to search for documents in the vector store
def search_documents(query, n_results=None):
    """
    Searches for documents in the vector store based on a query.
    :param query: The search query (text).
    :param n_results: Number of results to return.
    :return: A dictionary with the search results.
    """
    try:
        results = []
        page = 0
        page_size = 10  # Define a reasonable page size for pagination

        while True:
            logger.debug(f"Searching for query: {query} with n_results: {n_results} at page: {page}")
            current_results = collection.query(
                query_texts=[query],
                n_results=n_results if n_results is not None else page_size,
                # offset=page * page_size #ChromaDB hates offset? not sure
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

# Function to add analysis results to the vector store
def add_analysis_results(results, ids=None, metadatas=None):
    """
    Adds analysis results to the vector store.
    :param results: The analysis results to be stored.
    :param ids: List of IDs corresponding to the results.
    :param metadatas: Metadata for each result (optional).
    """
    if ids is None:
        ids = [str(i) for i in range(len(results))]
    logger.debug(f"Adding analysis results: {results}")
    analysis_collection.add(
        documents=results,
        ids=ids,
        metadatas=metadatas
    )

# Function to retrieve analysis results from the vector store
def get_analysis_results(query, n_results=5):
    """
    Retrieves analysis results from the vector store.
    :param query: The search query (text).
    :param n_results: Number of results to return.
    :return: The search results.
    """
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

# Function to list all analysis results in the vector store
def list_all_analysis_results():
    """
    Lists all analysis results stored in the vector store.
    :return: A list of all analysis results.
    """
    return analysis_collection.peek()

# Function to delete all analysis results from the vector store
def delete_all_analysis_results():
    """
    Deletes all analysis results from the vector store.
    :return: Confirmation message or warning if any results remain.
    """
    ids_to_delete = analysis_collection.get()["ids"]
    analysis_collection.delete(ids=ids_to_delete)

    # Verify if deletion was successful
    remaining_ids = analysis_collection.get()["ids"]
    if not remaining_ids:
        return "All analysis results deleted successfully."
    else:
        return f"Warning: Some analysis results could not be deleted. Remaining IDs: {remaining_ids}"
