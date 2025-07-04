from sage.all import *
import sys 

def is_fourth_power(x, p):
    if p % 4 == 1:
        return power_mod(x, (p - 1) // 4, p) == 1
    else:
        return power_mod(x, (p - 1) // 2, p) == 1

def frobenius_trace(A, B, p): # Sage implementation uses Schoof's algorithm
    k = GF(p)
    try:
        E = EllipticCurve(k, [Integer(A), Integer(B)])
        return -(p + 1 - E.cardinality())
    except (ArithmeticError):
        return "Singular Curve"

def inverse(a, p):
    return power_mod(a, p - 2, p) # allow zero 

def find_quartic_residue_classes(p):
    # Hardcoded small primes
    if p == 2:
        return [0, 1]
    elif p == 3:
        return [0, 1, 2]
    elif p == 5:
        return [0, 1, 2, 3, 4]

    class_reps = [0]  # Always include 0
    for i in range(1, p):
        in_prev_res_class = False
        for rep in class_reps:
            thing_to_check = (i * inverse(rep, p)) % p
            # isFourthPower: if exists x s.t. x^4 ≡ thing_to_check mod p
            if is_fourth_power(thing_to_check, p):
                in_prev_res_class = True
                break
        if not in_prev_res_class:
            class_reps.append(i)

        # Early stopping based on number of quartic residue classes
        if p % 4 == 3 and len(class_reps) >= 3:
            return class_reps
        elif p % 4 == 1 and len(class_reps) >= 5:
            return class_reps

    print("Something very bad has happened if this is printed.")
    return class_reps

def a_for_prime(p, output_dir='classdata'):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"file_{p}.csv")

    with open(filename, "w") as f:
        residue_classes = find_quartic_residue_classes(p)

        # A = 0 special case
        if p % 3 == 1:
            seen = set()
            written = 0
            for b in range(1, p):
                if written == 6:
                    break
                result = frobenius_trace(0, b, p)
                if result not in seen:
                    seen.add(result)
                    f.write(f"{b},{result}\n")
                    written += 1

        # A ≠ 0 cases (use quartic residues)
        for A in residue_classes[1:]:  # skip A = 0
            for B in range(p):
                result = frobenius_trace(A, B, p)
                f.write(f"{result}\n")

    return 1


def compute_a_constants(lower, upper, output_dir="classdata"):
    import os
    os.makedirs(output_dir, exist_ok=True)

    primes_list = list(primes(lower, upper))
    num_primes = len(primes_list)

    # Precompute Legendre symbols
    # bigArray = {}
    # for p in primes_list:
    #     table = [legendre_symbol(x, p) for x in range(p)]
    #     bigArray[p] = table
    #     print(f"Finished legendre symbols for {p}")

    for p in primes_list:
        # legendre_table = bigArray[p]
        filename = os.path.join(output_dir, f"file_{p}.csv")

        with open(filename, "w") as f:
            residue_classes = find_quartic_residue_classes(p)

            # A = 0 special case
            if p % 3 == 1:
                seen = set()
                written = 0
                for b in range(1, p):
                    if written == 6:
                        break
                    result = frobenius_trace(0, b, p)
                    if result not in seen:
                        seen.add(result)
                        f.write(f"{b},{result}\n")
                        written += 1

            # A ≠ 0 cases (use quartic residues)
            for A in residue_classes[1:]:  # skip A = 0
                for B in range(p):
                    result = frobenius_trace(A, B, p)
                    f.write(f"{result}\n")

        num_primes -= 1
        print(f"Primes Remaining: {num_primes}")

if __name__ == "__main__":
    if (len(sys.argv[1:]) != 2):
        print("Usage: sage -python trace_of_frobenius.py <lower> <upper>")
    else: 
        try: 
            compute_a_constants(sys.argv[1], sys.argv[2])
        except: 
            print("<lower> and <upper> must be integers")