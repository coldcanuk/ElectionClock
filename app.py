from flask import Flask, render_template
from datetime import datetime
import pytz

app = Flask(__name__)

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
