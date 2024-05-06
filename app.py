from flask import Flask, render_template
from datetime import datetime
import pytz
import os
import logging
import sys

app = Flask(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't', 'y')
log_level = "DEBUG" if DEBUG_MODE else "INFO"

log_dir = '/var/log/countdownapp/'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    filename=log_file,
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=log_level
)

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.info("***BEGIN app.py****")

elections = {
    'federal': '2025-10-19',
}

@app.route('/')
def countdown():
    now = datetime.now(pytz.timezone('America/Toronto'))
    next_election_date = datetime.strptime(elections['federal'], '%Y-%m-%d')
    next_election_date = pytz.timezone('America/Toronto').localize(next_election_date)
    time_left = next_election_date - now
    return render_template('countdown.html', time_left=time_left, election_date=next_election_date)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
