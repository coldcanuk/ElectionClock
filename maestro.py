# maestro.py
import sys
import os
import subprocess
from datetime import datetime
from quants.tsionhehkwen import add_documents
from loguru import logger
from dotenv import load_dotenv

# Constants
TEXT_FILE_PATH = "extractors/taillings/C-70_E.txt"
MAX_FILE_AGE_DAYS = 30
CHUNK_SIZE = 2000  # Adjust this chunk size as needed

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from the .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ElectionClockEnvironment/.env')
load_dotenv(dotenv_path=env_path)

# Determine if the application is running in debug mode based on environment variable
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
logger.info(f"The debug_mode is: {DEBUG_MODE}")

# Set the logging level based on whether the application is in debug mode
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin maestro")
logger.debug("Debug mode on")

# Function to execute xml2text.py
def run_extractor():
    try:
        result = subprocess.run(["python3", "extractors/xml2text.py"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error in xml2text.py: {result.stderr}")
        else:
            logger.info(result.stdout)
    except Exception as e:
        logger.error(f"Failed to run xml2text.py: {e}")

# Function to execute apollo.py
def run_analysis():
    try:
        result = subprocess.run(["python3", "quants/apollo.py"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error in apollo.py: {result.stderr}")
        else:
            logger.info(result.stdout)
    except Exception as e:
        logger.error(f"Failed to run apollo.py: {e}")

# Check if the text file exists and is less than a month old
def is_text_file_valid(file_path, max_age_days=30):
    if os.path.exists(file_path):
        file_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_path))).days
        return file_age_days < max_age_days
    return False

# Add document to vector store
def add_to_vector_store(file_path, chunk_size=2000):
    with open(file_path, "r", encoding="utf-8") as f:
        document = f.read()

    # Split the document into chunks
    chunks = [document[i:i + chunk_size] for i in range(0, len(document), chunk_size)]
    ids = [f"C-70_E_{i+1}" for i in range(len(chunks))]

    logger.debug(f"Chunking document into {len(chunks)} chunks.")
    add_documents(chunks, ids=ids)

# Main function
if __name__ == "__main__":
    if not is_text_file_valid(TEXT_FILE_PATH, MAX_FILE_AGE_DAYS):
        run_extractor()
        add_to_vector_store(TEXT_FILE_PATH, CHUNK_SIZE)
    else:
        logger.info("C-70_E.txt is valid. No need to download and parse.")
    run_analysis()
