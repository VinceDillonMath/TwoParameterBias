import os 
from tasks import main_prime
from sage.all import *

for p in list(primes(10000, 20000)):
    add.delay(main_prime(p))