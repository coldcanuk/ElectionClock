import openai
import os
import sys
import time
from dotenv import load_dotenv

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from quants.tsionhehkwen import search_documents

# Load environment variables from the .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ElectionClockEnvironment/.env')
load_dotenv(dotenv_path=env_path)

# Retrieve Keiko's assistant ID and OpenAI API key
#asst_keiko = os.getenv("id_KEIKO")
asst_keiko = os.environ.get("id_KEIKO")
#openai.api_key = os.getenv("keyOPENAI")
openai.api_key = os.environ.get("keyOPENAI")

# Function to analyze a chunk via Keiko's thread
def analyze_chunk_in_thread(chunk, assistant_id=asst_keiko):
    try:
        # Create and run a new thread
        run = openai.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={
                "messages": [
                    {"role": "user", "content": f"Analyze this section:\n\n{chunk}"}
                ]
            }
        )
        # Wait for the run to complete
        thread_id = run.thread_id
        run_id = run.id
        intLoop = 0
        sleep_time = 10
        while True:
            print(f"in the while loop at iteration: {intLoop} and sleep timer of {sleep_time}")
            status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id).status
            print(f"the status: {status}, thread_id: {thread_id}, run_id: {run_id}")
            
            if status == "completed":
                print(f"{status} matched completed")
                break
            elif status in ["failed", "cancelled"]:
                raise Exception(f"Run failed or was cancelled. Status: {status}")
            time.sleep(sleep_time)
            intLoop += 1
            sleep_time += 2

        # Retrieve and return the relevant message(s)
        thread_messages = openai.beta.threads.messages.list(
            thread_id=thread_id,
            run_id=run_id,
            order="asc",
            limit=1
        )

        if thread_messages.data:
            response_content = thread_messages.data[0].content
        else:
            response_content = "No response found"

        return response_content
    except Exception as e:
        return f"Thread Analysis Failed: {e}"

# Function to analyze chunks in the vector store
def analyze_chunks_from_vector_store():
    results = search_documents("C-70_E", n_results=1)
    if not results["documents"]:
        raise ValueError("Document C-70_E not found in Tsionhehkwen")
    document = results["documents"][0]

    # Split the document into chunks
    chunk_size = 3500
    chunks = [document[i:i + chunk_size] for i in range(0, len(document), chunk_size)]

    # Analyze each chunk
    output = []
    for i, chunk in enumerate(chunks, 1):
        try:
            analysis = analyze_chunk_in_thread(chunk)
            output.append(f"### Analysis of Chunk {i}:\n{analysis}\n\n")
        except Exception as e:
            output.append(f"### Analysis of Chunk {i} Failed:\n{e}\n\n")

    # Save the complete analysis to a file
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extractors/taillings/analysis.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(output)

    print("Analysis complete and saved to file.")

# Main function
if __name__ == "__main__":
    analyze_chunks_from_vector_store()
