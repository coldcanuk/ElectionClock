import os
import json

# Directory paths
project_root = os.path.dirname(os.path.dirname(__file__))
taillings_dir = os.path.join(project_root, "extractors/taillings")
html_output_dir = os.path.join(project_root, "templates")

def generate_analysis_html(analysis_file, bill_name):
    # Create the lists for use in creating the HTML
    listCollIndi = []
    listPhilo = []
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
                    # Extract Borg
                    borg_analysis = parsed_data['Analysis']['Borg_Collective_Analysis']
                    ind_analysis = parsed_data['Analysis']['Individual_Heart_Analysis']
                    list(listCollIndi).append(
                      {
                        'Cscore': borg_analysis['Score'],
                        'Cexplanation': borg_analysis['Explanation'],
                        'Iscore': ind_analysis['Score'],
                        'Iexplanation': ind_analysis['Explanation'] 
                      }
                    )
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
        <!-- version marker 3 -->
        <div class="analysis-content">
            <h2>{bill_name} Analysis</h2>
            <!-- Dynamically insert analysis text -->
            {generate_html_for_coll_indi(listCollIndi)}
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
    
def generate_html_for_coll_indi(analyses):
    html_parts = []
    for index, analysis in enumerate(analyses, start=1):
        html_parts.append(f"""
            <h2>Chunk {index}</h2>
            <h3>The Collective</h3>
            <p><strong>Score:</strong> {analysis['Cscore']}</p>
            <p><strong>Explanation:</strong> {analysis['Cexplanation']}</p>
            <h3>The Individual</h3>
            <p><strong>Score:</strong> {analysis['Iscore']}</p>
            <p><strong>Explanation:</strong> {analysis['Iexplanation']}</p>
        """)
    return ''.join(html_parts)

if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.json")
    generate_analysis_html(analysis_file_path, "C-70_E")
