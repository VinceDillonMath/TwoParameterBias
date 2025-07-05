import os
from sympy import primerange
primes= primes = list(primerange(0, 1000000))
import sys
import csv

def getMissingPrimes(file):
    missing = []
    primesDone = set(os.listdir(file))

    for p in primes:
        filename = f"file_{p}.csv"
        if filename not in primesDone:
            missing.append(p)
    return missing



if __name__ == "__main__":
    try:
        folder_path = sys.argv[1]
        newFileName = sys.argv[2]
        filepath = os.path.join(os.getcwd(), newFileName)
        missingPrimes = getMissingPrimes(folder_path)
        with open(newFileName, 'w', newline='') as f:
            writer = csv.writer(f)
            for num in missingPrimes:
                writer.writerow([num])
    except:
        "An Error Occured. Check the file directory."




