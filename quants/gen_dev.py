import os
import json

# Directory paths
project_root = os.path.dirname(os.path.dirname(__file__))
taillings_dir = os.path.join(project_root, "extractors/taillings")
html_output_dir = os.path.join(project_root, "templates")

def generate_analysis_html(analysis_file, bill_name):
    analyses = []  # List to store all analyses
    try:
        with open(analysis_file, "r", encoding="utf-8") as file:
            analysis_content = json.load(file)  # Directly load the JSON data

        # Assuming 'text' contains nested JSON that needs to be interpreted as such
        for key, value in analysis_content.items():
            if isinstance(value['text'], list):
                # Assuming the desired content is always the first item in the list
                # Print the problematic JSON string for debugging
                json_str = value['text'][0]['text']['value']
                print("JSON string before parsing:", json_str)
                try:
                    # Parse the inner JSON string
                    parsed_data = json.loads(json_str)
                    # Extract the specific data you need for the HTML
                    borg_analysis = parsed_data['Analysis']['Borg_Collective_Analysis']
                    analyses.append({
                        'score': borg_analysis['Score'],
                        'explanation': borg_analysis['Explanation']
                    })
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    continue
    except Exception as e:
        print(f"Error reading or processing analysis file: {e}")
        return

    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
        <title>{bill_name} Analysis</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <div class="countdown-container">
            <h2>{bill_name} Analysis</h2>
            {generate_html_for_analyses(analyses)}
        </div>
    </body>
    </html>
    """

    output_file = os.path.join(html_output_dir, f"{bill_name}_analysis.html")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)
    print(f"Generated HTML file: {output_file}")
    
def generate_html_for_analyses(analyses):
    html_parts = []
    for index, analysis in enumerate(analyses, start=1):
        html_parts.append(f"""
            <h2>Chunk {index}</h2>
            <p><strong>Score:</strong> {analysis['score']}</p>
            <p><strong>Explanation:</strong> {analysis['explanation']}</p>
        """)
    return ''.join(html_parts)

if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.json")
    generate_analysis_html(analysis_file_path, "C-70_E")
