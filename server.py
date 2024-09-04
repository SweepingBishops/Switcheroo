from flask import Flask, render_template, redirect, url_for, request, session, flash
import json
import time

app = Flask(__name__)
app.secret_key = "Zucc"

with open('static/questions.json', 'r') as file:
    questions = json.load(file)

def set_attempts():
    attempts = {}
    for team in users_data:
        attempts[team] = {}
        for i in range(1, len(questions)+1):
            attempts[team][i] = [0,False]
    return attempts

def update_stats(team_name, question):
    current_time = time.localtime()
    time_str = time.strftime("%H:%M:%S", current_time)
    record = f"{team_name} solved Question {question} at {time_str}\n"

    stats_data[team_name][question][1] = True
    update_attempt(stats_data)
    with open('static/stats.csv', 'a') as file:
        file.write(record)



def update_attempt(stats_data):
    with open('static/attempts.json', 'w') as file:
        json.dump(stats_data, file, indent=4)

with open('static/users.json',  'r') as file:
    users_data = json.load(file)


stats_data = set_attempts()
update_attempt(stats_data)
TOTAL_ATTEMPTS = 3

@app.route('/')
def index():
    if 'team_name' in session:
        return render_template('index.html', questions=questions, team_name=session['team_name'], stats_data=stats_data)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        password = request.form.get('password')

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
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    question_data = questions[question_id]
    team_name = session['team_name']
    attempt = stats_data[team_name][(question_id+1)][0]
    solved = stats_data[team_name][(question_id+1)][1]
    # print(attempt)
    if request.method == 'POST':
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
            print(f'attempts: {attempt}')
            return render_template('ans_wrong.html', attempt=TOTAL_ATTEMPTS-attempt-1)

    if solved:
        return render_template('freeze.html', title_message=f"You have already solved Question {question_id+1}")

    if attempt >= TOTAL_ATTEMPTS:
            return render_template('freeze.html', title_message=f"You have exhausted all your attempts for Question {question_id+1}", freeze_message = f"You've attempted this question {attempt} times")
            
    return render_template('question.html', question_data=question_data, attempt=TOTAL_ATTEMPTS-attempt)


app.run(host = "0.0.0.0",port = 5000, debug=True)
