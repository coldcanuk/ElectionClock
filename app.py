from flask import Flask, render_template
from datetime import datetime
import pytz
import sys
import os
import logging
from loguru import logger  # Loguru is a library for easier logging in Python

app = Flask(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
# Set the logging level based on whether the application is in debug mode
log_level = "DEBUG" if DEBUG_MODE else "INFO"

# Create a directory for logs if it doesn't exist
log_dir = '/var/log/countdownapp/'
os.makedirs(log_dir, exist_ok=True)

# Configure the log file path
log_file = os.path.join(log_dir, 'app.log')

# Configure logging
logging.basicConfig(
    filename=log_file,
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=log_level
)

# Add a standard output handler with the newly set log level
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Log a message to indicate the application startup
logging.info("****BEGIN app.py*****")

elections = {
    'federal': '2025-10-19',
}

@app.route('/')
def countdown():
    now = datetime.now(pytz.timezone('America/Toronto'))
    next_election_date = datetime.strptime(elections['federal'], '%Y-%m-%d')
    next_election_date = pytz.timezone('America/Toronto').localize(next_election_date)
    time_left = next_election_date - now
    return render_template('countdown.html', time_left=time_left)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)