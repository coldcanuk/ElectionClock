# Quants Directory

This directory contains the key Python scripts responsible for managing the vector store, analyzing documents, and generating HTML reports. Below is a detailed explanation of each file's main job and how it contributes to the overall functionality of the project.

## `apollo.py`

The `apollo.py` script's main job is to analyze text data retrieved from a vector store using OpenAI's API and save the analysis results to a JSON file.

### Key Responsibilities:
- **Environment Setup**: The script loads environment variables and sets up logging based on whether the application is in debug mode.
- **API Configuration**: Retrieves API keys and assistant IDs from environment variables to ensure that critical configuration is available.
- **Text Chunk Analysis**: Retrieves a document from the vector store, splits it into chunks, and sends each chunk to OpenAI for analysis. The results are collected and stored.
- **Custom JSON Encoding**: Handles the serialization of complex objects, allowing the results to be saved in a structured format.
- **File Output**: The analyzed data is saved to a JSON file, which can be used for generating reports or visualizations.

## `tsionhehkwen.py`

The `tsionhehkwen.py` script is responsible for managing the vector store operations, including adding, searching, and retrieving documents and analysis results.

### Key Responsibilities:
- **Environment Setup**: Loads environment variables and configures the logging setup.
- **Vector Store Management**: Initializes the ChromaDB client with disk persistence, ensuring that documents and analysis results can be stored and retrieved efficiently.
- **Document Management**: Provides functions to add documents to the vector store, split documents into chunks for better indexing, and search for documents based on a query.
- **Analysis Management**: Manages the addition and retrieval of analysis results from a dedicated collection in the vector store. It also includes functions to list all stored analysis results and delete them if needed.

## `generate_analysis_html.py`

The `generate_analysis_html.py` script's main job is to generate HTML files based on AI analysis results stored in JSON files, creating a user-friendly display of the data.

### Key Responsibilities:
- **Environment Setup**: Loads environment variables and sets up logging to ensure that the application can run in both debug and production modes.
- **HTML Generation**: Reads AI analysis results from a JSON file, processes the data, and generates structured HTML content. The content is saved to a file in the `templates` directory, making it ready for web presentation.
- **Data Processing**: The script processes various types of analysis results, including Keiko’s analysis, collective and individual impact analyses, and philosopher perspectives, formatting them into readable and organized HTML sections.
