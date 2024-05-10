import openai
import os
import sys
import time
import json
from dotenv import load_dotenv
from loguru import logger

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from quants.tsionhehkwen import search_documents

# Load environment variables from the .env file
env_path = os.getenv('HOME') + "/web/ElectionClockEnvironment/.env"
load_dotenv(dotenv_path=env_path)

# Determine if the application is running in debug mode based on the environment variable
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin apollo")
logger.debug("Debug mode on")

# Retrieve Keiko's assistant ID and OpenAI API key
asst_keiko = os.getenv("id_KEIKO")
openai.api_key = os.getenv("keyOPENAI")

if not asst_keiko:
    logger.error("Keiko Assistant ID not found. Please set 'id_KEIKO' in the environment variables.")
    raise ValueError("Keiko Assistant ID not found.")
if not openai.api_key:
    logger.error("OpenAI API key not found. Please set 'keyOPENAI' in the environment variables.")
    raise ValueError("OpenAI API key not found.")

# Function to analyze a chunk via Keiko's thread
def analyze_chunk_in_thread(chunk, assistant_id=asst_keiko):
    try:
        run = openai.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={"messages": [{"role": "user", "content": f"Analyze this section:\n\n{chunk}"}]}
        )
        while True:
            status = openai.beta.threads.runs.retrieve(run.thread_id, run.id).status
            if status == "completed":
                break
            elif status in ["failed", "cancelled"]:
                raise Exception(f"Run failed or was cancelled. Status: {status}")
            time.sleep(10)

        thread_messages = openai.beta.threads.messages.list(
            thread_id=run.thread_id,
            run_id=run.id,
            order="asc",
            limit=1
        )

        if thread_messages.data:
            # Assuming the response content is in the first item of the list
            response_content = thread_messages.data[0].content
            if isinstance(response_content, list):
                # Handle list data here
                response_dict = {"analysis": response_content}  # Convert list to dictionary if necessary
                return response_dict
            else:
                return {"error": "Unexpected data type"}

    except Exception as e:
        logger.error(f"Thread Analysis Failed: {e}")
        return {"error": str(e)}

# Function to analyze chunks in the vector store
def analyze_chunks_from_vector_store():
    logger.info("Begin function analyze_chunks_from_vector_store")
    results = search_documents("C-70_E", n_results=1)
    if not results["documents"] or not results["documents"][0]:
        logger.debug("Document C-70_E not found in Tsionhehkwen")
        raise ValueError("Document C-70_E not found in Tsionhehkwen")
    document = results["documents"][0][0]  # Retrieve the actual document content

    # Split the document into chunks
    chunk_size = 3500
    try:
        chunks = [document[i:i + chunk_size] for i in range(0, len(document), chunk_size)]
    except Exception as e:
        logger.error(f"failed chunks!!:  {e}")

    # Analyze each chunk
    logger.info("Analyze each chunk")
    output = {}
    intLoop = 0
    for i, chunk in enumerate(chunks, 1):
        logger.debug(f"Begin loop at iteration {intLoop}")
        try:
            analysis = analyze_chunk_in_thread(chunk)
            if isinstance(analysis, dict):  # Check if the analysis is already a dictionary
                output[f"Analysis of Chunk {i}"] = {
                    "TextContentBlock": {
                        "text": {
                            "annotations": [],
                            "value": analysis,  # Directly use the dictionary
                            "type": "text"
                        }
                    }
                }
            else:
                raise ValueError("Analysis is not in the expected format.")
            logger.debug(f"### Analysis of Chunk {i}:\n{analysis}\n\n")
            intLoop += 1
        except Exception as e:
            output[f"Analysis of Chunk {i}"] = f"Analysis of Chunk {i} Failed: {e}"
            logger.debug(f"### Analysis of Chunk {i} Failed:\n{e}\n\n")

    # Log the raw JSON output for debugging
    logger.debug(f"Raw pre-JSON output: {output}")

    # Save the complete analysis to a file
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extractors/taillings/C-70_E_analysis.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    logger.info("Analysis complete and saved to file.")

# Main function
if __name__ == "__main__":
    analyze_chunks_from_vector_store()
