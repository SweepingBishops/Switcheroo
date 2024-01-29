from flask import Flask, render_template, redirect, url_for, request, session, flash
import json
import time

app = Flask(__name__)
app.secret_key = "Zucc"

with open('static/questions_1.json', 'r') as file:
    questions = json.load(file)

def update_stats(team_name, question):
    with open('static/stats.csv', 'a') as file:
        file.write(f"{team_name}, {str(question)}, {(time.localtime()[3:6])} \n")


with open('static/users.json',  'r') as file:
    users_data = json.load(file)


@app.route('/')
def index():
    if 'team_name' in session:
        return render_template('index.html', questions=questions, team_name=session['team_name'])
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
    if request.method == 'POST':
        user_answer = (request.form.get('answer'))
        correct_answer = question_data['answer']
        if user_answer == correct_answer:
            print(session)
            team_name = session['team_name']
            # update_score(team_name, stats_data.get(team_name, {}).get('score', 0) + 1)
            update_stats(team_name, question_id+1) # The +1 is for changing the index to question number
            return render_template('ans_correct.html')
        else:
            return render_template('ans_wrong.html')

    return render_template('question.html', question_data=question_data)


app.run(host = "0.0.0.0", debug=True)
