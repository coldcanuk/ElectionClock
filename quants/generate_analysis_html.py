import os
import json
import sys
from loguru import logger
from dotenv import load_dotenv

# Load environment variables from the .env file
env_path = os.getenv('HOME') + "/web/ElectionClockEnvironment/.env"
load_dotenv(dotenv_path=env_path)

# Check if the application is running in debug mode
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger for console output
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin apollo")
logger.debug("Debug mode on")

# Directory paths for input and output files
project_root = os.path.dirname(os.path.dirname(__file__))
taillings_dir = os.path.join(project_root, "extractors/taillings")
html_output_dir = os.path.join(project_root, "templates")

# Function to generate an HTML file from the AI analysis JSON
def generate_analysis_html(analysis_file, bill_name):
    """
    Generates an HTML file based on AI analysis results stored in a JSON file.
    :param analysis_file: Path to the JSON file containing the analysis results.
    :param bill_name: The name of the bill or document being analyzed.
    """
    listKeikoAnalysis = []
    listCollIndi = []
    listPhilo = []

    try:
        with open(analysis_file, "r", encoding="utf-8") as file:
            analysis_content = json.load(file)  # Load the JSON data from the file

        # Process each analysis result
        for key, value in analysis_content.items():
            if isinstance(value['text'], list):
                logger.debug("Matched a list in the analysis results")
                json_data_str = value['text'][0]['text']['value']
                try:
                    # Parse the string value to actual JSON
                    json_data = json.loads(json_data_str)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON from 'value': {e}")
                    continue

                analysis = json_data.get('Analysis', {})
                for topic, details in analysis.items():
                    if topic in ["Individual_Heart_Analysis", "Borg_Collective_Analysis"]:
                        logger.debug(f"Processing {topic}")
                        listCollIndi.append({
                            'Topic': topic,
                            'Score': details.get('Score'),
                            'Explanation': details.get('Explanation')
                        })
                    else:
                        logger.debug(f"Adding topic to listKeikoAnalysis: {topic}")
                        listKeikoAnalysis.append({topic: details})

                # Extract Philosopher Perspectives
                philosopher_perspectives = json_data.get('Philosopher_Perspectives', [])
                for perspective in philosopher_perspectives:
                    philosopher = perspective.get('Philosopher')
                    perspective_text = perspective.get('Perspective')
                    listPhilo.append(
                        {
                            'Philosopher': philosopher,
                            'Perspective': perspective_text
                        }
                    )
    except Exception as e:
        logger.error(f"Error reading or processing analysis file: {e}")
        return

    # Create HTML content using the processed data
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
        <title>{bill_name} AI Analysis</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <div class="countdown-container">
            <h2 class="countdown-text">Until the Next Canadian Federal Election:</h2>
            <div id="countdown-timer"></div>
        </div>
        <div class="analysis-content">
            <h2>{bill_name} Analysis</h2>
            {generate_html_for_keiko_analysis(listKeikoAnalysis)}
            {generate_html_for_coll_indi(listCollIndi)}
            {generate_html_for_coll_phil(listPhilo)}
        </div>
        <script>
            // Countdown timer script
        </script>
    </body>
    </html>
    """
    output_file = os.path.join(html_output_dir, f"{bill_name}_analysis.html")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)
    print(f"Generated HTML file: {output_file}")

# Function to generate HTML for Keiko's analysis
def generate_html_for_keiko_analysis(analyses):
    """
    Generates HTML for Keiko's analysis results.
    :param analyses: List of Keiko's analysis results.
    :return: HTML content as a string.
    """
    html_parts = []
    for analysis in analyses:
        for topic, content in analysis.items():
            if isinstance(content, dict) and topic == "Details":
                html_parts.append("<div class='analysis-section'><h2>Details</h2>")
                for part, info in content.items():
                    html_parts.append(f"<h3>{part}</h3><ul>")
                    if isinstance(info, dict) and 'Amendments' in info:
                        for amendment in info['Amendments']:
                            html_parts.append("<li>")
                            for key, value in amendment.items():
                                html_parts.append(f"<strong>{key}:</strong> {value} ")
                            html_parts.append("</li>")
                    html_parts.append("</ul>")
                html_parts.append("</div>")
            elif isinstance(content, str):
                html_parts.append(f"""
                  <div class="analysis-section">
                    <h2>{topic}</h2>
                    <p>{content}</p>
                  </div>
                """)
            else:
                html_parts.append(f"""
                  <div class="analysis-section">
                    <h2>{topic}</h2>
                    <p>Content not displayed properly</p>
                  </div>
                """)
    return ''.join(html_parts) if html_parts else "<p>No additional analysis provided.</p>"

# Function to generate HTML for collective and individual analyses
def generate_html_for_coll_indi(analyses):
    """
    Generates HTML for collective and individual impact analyses.
    :param analyses: List of collective and individual analyses.
    :return: HTML content as a string.
    """
    html_parts = []
    for analysis in analyses:
        if analysis['Topic'] == "Borg_Collective_Analysis":
            html_parts.append(f"""
              <h2>Collective Impact Analysis</h2>
              <h3>The Collective Score: {analysis['Score']}</h3>
              <p><strong>Explanation:</strong> {analysis['Explanation']}</p>
            """)
        elif analysis['Topic'] == "Individual_Heart_Analysis":
            html_parts.append(f"""
              <h2>Individual Impact Analysis</h2>
              <h3>The Individual Score: {analysis['Score']}</h3>
              <p><strong>Explanation:</strong> {analysis['Explanation']}</p>
            """)
    return ''.join(html_parts) if html_parts else "<p>No impact analysis provided.</p>"

# Function to generate HTML for philosopher perspectives
def generate_html_for_coll_phil(analyses):
    """
    Generates HTML for philosopher perspectives.
    :param analyses: List of philosopher perspectives.
    :return: HTML content as a string.
    """
    html_parts = [f"<h3>Philosophers:</h3>"]
    for analysis in analyses:
        html_parts.append(f"""
            <p><strong>{analysis['Philosopher']}: {analysis['Perspective']}</strong></p>
        """)
    return ''.join(html_parts) if html_parts else "<p>No philosopher perspectives provided.</p>"

# Main function to generate HTML based on the analysis JSON file
if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.json")
    generate_analysis_html(analysis_file_path, "C-70_E")
