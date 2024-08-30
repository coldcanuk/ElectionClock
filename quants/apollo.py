import openai
import os
import sys
import time
import json
from dotenv import load_dotenv
from loguru import logger

# Add the root directory to the Python path for module imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the function to search documents from the vector store
from quants.tsionhehkwen import search_documents

# Load environment variables from the .env file
env_path = os.getenv('HOME') + "/web/ElectionClockEnvironment/.env"
load_dotenv(dotenv_path=env_path)

# Check if the application is running in debug mode
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger for console output
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin apollo")
logger.debug("Debug mode on")

# Retrieve API keys and assistant ID from environment variables
asst_keiko = os.getenv("id_KEIKO")
openai.api_key = os.getenv("keyOPENAI")

# Ensure critical API configuration is available
if not asst_keiko or not openai.api_key:
    logger.error("API key or Assistant ID not found. Please check your environment variables.")
    sys.exit("Missing critical API configuration.")

# Function to analyze a chunk of text using OpenAI's API
def analyze_chunk_in_thread(chunk, assistant_id=asst_keiko):
    """
    Sends a chunk of text to the OpenAI API for analysis in a thread.
    :param chunk: The text chunk to be analyzed.
    :param assistant_id: The ID of the AI assistant used for analysis.
    :return: The analysis result as a string or an error message.
    """
    try:
        # Create and run a new thread for the analysis
        run = openai.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={"messages": [{"role": "user", "content": f"Analyze this section:\n\n{chunk}"}]}
        )
        # Poll the status until the analysis is complete
        while True:
            status = openai.beta.threads.runs.retrieve(run_id=run.id, thread_id=run.thread_id).status
            if status == "completed":
                break
            elif status in ["failed", "cancelled"]:
                raise Exception(f"Run failed or was cancelled. Status: {status}")
            time.sleep(10)

        # Retrieve and return the first message from the analysis response
        response = openai.beta.threads.messages.list(run_id=run.id, thread_id=run.thread_id)
        if response.data:
            return response.data[0].content
        return {"error": "No response found"}
    except Exception as e:
        logger.error(f"Thread Analysis Failed: {e}")
        return {"error": str(e)}

# Custom JSON encoder to handle complex objects
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__  # Serialize objects by their dictionary representation
        return json.JSONEncoder.default(self, obj)

# Function to analyze chunks of text retrieved from the vector store
def analyze_chunks_from_vector_store():
    """
    Retrieves each chunk of the document from the vector store and sends it
    to the OpenAI API for analysis. The results are saved to a JSON file.
    """
    # Search for the document chunks in the vector store
    results = search_documents("C-70_E", n_results=100)
    if not results["documents"]:
        raise ValueError("No chunks found for the document in the vector store")

    logger.info(f"Total chunks to process: {len(results['documents'])}")
    output = {}

    # Analyze each chunk and store the results
    for i, (chunk, _) in enumerate(results['documents'], 1):
        logger.debug(f"Processing chunk {i} of {len(results['documents'])}")
        result = analyze_chunk_in_thread(chunk)
        output[f"Analysis of Chunk {i}"] = {"text": result}
        logger.debug(f"Completed processing chunk {i}")

    # Serialize the output using the custom encoder and save it to a file
    output_string = json.dumps(output, indent=2, cls=CustomEncoder)
    logger.info("Output as a single string for inspection:")
    logger.info(output_string)

    output_directory = "extractors/taillings/"  # Directory to save the output file
    output_file_path = os.path.join(output_directory, "C-70_E_analysis.json")

    try:
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(output_string)  # Write the output to a file
        logger.info("Analysis complete and saved to file.")
    except Exception as e:
        logger.error(f"Failed to write output to file: {e}")

# Main function to start the analysis process
if __name__ == "__main__":
    analyze_chunks_from_vector_store()
