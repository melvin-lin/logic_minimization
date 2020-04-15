# Name: Melvin Lin
# Software Project: Designing a CAD Tool for Logic Minimization

#                              funQM.py
# Purpose: This module does the bulk of the Quine-McCluskey algorithm,
# which are placed into functions because these functions can be reused
# for both the SOP and POS expressions. 
#

import re
from collections import Counter

# Function to find the value of n
def find_n(no_cares, minterms): 
    if len(no_cares) == 0: 
        max_value = max(minterms)
    else: 
        max_value = max(minterms) if max(minterms) > max(no_cares) else max(no_cares)

    for i in range(11): 
        if max_value <= (2**i - 1): 
            return i

# Function to create the array of n literals (A - J)
def create_literals_array(n): 
    literals = [[]]
    ascii_start = 65
    
    for i in range(n - 1): 
        literals.append([])
    
    for i in range(len(literals)): 
        for j in range(2): 
            char = chr(ascii_start + i)
            if j == 0: 
                char += '\''
            literals[i].append(char)
    
    return literals 

# Function to create implicants from minterms and don't cares or maxterms and don't cares
def find_implicants(mterms, no_cares, n):    
    bmterms = [[]]
    
    for i in range(n):
        bmterms.append([])
        
    for i in range(0, len(mterms)):
        bmterms[bin(mterms[i]).count("1")].append(format(mterms[i], '0' + str(n) + 'b'))
    
    for i in range(0, len(no_cares)): 
        bmterms[bin(no_cares[i]).count("1")].append(format(no_cares[i], '0' + str(n) + 'b'))

    return bmterms  

# Determines all the primes present for minterms and don't cares or maxterms and don't cares
def find_primes(implicants, n): 
    primes = []

    is_end = False
    while (is_end == False):
        new_implicants = [[]]
        is_prime = [ [ True for j in range(len(implicants[i])) ] for i in range(len(implicants))]
        not_primes_count = 0; 
        for i in range(n): 
            new_implicants.append([])

        for i in range(n):
            for j in range(len(implicants[i])): 
                for k in range(len(implicants[i+1])):
                    index = -1
                    diff_count = 0
                    for w in range(len(implicants[i][j])):
                        if implicants[i][j][w] != implicants[i+1][k][w]:
                            diff_count += 1
                            index = w
                    if diff_count == 1: 
                        curr_implicant = list(implicants[i][j])
                        curr_implicant[index] = '-'
                        new_implicants[i].insert(j, ''.join(curr_implicant))
                        is_prime[i][j] = False
                        is_prime[i+1][k] = False

        for i in range(len(is_prime)): 
            curr_primes = [j for j in range(len(is_prime[i])) if is_prime[i][j] == True] 
            not_primes = [j for j in range(len(is_prime[i])) if is_prime[i][j] == False] 
            not_primes_count += len(not_primes)
            for k in range(len(curr_primes)): 
                primes.append(implicants[i][curr_primes[k]])

        implicants = new_implicants

        if (not_primes_count == 0): 
            is_end = True
            
    return list(set(primes))

# Create the prime implicant table 

def create_prime_table(mterms, primes, n):
    new_mterms = []
    implicant_table = [[]]
    
    for i in range(0, len(mterms)): 
        new_mterms.append(format(mterms[i], '0' + str(n) + 'b'))
    
    for i in range(len(new_mterms) - 1): 
        implicant_table.append([])
    
    for i in range(len(mterms)): 
        for j in range(len(primes)): 
            match = 0 
            for k in range(len(primes[j])): 
                if new_mterms[i][k] == primes[j][k] or primes[j][k] == '-':
                    match += 1
            if (match == n): 
                implicant_table[i].append(primes[j])
                
    return implicant_table

# Finds all the most common values from 2D list
def most_common(lst): 
    return [Counter(col).most_common(1)[0][0] for col in zip(*lst)]

# Retrieves the last essential prime implicant
def find_last_essential(implicant_table):
    index = 0
    element = ''
    essential = []
    
    for i in range(len(implicant_table)):
        for j in range(len(implicant_table[i])): 
            if len(implicant_table[i]) != 0:
                essential = implicant_table[i]
    
    for i in range(len(essential)-1): 
        if essential[i].count('-') > essential[i+1].count('-'): 
            element = essential[i]
            index = i
        else: 
            element = essential[i+1]
            index = i+1
            
    return element 

# Retrieves all the essential prime implicants from prime implicants table
def find_essential_primes(implicant_table): 
    essential_primes = []

    for i in range(len(implicant_table)): 
        if len(implicant_table[i]) == 1: 
            essential_primes.append(implicant_table[i][0])
            implicant_table[i].pop(0)
        
    if len(essential_primes) == 0: 
        essential_primes = most_common(implicant_table)

    for i in range(len(essential_primes)): 
        for j in range(len(implicant_table)): 
            if len(implicant_table[j]) != 0: 
                if implicant_table[j].count(essential_primes[i]) != 0: 
                    for k in range(len(implicant_table[j])): 
                        implicant_table[j].pop(len(implicant_table[j])-1)
    
    essential = find_last_essential(implicant_table)
    
    if (len(essential) != 0): 
        essential_primes.append(essential)

    return list(set(essential_primes))

# Negates the value for POS
def negate_primes(essential_primes): 
    negated_primes = []
    
    for i in range(len(essential_primes)): 
        current_prime = list(essential_primes[i])
        for j in range(len(essential_primes[i])): 
            if essential_primes[i][j] == '0':
                current_prime[j] = '1'
            elif essential_primes[i][j] == '1': 
                current_prime[j] = '0'
        negated_primes.insert(i, ''.join(current_prime))
    
    return negated_primes

# Change Binary to Literals
def binary_to_literals(essential_primes, literals,i): 
    expression = []
    
    for j in range(len(essential_primes[i])): 
        if (essential_primes[i][j] == '0'): 
            expression.append(literals[j][0])
        elif (essential_primes[i][j] == '1'): 
            expression.append(literals[j][1])
    
    return expression

# Change to SOP Expression
def expression_SOP(essential_primes, literals): 
    SOP = []
    expression = ''
    
    for i in range(len(essential_primes)): 
        element = binary_to_literals(essential_primes, literals, i)   
        SOP.append(''.join([str(i) for i in element]))
    
    for i in range(len(SOP)): 
        expression += SOP[i]
        if (i < len(SOP) - 1): 
            expression += " + "
            
    return expression

# Change to POS Expression
def expression_POS(essential_primes, literals): 
    POS = []
    expression = ''
    
    for i in range(len(essential_primes)): 
        value = ''
        element = binary_to_literals(essential_primes, literals, i)  
        for j in range(len(element) - 1): 
            value += element[j] + " + "
        value += element[len(element) - 1]
        POS.append(value)
    
    for i in range(len(POS)): 
        if (len(POS[i]) == 2 and POS[i].count('\'') == 1) or len(POS[i]) == 1:  
            expression += POS[i]
        else: 
            expression += "(" + POS[i] + ")"
    
    return expression 