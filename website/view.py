from flask import render_template, Blueprint, request, session, redirect, url_for
from website import generatingQuestions
from redis import Redis
from rq import Worker, Queue, Connection

view = Blueprint('view', __name__)
redis_conn = Redis.from_url('redis://localhost:6379/0')
rq_queue = Queue('default', connection=redis_conn)


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
        job = rq_queue.enqueue(generatingQuestions.get_response, text, questionsCount)
        session['job_id'] = job.get_id()

        return render_template('processing.html')
      
        # session['score'] = 0
        # session['incorrect_answers'] = []
        # session['total'] = len(gptR)
        # print(gptR)

        # return render_template('index.html', data = gptR[0])
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

  

@view.route('/display_question')
def display_question():
  job_id = session.get('job_id')

  if job_id:
      job = rq_queue.fetch_job(job_id)

      if job.is_finished:
          gptR = job.result["questions"]
          session.pop('job_id', None)
      else:
          return render_template('processing.html')

  else:
      gptR = session.get('gptR')

  currentQuestion = session.get('currentQuestion')
  return render_template('index.html', data=gptR[currentQuestion])





