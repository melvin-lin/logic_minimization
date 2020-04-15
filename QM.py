# Name: Melvin Lin
# Software Project: Designing a CAD Tool for Logic Minimization

#                           QM.py
# Purpose: The top level of the Quine-McCluskey algorithm that retrieves 
# information and calls functions from the funQM module and returns the 
# desired structure of the expressions in a string format
#

import funQM as QM
import re

def run(input): 
    text = ''; 

    x = input.partition("+")
    minterms = [int(i) for i in re.findall(r'\b\d+\b', x[0]) if "m" in x[0]]
    no_cares = [int(i) for i in re.findall(r'\b\d+\b', x[2]) if "d" in x[2]]

    n = QM.find_n(no_cares, minterms)

    maxterms = [i for i in range(2**n) if minterms.count(i) == 0 and no_cares.count(i) == 0]

    literals = QM.create_literals_array(n)

    minterms.sort()
    no_cares.sort()
    maxterms.sort()

    # Sum-of-Products (SOP) Process
    min_implicants = QM.find_implicants(minterms, no_cares, n)
    min_primes = QM.find_primes(min_implicants, n)
    min_prime_table = QM.create_prime_table(minterms, min_primes, n)
    min_essential_primes = QM.find_essential_primes(min_prime_table)
    SOP = QM.expression_SOP(min_essential_primes, literals)
    text += "SOP:" + SOP + "\n"

    # Product-of-Sums (POS) Process
    max_implicants = QM.find_implicants(maxterms, no_cares, n)
    max_primes = QM.find_primes(max_implicants, n)
    max_prime_table = QM.create_prime_table(maxterms, max_primes, n)
    max_essential_primes = QM.find_essential_primes(max_prime_table)
    max_essential_primes = QM.negate_primes(max_essential_primes)
    POS = QM.expression_POS(max_essential_primes, literals)
    text += "POS:" + POS

    return text