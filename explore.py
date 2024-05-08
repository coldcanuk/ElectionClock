import os
import sys
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# Ensure the project root is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from the .env file
load_dotenv()

# Retrieve OpenAI API Key
openai_api_key = os.getenv("keyOPENAI")
if not openai_api_key:
    raise ValueError("Please provide an OpenAI API key in the .env file with key 'keyOPENAI'.")

# Ensure the vector store directory exists
vector_store_directory = "quants/vector_store"
os.makedirs(vector_store_directory, exist_ok=True)

# Initialize the ChromaDB client with disk persistence
client = chromadb.PersistentClient(path=vector_store_directory)

# Use OpenAI's `text-embedding-ada-002` model
embedding_function = OpenAIEmbeddingFunction(api_key=openai_api_key, model_name="text-embedding-ada-002")

# Retrieve or create the collection
collection = client.get_or_create_collection(
    name="Tsionhehkwen",
    embedding_function=embedding_function
)

# Function to show all documents
def show_all_documents(collection):
    documents = collection.get()
    if not documents["documents"]:
        print("No documents found in the collection.")
        return
    for i, (doc_id, document) in enumerate(zip(documents["ids"], documents["documents"]), 1):
        print(f"\n{i}. ID: {doc_id}\nContent:\n{document}\n")

# Function to delete all documents
def delete_all_documents(collection):
    ids_to_delete = collection.get()["ids"]
    collection.delete(ids=ids_to_delete)
    
    # Verify if deletion was successful
    remaining_ids = collection.get()["ids"]
    if not remaining_ids:
        print("All documents deleted successfully.")
    else:
        print(f"Warning: Some documents could not be deleted. Remaining IDs: {remaining_ids}")

# Function to explore the collection
def explore_collection(collection):
    while True:
        print("\n--- Tsionhehkwen Vector Store Explorer ---")
        print("1. Show all documents")
        print("2. List document IDs")
        print("3. Retrieve a specific document")
        print("4. Search documents")
        print("5. Delete all documents")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_all_documents(collection)
        elif choice == "2":
            documents = collection.peek()
            print("Documents in Collection:")
            for i, doc_id in enumerate(documents["ids"], 1):
                print(f"{i}. {doc_id}")
        elif choice == "3":
            doc_id = input("Enter a document ID to retrieve: ").strip()
            if doc_id:
                document = collection.get(ids=[doc_id])
                if document["documents"]:
                    print(f"\nDocument Content ({doc_id}):\n{document['documents'][0]}")
                else:
                    print(f"No document found with ID: {doc_id}")
        elif choice == "4":
            query = input("Enter a search query: ").strip()
            if query:
                results = collection.query(query_texts=[query], n_results=5)
                print(f"\nSearch Results for '{query}':")
                for i, doc in enumerate(results["documents"], 1):
                    print(f"{i}. {doc}")
        elif choice == "5":
            confirm = input("Are you sure you want to delete all documents? (yes/no): ").strip().lower()
            if confirm == "yes":
                delete_all_documents(collection)
            else:
                print("Deletion canceled.")
        elif choice == "6":
            print("Exiting Tsionhehkwen Vector Store Explorer.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    explore_collection(collection)
