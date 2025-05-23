
from flask import Flask, render_template, request, redirect, session, url_for
import os
import dummy_data

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    return render_template('index.html', metrics=dummy_data.metrics)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if request.form['passcode'] == 'secure123':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "<h3>Incorrect passcode. Try again.</h3>"
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
