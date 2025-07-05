from celery import Celery
# from trace_of_frobenius import a_for_prime

app = Celery('tasks', broker='a')

@app.task
def main_prime(p):
    return p
