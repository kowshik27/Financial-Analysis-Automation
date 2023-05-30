from flask import Flask, render_template, request, redirect, url_for
from financial_analysis import financial_analysis_reports

import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/automated-analysis', methods=['POST'])
def automated_analysis():
    user_email = request.form['email']
    financial_analysis_reports(user_email)
    time.sleep(20)
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('delivered.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
