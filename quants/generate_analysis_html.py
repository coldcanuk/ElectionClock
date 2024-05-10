# generate_analysis_html.py
import os

# Directory paths
project_root = os.path.dirname(os.path.dirname(__file__))
taillings_dir = os.path.join(project_root, "extractors/taillings")
html_output_dir = os.path.join(project_root, "templates")
print(f"The project root directory is: {project_root}")
# Utility function to read analysis file and generate HTML
def generate_analysis_html(analysis_file, bill_name):
    # Read analysis text content
    with open(analysis_file, "r", encoding="utf-8") as file:
        analysis_content = file.read()

    # Create HTML content based on the layout
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- Make it mobile friendly -->
        <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
        <title>{bill_name} Analysis</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <div class="countdown-container">
            <!-- Countdown Timer -->
            <div id="countdown-timer">
                <div class="ring">Months</div>
                <div class="ring">Days</div>
                <div class="ring">Hours</div>
                <div class="ring">Minutes</div>
                <div class="ring">Seconds</div>
                <div class="ring">Milliseconds</div>
            </div>
            <!-- Analysis Text -->
            <div class="analysis-content">
                {analysis_content}
            </div>
            <!-- Characters and Portraits -->
            <div class="character-content">
                <div class="character-portrait">Portrait of Character</div>
                <div class="character-description">The character's words go here</div>
                <div class="character-portrait">Portrait of Character</div>
                <div class="character-description">The character's words go here</div>
                <div class="character-portrait">Portrait of Character</div>
                <div class="character-description">The character's words go here</div>
                <div class="character-portrait">Portrait of Character</div>
                <div class="character-description">The character's words go here</div>
            </div>
        </div>
    </body>
    </html>
    """

    # Output HTML file path
    output_file = os.path.join(html_output_dir, f"{bill_name}_analysis.html")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)

    print(f"Generated HTML file: {output_file}")

# Example usage
if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.txt")
    generate_analysis_html(analysis_file_path, "C-70_E")