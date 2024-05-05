from flask import Flask, render_template
from datetime import datetime
import pytz
import sys
import os
from dotenv import load_dotenv
from loguru import logger  # Loguru is a library for easier logging in Python

app = Flask(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
# Set the logging level based on whether the application is in debug mode
log_level = "DEBUG" if DEBUG_MODE else "INFO"
# Remove all handlers associated with the logger
logger.remove()
# Re-add a standard output handler with the newly set log level
logger.add(sys.stdout, level=log_level)
logger.debug("***BEGIN app.py****")

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
    app.run(debug=True)
