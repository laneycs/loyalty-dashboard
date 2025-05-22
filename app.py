
from flask import Flask, render_template, redirect, url_for, request, session
from login import check_login
from dummy_data import metrics
app = Flask(__name__)
app.secret_key = 'replace_with_a_real_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if check_login(request.form['passcode']):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', metrics=metrics)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
