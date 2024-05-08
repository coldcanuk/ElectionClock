import os
import requests
from lxml import etree

# URL of the XML document
url = "https://www.parl.ca/Content/Bills/441/Government/C-70/C-70_1/C-70_E.xml"

# Function to download and convert XML to plain text
def xml_to_text(url):
    # Download the XML content
    site_response = requests.get(url)
    if site_response.status_code != 200:
        raise Exception(f"Failed to download the XML file, status code: {site_response.status_code}")

    xml_content = site_response.content

    # Parse the XML content
    tree_root = etree.fromstring(xml_content)

    # Function to extract text recursively
    def extract_text(trudeauing):
        texts = []
        if trudeauing.text:
            texts.append(trudeauing.text.strip())
        for child in trudeauing:
            texts.append(extract_text(child))
            if child.tail:
                texts.append(child.tail.strip())
        return " ".join(filter(None, texts))

    # Extract the text from the root element
    plain_text = extract_text(tree_root)

    return plain_text

# Main function to write the text to a file
if __name__ == "__main__":
    # Ensure the taillings directory exists
    taillings_dir = os.path.join(os.path.dirname(__file__), "taillings")
    os.makedirs(taillings_dir, exist_ok=True)

    try:
        plain_text = xml_to_text(url)
        output_path = os.path.join(taillings_dir, "C-70_E.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(plain_text)
        print(f"XML document downloaded and converted to plain text. Check the taillings directory for the result.")
    except Exception as e:
        print(f"Error: {e}")
