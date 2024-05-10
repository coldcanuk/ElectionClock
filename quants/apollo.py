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

# Load environment variables
env_path = os.getenv('HOME') + "/web/ElectionClockEnvironment/.env"
load_dotenv(dotenv_path=env_path)

# Debug mode check
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin apollo")
logger.debug("Debug mode on")

# API keys and assistant ID
asst_keiko = os.getenv("id_KEIKO")
openai.api_key = os.getenv("keyOPENAI")

if not asst_keiko or not openai.api_key:
    logger.error("API key or Assistant ID not found. Please check your environment variables.")
    sys.exit("Missing critical API configuration.")

def analyze_chunk_in_thread(chunk, assistant_id=asst_keiko):
    try:
        run = openai.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={"messages": [{"role": "user", "content": f"Analyze this section:\n\n{chunk}"}]}
        )
        while True:
            status = openai.beta.threads.runs.retrieve(run_id=run.id,thread_id=run.thread_id).status
            if status == "completed":
                break
            elif status in ["failed", "cancelled"]:
                raise Exception(f"Run failed or was cancelled. Status: {status}")
            time.sleep(10)

        response = openai.beta.threads.messages.list(run_id=run.id,thread_id=run.thread_id)
        if response.data:
            return response.data[0].content
        return {"error": "No response found"}
    except Exception as e:
        logger.error(f"Thread Analysis Failed: {e}")
        return {"error": str(e)}

def analyze_chunks_from_vector_store():
    results = search_documents("C-70_E", n_results=1)
    if not results["documents"]:
        raise ValueError("Document not found in vector store")

    document = results["documents"][0][0]
    chunk_size = 3500
    chunks = [document[i:i + chunk_size] for i in range(0, len(document), chunk_size)]

    output = {}
    for i, chunk in enumerate(chunks, 1):
        result = analyze_chunk_in_thread(chunk)
        output[f"Analysis of Chunk {i}"] = {"text": result}

    with open("C-70_E_analysis.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    logger.info("Analysis complete and saved to file.")

if __name__ == "__main__":
    analyze_chunks_from_vector_store()
