# app.py
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from auth import require_auth
from quants.tsionhehkwen import get_analysis_results, add_analysis_results
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

# Add a check for permission errors
try:
    logging.basicConfig(
        filename=log_file,
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=log_level
    )
except PermissionError as e:
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=log_level
    )
    logging.warning(f"PermissionError encountered with logging to file {log_file}: {e}")

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

@app.route('/get_analysis', methods=['GET'])
@require_auth
def get_analysis():
    query = request.args.get("query", "C-70_E_Analysis")
    results = get_analysis_results(query, n_results=1)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
