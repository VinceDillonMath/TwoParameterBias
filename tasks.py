from celery import Celery
# from trace_of_frobenius import a_for_prime

app = Celery('tasks', broker='amqp://pr4:small2025@137.165.79.192/')

@app.task
def main_prime(p):
    return p
