# maestro.py

import sys
import os
import subprocess  # For running shell commands
from datetime import datetime  # To handle dates and times
from quants.tsionhehkwen import add_documents  # Function to add documents to the vector store
from loguru import logger  # For logging events and errors
from dotenv import load_dotenv  # To load environment variables from a .env file

# Constants
TEXT_FILE_PATH = "extractors/taillings/C-70_E.txt"  # Path to the text file used for analysis
MAX_FILE_AGE_DAYS = 30  # Maximum age of the text file before it's considered outdated
CHUNK_SIZE = 2000  # Size of the chunks to split the document into for vector storage

# Add the root directory to the Python path to ensure modules are found
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from the .env file located in ElectionClockEnvironment directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ElectionClockEnvironment/.env')
load_dotenv(dotenv_path=env_path)

# Determine if the application is running in debug mode based on environment variable
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
logger.info(f"The debug_mode is: {DEBUG_MODE}")

# Set the logging level based on whether the application is in debug mode
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger to output logs to the console with the appropriate level
logger.remove()  # Remove any default logger configuration
logger.add(sys.stdout, level=log_level)  # Add a new logger that outputs to the console
logger.info("Begin maestro")  # Log the start of the script
logger.debug("Debug mode on")  # Log that debug mode is enabled if applicable

# Function to execute the xml2text.py script
def run_extractor():
    """
    Runs the xml2text.py script to extract data and convert it into a text format.
    """
    try:
        result = subprocess.run(["python3", "extractors/xml2text.py"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error in xml2text.py: {result.stderr}")  # Log an error if the script fails
        else:
            logger.info(result.stdout)  # Log the output of the script if successful
    except Exception as e:
        logger.error(f"Failed to run xml2text.py: {e}")  # Log any exceptions that occur during execution

# Function to execute the apollo.py script
def run_analysis():
    """
    Runs the apollo.py script to perform AI analysis on the extracted data.
    """
    try:
        result = subprocess.run(["python3", "quants/apollo.py"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error in apollo.py: {result.stderr}")  # Log an error if the script fails
        else:
            logger.info(result.stdout)  # Log the output of the script if successful
    except Exception as e:
        logger.error(f"Failed to run apollo.py: {e}")  # Log any exceptions that occur during execution

# Function to check if the text file is valid (i.e., exists and is not too old)
def is_text_file_valid(file_path, max_age_days=30):
    """
    Checks whether the specified text file exists and is within the allowed age limit.
    :param file_path: Path to the file to check
    :param max_age_days: Maximum allowed age of the file in days
    :return: True if the file exists and is within the allowed age, False otherwise
    """
    if os.path.exists(file_path):  # Check if the file exists
        file_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_path))).days
        return file_age_days < max_age_days  # Return True if the file is not too old
    return False  # Return False if the file does not exist

# Function to add the document to the vector store
def add_to_vector_store(file_path, chunk_size=2000):
    """
    Adds the content of the specified text file to the vector store after splitting it into chunks.
    :param file_path: Path to the text file to add
    :param chunk_size: Size of each chunk to split the document into
    """
    logger.debug("Begin function add_to_vector_store")
    with open(file_path, "r", encoding="utf-8") as f:
        document = f.read()  # Read the entire document into memory
    logger.info("Split the document into chunks")

    # Split the document into chunks of specified size
    chunks = [document[i:i + chunk_size] for i in range(0, len(document), chunk_size)]
    ids = [f"C-70_E_{i+1}" for i in range(len(chunks))]  # Generate unique IDs for each chunk

    logger.debug(f"Chunking document into {len(chunks)} chunks.")
    add_documents(chunks, ids=ids)  # Add the chunks to the vector store with their corresponding IDs

# Main function that orchestrates the workflow
if __name__ == "__main__":
    # Check if the text file is valid (exists and is not too old)
    if not is_text_file_valid(TEXT_FILE_PATH, MAX_FILE_AGE_DAYS):
        run_extractor()  # Extract data if the file is not valid
        add_to_vector_store(TEXT_FILE_PATH, CHUNK_SIZE)  # Add the extracted data to the vector store
    else:
        logger.info("C-70_E.txt is valid. No need to download and parse.")

    run_analysis()  # Run AI analysis regardless of whether the text file was updated
