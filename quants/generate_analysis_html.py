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

                    console.log('Drawing ' + label + ':', Math.floor(value), 'at (' + x + ',' + y + ')');

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

    # Output HTML file path
    output_file = os.path.join(html_output_dir, f"{bill_name}_analysis.html")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)

    print(f"Generated HTML file: {output_file}")

# Example usage
if __name__ == "__main__":
    analysis_file_path = os.path.join(taillings_dir, "C-70_E_analysis.txt")
    generate_analysis_html(analysis_file_path, "C-70_E")
