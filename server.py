#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request, session, flash
import json
import time
from os.path import isfile
from hashlib import sha256

app = Flask(__name__)
app.secret_key = "Zucc"

CONFIG_FILE = 'static/config.json'
with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)
    TOTAL_ATTEMPTS = config['total_attempts']
    ATTEMPTS_FILE = config['attempts_file']
    STATS_FILE = config['stats_file']
    USERS_FILE = config['users_file']
    QUESTIONS_FILE = config['questions_file']

with open(QUESTIONS_FILE, 'r') as file:
    questions = json.load(file)

def set_attempts():
    attempts = {}
    for team in users_data:
        attempts[team] = dict()
        for i in range(1, len(questions)+1):
            attempts[team][i] = [0,False]
    return attempts

def update_stats(team_name, question):
    current_time = time.localtime()
    time_str = time.strftime("%H:%M:%S", current_time)
    record = f"{team_name} solved Question {question} at {time_str}\n"

    stats_data[team_name][question][1] = True
    stats_data[team_name][question].append(time_str)
    update_attempt(stats_data)
    with open(STATS_FILE, 'a') as file:
        file.write(record)

def update_attempt(stats_data):
    with open(ATTEMPTS_FILE, 'w') as file:
        json.dump(stats_data, file, indent=4)

with open(USERS_FILE,  'r') as file:
    users_data = json.load(file)


if isfile(ATTEMPTS_FILE):
    with open(ATTEMPTS_FILE, 'r') as file:
        stats_data = {k:{int(k1):v1 for k1,v1 in v.items()} for k,v in json.load(file).items()}
else:
    stats_data = set_attempts()
    update_attempt(stats_data)

timer_running = True

@app.route('/toggle_timer', methods=['GET', 'POST'])
def toggle_timer():
    global timer_running
    if 'admin_name' in session:
        timer_running = not timer_running
        if timer_running:
            flash('Timer started!', 'success')
        else:
            flash('Timer paused!', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/')
def index():
    if 'team_name' in session:
        if timer_running:
            return render_template('index.html', questions=questions, team_name=session['team_name'], stats_data=stats_data, TOTAL_ATTEMPTS = TOTAL_ATTEMPTS)
    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        password = request.form.get('password')
        password = sha256(password.encode('utf-8')).hexdigest()

        if team_name in users_data and password == users_data[team_name]:
            session['team_name'] = team_name
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid team name or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('team_name', None)
    session.pop('admin_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Admin user
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        password = request.form.get('password')
        password = sha256(password.encode('utf-8')).hexdigest()

        if admin_name == 'admin' and password == users_data[admin_name]:
            session['admin_name'] = admin_name
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials. Please try again.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_name' in session:
        return render_template('admin_dashboard.html', stats_data=stats_data, questions=questions, timer_running=timer_running)
    else:
        flash('Please login as an admin to access the dashboard.', 'danger')
        return redirect(url_for('login'))

@app.before_request
def restrict_admin_routes():
    if request.endpoint in ['admin_dashboard', 'start_timer', 'pause_timer', 'reset_timer'] and 'admin_name' not in session:
        return redirect(url_for('login'))
    
@app.before_request
def freeze_website_on_timer_pause():
    if not timer_running and 'admin_name' not in session and request.endpoint not in ['login','admin_login']:
        return redirect(url_for('login'))

@app.route('/resources/<int:question_id>', methods=['GET', 'POST'])
def resources(question_id):
    if not timer_running:
        return redirect(url_for('login'))

    if 'team_name' not in session:
        return redirect(url_for('login'))
    question_data = questions[question_id]

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if not timer_running:
        return redirect(url_for('login'))

    if 'team_name' not in session:
        return redirect(url_for('login'))
    question_data = questions[question_id]
    team_name = session['team_name']
    attempt = stats_data[team_name][(question_id+1)][0]
    solved = stats_data[team_name][(question_id+1)][1]
    # print(attempt)
    if request.method == 'POST':
        if not timer_running:
            return redirect(url_for('login'))
        stats_data[team_name][(question_id+1)][0] = attempt + 1
        update_attempt(stats_data)
        user_answer = (request.form.get('answer'))
        correct_answer = question_data['answer']        
        # stats_data[session['team_name']] = {question_id: attempt}
        if user_answer == correct_answer and attempt < TOTAL_ATTEMPTS:
            # update_score(team_name,question_id+1)
            update_stats(team_name, question_id+1) # The +1 is for changing the index to question number
            return render_template('ans_correct.html')
        else:
            # print(f'attempts: {attempt}')
            return render_template('ans_wrong.html', attempt=TOTAL_ATTEMPTS-attempt-1)

    if solved:
        return render_template('freeze.html', title_message=f"You have already solved Question {question_id+1}")

    if attempt >= TOTAL_ATTEMPTS:
            return render_template('freeze.html', title_message=f"You have exhausted all your attempts for Question {question_id+1}", freeze_message = f"You've attempted this question {attempt} times")
    return render_template('question.html', question_data=question_data, attempt=TOTAL_ATTEMPTS-attempt)


app.run(host = "0.0.0.0",port = 4000, debug=False)
