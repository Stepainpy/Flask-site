from db_prog import get_question_after, get_quises, check_answer
from flask import Flask, session, request, redirect, url_for, render_template
from random import shuffle
import os

def start_quis(qi):
    session['quiz'] = qi
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    q_list = get_quises()
    return render_template('start.html', q_list=q_list)

def save_answer():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] += 1

def question_form(question):
    answer_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answer_list)
    return render_template('test.html', question=question[1], quest_id=question[0], answer_list=answer_list)

def index():
    if request.method == 'GET':
        start_quis(-1)
        return quiz_form()
    else:
        quest_id = request.form.get('quiz')
        start_quis(quest_id)
        return redirect(url_for('test'))

def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            if request.method == 'POST':
                save_answer()
            
            next_question = get_question_after(session['last_question'], session['quiz'])
            if next_question is None or len(next_question) == 0:
                return redirect(url_for('result'))
            else:
                return question_form(next_question)

def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html

folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test', 'test', test, methods=['post', 'get'])
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = 'cf,bjdflubkihgfbhfj'

if __name__ == "__main__":
    app.run()