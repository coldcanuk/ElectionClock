import os
import json

# Directory paths
project_root = os.path.dirname(os.path.dirname(__file__))
taillings_dir = os.path.join(project_root, "extractors/taillings")
html_output_dir = os.path.join(project_root, "templates")
print(f"The project root directory is: {project_root}")

# Utility function to read analysis file and generate HTML
def generate_analysis_html(analysis_file, bill_name):
    # Read analysis text content
    try:
        with open(analysis_file, "r", encoding="utf-8") as file:
            analysis_content = file.read()
        
        # Extract JSON-like content
        start = analysis_content.find("{")
        end = analysis_content.rfind("}") + 1
        analysis_json_content = analysis_content[start:end]
        
        try:
            analysis_data = json.loads(analysis_json_content.replace("\'", "\""))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    except Exception as e:
        print(f"Error reading analysis file: {e}")
        return

    # Extract data
    keiko = analysis_data.get("KEIKO", "")
    analysis = analysis_data.get("Analysis", {})
    part1 = analysis.get("Part 1", {})
    part2 = analysis.get("Part 2", {})
    philosophies = analysis_data.get("Philosophical Perspectives", {})

    individual_heart_score_1 = part1.get("Individual_Heart Score Analysis", {}).get("Score", "")
    individual_heart_explanation_1 = part1.get("Individual_Heart Score Analysis", {}).get("Explanation", "")

    borg_collective_score_1 = part1.get("Borg_Collective Score Analysis", {}).get("Score", "")
    borg_collective_explanation_1 = part1.get("Borg_Collective Score Analysis", {}).get("Explanation", "")

    individual_heart_score_2 = part2.get("Individual_Heart Score Analysis", {}).get("Score", "")
    individual_heart_explanation_2 = part2.get("Individual_Heart Score Analysis", {}).get("Explanation", "")

    borg_collective_score_2 = part2.get("Borg_Collective Score Analysis", {}).get("Score", "")
    borg_collective_explanation_2 = part2.get("Borg_Collective Score Analysis", {}).get("Explanation", "")

    ayn_rand = philosophies.get("Ayn Rand", "")
    thomas_sowell = philosophies.get("Thomas Sowell", "")

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
                <h2>Countering Foreign Interference Act 2024 Analysis</h2>
                <h3>Overview:</h3>
                <p>{keiko}</p>
                <h3>Part 1 Analysis:</h3>
                <p><strong>Individual Heart Score:</strong> {individual_heart_score_1}</p>
                <p>{individual_heart_explanation_1}</p>
                <p><strong>Borg Collective Score:</strong> {borg_collective_score_1}</p>
                <p>{borg_collective_explanation_1}</p>
                <h3>Part 2 Analysis:</h3>
                <p><strong>Individual Heart Score:</strong> {individual_heart_score_2}</p>
                <p>{individual_heart_explanation_2}</p>
                <p><strong>Borg Collective Score:</strong> {borg_collective_score_2}</p>
                <p>{borg_collective_explanation_2}</p>
                <h3>Philosophical Perspectives:</h3>
                <p><strong>Ayn Rand:</strong> {ayn_rand}</p>
                <p><strong>Thomas Sowell:</strong> {thomas_sowell}</p>
            </div>
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

                    console.log(`Drawing {label}:`, Math.floor(value), `at ({x},{y})`);

                    $r.ctx.save();
                    $r.ctx.translate(x, y);
                    $r.ctx.clearRect($r.actual_size * -0.5, $r.actual_size * -0.5, $r.actual_size, $r.actual_size);

                    // first circle (background)
                    $r.ctx.strokeStyle = "rgba(200, 200, 200, 0.3)";
                    $r.ctx.beginPath();
                    $r.ctx.arc(0, 0, $r.r_size / 2, 0, 2 * Math.PI, true);
                    $r.ctx.lineWidth = $r.r_thickness;
                    $r.ctx.stroke();

                    // second circle (progress)
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

    # Output HTML file path
    output_file = os.path.join(html_output_dir, f"{bill_name}_analysis.html")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)

    print(f"Generated HTML file: {output_file}")

# Example usage
if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.txt")
    generate_analysis_html(analysis_file_path, "C-70_E")
