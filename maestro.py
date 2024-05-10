# maestro.py
import os
import subprocess
from datetime import datetime
from quants.tsionhehkwen import add_chunks_to_vector_store, get_analysis_results
from dotenv import load_dotenv

# Load environment variables
env_path =  os.getenv('HOME') + "/web/ElectionClockEnvironment/.env"
load_dotenv(dotenv_path=env_path)
# Constants
BILL_NAME = "C-70_E"
TEXT_FILE_PATH = f"extractors/taillings/{BILL_NAME}.txt"
ANALYSIS_FILE_PATH = f"extractors/taillings/{BILL_NAME}_analysis.txt"
MAX_FILE_AGE_DAYS = 30

# Function to execute xml2text.py
def run_extractor():
    try:
        result = subprocess.run(["python3", "extractors/xml2text.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error in xml2text.py: {result.stderr}")
        else:
            print(result.stdout)
    except Exception as e:
        print(f"Failed to run xml2text.py: {e}")

# Check if the text file exists and is less than a month old
def is_text_file_valid(file_path, max_age_days=30):
    if os.path.exists(file_path):
        file_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_path))).days
        return file_age_days < max_age_days
    return False

# Add document to vector store
def add_to_vector_store(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        document = f.read()
    add_chunks_to_vector_store(document, doc_id=BILL_NAME)

# Update law data function
def update_law_data():
    if not is_text_file_valid(TEXT_FILE_PATH, MAX_FILE_AGE_DAYS):
        run_extractor()
        add_to_vector_store(TEXT_FILE_PATH)
    else:
        print(f"{BILL_NAME}.txt is valid. No need to download and parse.")
    
    analysis = get_analysis_results(f"{BILL_NAME}_Analysis", n_results=1)
    with open(ANALYSIS_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(f"### Analysis of Chunk 1:\n{analysis}")

# Main function
if __name__ == "__main__":
    update_law_data()
