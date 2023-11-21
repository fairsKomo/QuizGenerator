from flask import render_template, Blueprint, request, session, redirect, url_for
from rq import Queue, get_current_job
from redis import Redis
from tasks import generate_questions
import generatingQuestions

view = Blueprint('view', __name__)

redis_conn = Redis.from_url("redis://localhost:6379/0")
rq = Queue(connection=redis_conn)

@view.route('/')
def upload_pdf():
    return render_template('index.html')

@view.route('/', methods = ['GET', 'POST'])
def upload_file():

   if request.method == 'POST':
      if 'file' in request.files:
        f = request.files['file']
        questionsCount = request.form.get('questionCount')

        text = generatingQuestions.loadPdf(f)
        job = rq.enqueue(generate_questions, text, questionsCount)

        return render_template('loading.html', job_id=job.id)
              
        # session['gptR'] = gptR
        # session['currentQuestion'] = 0
        # session['score'] = 0
        # session['incorrect_answers'] = []
        # session['total'] = len(gptR)
        # print(gptR)

      elif 'quiz-option' in request.form:
        selected_option = request.form.get('quiz-option')
        gptR = session.get('gptR')
        currentQuestion = session.get('currentQuestion')

        correct_answer = gptR[currentQuestion]["correct_answer"]
        if selected_option == correct_answer:
          print("correct")
          session['score'] += 1
        else:
          print("false")
          session['incorrect_answers'].append({
              'question':gptR[currentQuestion]["question"],
              'your_answer':selected_option,
              'correct_answer':correct_answer
          })
          
        if currentQuestion + 1 < len(gptR):
          session['currentQuestion'] += 1

          return redirect(url_for('view.display_question'))
        else:
          score = session.get('score')
          total = session.get('total')
          incorrect_answers = session.get('incorrect_answers')
          return render_template('index.html', myScore = f"{score}/{total}", incorrect_answers=incorrect_answers)

      else:
         return render_template('index.html')

  

@view.route('/check_task/<job_id>')
def check_task(job_id):
    job = get_current_job(job_id, connection=redis_conn)
    if job.is_finished:
        gpt_r = job.result
        session['gptR'] = gpt_r
        session['currentQuestion'] = 0
        session['score'] = 0
        session['incorrect_answers'] = []
        session['total'] = len(gpt_r)
        return render_template('index.html', data=gpt_r[0])
    elif job.is_failed:
        error_message = job.meta.get('error', 'Unknown error')
        return render_template('error.html', error_message=error_message)
    else:
        return render_template('loading.html', job_id=job.id)
