from rq import get_current_job
from website import generatingQuestions

def generate_questions(text, questions_count):
    job = get_current_job()
    try:
        result = generatingQuestions.get_response(text, questions_count)["questions"]
        return result
    except Exception as e:

        job.meta['error'] = str(e)
        job.save()

