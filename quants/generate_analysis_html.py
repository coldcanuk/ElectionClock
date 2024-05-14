import os
import json
import sys
from loguru import logger
from dotenv import load_dotenv
# Load environment variables from the .env file
env_path = os.getenv('HOME') + "/web/ElectionClockEnvironment/.env"
load_dotenv(dotenv_path=env_path)
# Debug mode check
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Set up logger
logger.remove()
logger.add(sys.stdout, level=log_level)
logger.info("Begin apollo")
logger.debug("Debug mode on")


# Directory paths
project_root = os.path.dirname(os.path.dirname(__file__))
taillings_dir = os.path.join(project_root, "extractors/taillings")
html_output_dir = os.path.join(project_root, "templates")

def generate_analysis_html(analysis_file, bill_name):
    listKeikoAnalysis = []
    listCollIndi = []
    listPhilo = []

    try:
        with open(analysis_file, "r", encoding="utf-8") as file:
            analysis_content = json.load(file)  # Directly load the JSON data

        for key, value in analysis_content.items():
            if isinstance(value['text'], list):
                logger.debug("Made match and we are a list")
                json_data_str = value['text'][0]['text']['value']
                try:
                    # Here we parse the string value to actual JSON
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
                        logger.debug(f"Adding topic to listCollAnalysis: {topic}")
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

# Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <!-- version marker 22 -->
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
        
            <!-- Twitter and GitHub Buttons -->
            <div class="button-container">
                <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-show-count="false">Tweet</a>
                <iframe src="https://ghbtns.com/github-btn.html?user=coldcanuk&repo=ElectionClock&type=star&count=true&size=large"
                        frameborder="0" scrolling="0" width="170" height="30"></iframe>
                <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            </div>
            <!-- Text Header -->
            <h2 class="countdown-text">Until the Next Canadian Federal Election:</h2>
            <!-- Ring Countdown Timer -->
            <div id="countdown-timer"></div>   
   
        </div>
        <!-- Keiko's content analysis -->
        
        <div class="analysis-content">
            <h2>{bill_name} Analysis</h2>
            <!-- Dynamically insert first portions of Keiko's output -->
            {generate_html_for_keiko_analysis(listKeikoAnalysis)}
            <!-- Dynamically insert analysis text -->
            {generate_html_for_coll_indi(listCollIndi)}
            <!-- Dynamically insert philospher opinions-->
            {generate_html_for_coll_phil(listPhilo)}
        </div> 
        
        <script>
            var ringer = {{
                countdown_to: "10/19/2025", // Target election date
                rings: {{
                    'MONTHS': {{ s: 2628000000, max: 12 }},
                    'DAYS': {{ s: 86400000, max: 7 }},
                    'HOURS': {{ s: 3600000, max: 24 }},
                    'MINUTES': {{ s: 60000, max: 60 }},
                    'SECONDS': {{ s: 1000, max: 60 }},
                    'MILLISEC': {{ s: 10, max: 100 }}
                }},
                r_count: 7,
                r_spacing: 16,
                r_size: 100,
                r_thickness: 5,
                update_interval: 22,

                init: function () {{
                    var $r = this;
                    $r.cvs = document.createElement('canvas');
                    $r.size = {{
                        w: ($r.r_size + $r.r_thickness) * $r.r_count + ($r.r_spacing * ($r.r_count - 1)),
                        h: ($r.r_size + $r.r_thickness)
                    }};
                    $r.cvs.setAttribute('width', $r.size.w);
                    $r.cvs.setAttribute('height', $r.size.h);
                    $r.ctx = $r.cvs.getContext('2d');
                    document.getElementById('countdown-timer').appendChild($r.cvs);
                    $r.ctx.textAlign = 'center';
                    $r.actual_size = $r.r_size + $r.r_thickness;
                    $r.countdown_to_time = new Date($r.countdown_to).getTime();
                    console.log("Canvas initialized, size:", $r.size);
                    $r.go();
                }},
                ctx: null,
                go: function () {{
                    var $r = this;
                    var idx = 0;
                    $r.time = ($r.countdown_to_time) - (new Date().getTime());
                    console.log("Time remaining:", $r.time);
                    for (var r_key in $r.rings) $r.unit(idx++, r_key, $r.rings[r_key]);
                    setTimeout($r.go.bind($r), $r.update_interval);
                }},
                unit: function (idx, label, ring) {{
                    var $r = this;
                    var x, y, value, ring_secs = ring.s;
                    value = parseFloat($r.time / ring_secs);
                    $r.time -= Math.round(parseInt(value)) * ring_secs;
                    value = Math.abs(value);

                    x = ($r.r_size * 0.5 + $r.r_thickness * 0.5) + (idx * ($r.r_size + $r.r_spacing + $r.r_thickness));
                    y = $r.r_size * 0.5 + $r.r_thickness * 0.5;

                    // calculate arc end angle
                    var degrees = 360 - (value / ring.max) * 360.0;
                    var endAngle = degrees * (Math.PI / 180);

                    console.log(`Drawing ${{label}}:`, Math.floor(value), `at (${{x}},${{y}})`);

                    $r.ctx.save();
                    $r.ctx.translate(x, y);
                    $r.ctx.clearRect($r.actual_size * -0.5, $r.actual_size * -0.5, $r.actual_size, $r.actual_size);

                    // first circle (background)
                    $r.ctx.strokeStyle = "rgba(200, 200, 200, 0.3)";
                    $r.ctx.beginPath();
                    $r.ctx.arc(0, 0, $r.r_size / 2, 0, 2 * Math.PI, true);
                    $r.ctx.lineWidth = $r.r_thickness;
                    $r.ctx.stroke();

                    // second circle (progress) - Changed to red
                    $r.ctx.strokeStyle = "rgba(255, 0, 0, 1)";
                    $r.ctx.beginPath();
                    $r.ctx.arc(0, 0, $r.r_size / 2, 0, endAngle, true);
                    $r.ctx.lineWidth = $r.r_thickness;
                    $r.ctx.stroke();

                    // label
                    $r.ctx.fillStyle = "#ffffff";
                    $r.ctx.font = '12px Helvetica';
                    $r.ctx.fillText(label, 0, 23);
                    $r.ctx.font = 'bold 40px Helvetica';
                    $r.ctx.fillText(Math.floor(value), 0, 10);
                    $r.ctx.restore();
                }}
            }}

            // Initialize the Ring Countdown Timer
            ringer.init();
        </script>
    </body>
    </html>
    """
    output_file = os.path.join(html_output_dir, f"{bill_name}_analysis.html")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)
    print(f"Generated HTML file: {output_file}")
#Define the function that generate HTML for Keiko's analysis
def generate_html_for_keiko_analysis(analyses):
    html_parts = []
    for index, analysis in enumerate(analyses, start=0):
        for topic, content in analysis.items():
            if isinstance(content, dict):
                html_parts.append(f"""
                  <div class="analysis-section">
                    <h2>{topic}</h2>
                    <p>{content.get('Overview', 'No overview provided')}</p>
                    <ul>
                    {''.join(f"<li>{change}</li>" for change in content.get('Details', {}).get('Amendments', ['No details provided']))}
                    </ul>
                  </div>
                """)
            else:
                # Handling for string type data like 'Overview'
                html_parts.append(f"""
                  <div class="analysis-section">
                    <h2>{topic}</h2>
                    <p>{content}</p>
                  </div>
                """)
    return ''.join(html_parts) if html_parts else "<p>No additional analysis provided.</p>"

# Define the function that generates HTML for collective and individual analyses
def generate_html_for_coll_indi(analyses):
    html_parts = []
    for index, analysis in enumerate(analyses, start=1):
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
    if len(html_parts) >= 1:
      return ''.join(html_parts)
    else:
      logger.error(f"html_parts has a length of {len(html_parts)}")

      
def generate_html_for_coll_phil(analyses):
    html_parts = []
    html_parts.append(f"""
        <h3>Philosophers:</h3>
        """)
    for index, analysis in enumerate(analyses, start=0):
        html_parts.append(f"""
            <p><strong>{analysis['Philosopher']}: {analysis['Perspective']}</strong></p>
        """)
    if len(html_parts) >= 1:
      return ''.join(html_parts)
    else:
      logger.error(f"html_parts has a length of {len(html_parts)}")

if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.json")
    generate_analysis_html(analysis_file_path, "C-70_E")