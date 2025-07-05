import os 
from tasks import main_prime
from sympy import primerange
from celery.signals import task_postrun

# from sage.all import *

with open('missing', 'r', newline='') as f:
    for line in f:
        main_prime.delay(int(line))

