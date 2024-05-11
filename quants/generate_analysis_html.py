import os
import json

# Directory paths
project_root = os.path.dirname(os.path.dirname(__file__))
taillings_dir = os.path.join(project_root, "extractors/taillings")
html_output_dir = os.path.join(project_root, "templates")

def generate_analysis_html(analysis_file, bill_name):
    try:
        with open(analysis_file, "r", encoding="utf-8") as file:
            analysis_content = json.load(file)  # Directly load the JSON data

        # Assuming 'text' contains nested JSON that needs to be interpreted as such
        for key, value in analysis_content.items():
            if isinstance(value['text'], str):
                value['text'] = json.loads(value['text'])

        # Use 'value['text']' directly in HTML generation below

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
            <div id="countdown-timer">
                <div class="ring">Months</div>
                <div class="ring">Days</div>
                <div class="ring">Hours</div>
                <div class="ring">Minutes</div>
                <div class="ring">Seconds</div>
                <div class="ring">Milliseconds</div>
            </div>
            <div class="analysis-content">
                <h2>{bill_name} Analysis</h2>
                {value['text']}  <!-- Dynamically insert analysis text -->
            </div>
        </div>
        <script>
            // JavaScript for countdown timer (as previously defined)
        </script>
    </body>
    </html>
    """

    output_file = os.path.join(html_output_dir, f"{bill_name}_analysis.html")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)
    print(f"Generated HTML file: {output_file}")

if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.json")
    generate_analysis_html(analysis_file_path, "C-70_E")
