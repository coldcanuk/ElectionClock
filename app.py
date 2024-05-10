# app.py
from flask import Flask, render_template, jsonify, request, send_from_directory
from datetime import datetime
from auth import require_auth
from quants.tsionhehkwen import get_analysis_results, add_documents, add_analysis_results
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

@app.route('/analyze', methods=['POST'])
@require_auth
def analyze_document():
    data = request.get_json()
    document = data.get("document")
    document_id = data.get("document_id")
    if not document or not document_id:
        return jsonify({"error": "Missing document or document_id"}), 400
    add_documents([document], ids=[document_id])
    return jsonify({"status": "Document added"}), 200

@app.route('/get_analysis', methods=['GET'])
@require_auth
def get_analysis():
    query = request.args.get("query", "C-70_E_Analysis")
    results = get_analysis_results(query, n_results=1)
    return jsonify(results)

@app.route('/<page_name>.html')
def serve_analysis_page(page_name):
    # Serve dynamically generated analysis HTML pages
    try:
        return render_template(f"{page_name}.html")
    except Exception as e:
        return jsonify({"error": f"Page not found: {e}"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
