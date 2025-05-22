
from flask import Flask, render_template, redirect, url_for, request, session
from login import check_login
from dummy_data import metrics, location_data, funnel_data
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
    selected_location = request.args.get('location', 'All')
    time_range = request.args.get('range', 'Weekly')
    loc_data = location_data.get(selected_location, location_data['All'])
    return render_template('dashboard.html', metrics=metrics, funnel_data=funnel_data,
                           location_data=loc_data, selected_location=selected_location,
                           locations=location_data.keys(), time_range=time_range)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
