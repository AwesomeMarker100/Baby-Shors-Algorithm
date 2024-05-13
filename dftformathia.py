import cmath
import math
import random


def exponentiation(a : int, I : int, x : int):
    #f(x) = a^x mod I where I is our semi-prime to factor
    return math.pow(a, x) % I


def computeValues(a, I):
    
    #compute an arbitrary list of function values, i just do 10 (easy on the hardware)
    function_values = []

    for x in range(0, 10):

        function_values.append(exponentiation(a, I, x))


    return function_values

def DFT(N : int, func_values : list[:int]):

    dft_values = []
    
    #summing for all k frequencies
    for k in range(0, 4):
        grand_sum = 0
        #for each k frequency, we have to take the sum from 0 to N and take the function value * the complex part (look at formula for DFT in section 3.2.1)
        for n in range(0, N):
            
            real_part_complex = math.cos((-2 * math.pi * n * k) / N)
            im_part_complex = math.sin((-2 * math.pi * n * k) / N)

            complex_num = complex(real_part_complex, im_part_complex)
            grand_sum += func_values[n] * complex_num

        dft_values.append((1 / math.sqrt(N)) * grand_sum)
    
    return dft_values

def calculateMagnitudes(the_values):

    #this just creates a list of the magnitudes of each of the complex numbers we get from running the DFT function
    new_values = []
    for value in the_values:
        new_values.append(math.sqrt(math.pow(value.real, 2) + math.pow(value.imag, 2)))
    return new_values

def getLargestMagnitude(magnitude_values):

    #just a simple function for getting our largest magnitude (we're going to use this to assume our period)
    largest_value = 1
    for value in range(2, len(magnitude_values)):
        if magnitude_values[value] > magnitude_values[largest_value]: largest_value = value
    return largest_value

#GOOD
def euclideanAlgo(a, b):

    #look at section 3.1 for the process on this one, not the most concise function i've ever written but it does the job
    remainder = a % b
    if remainder == 0: return b
    q = b
    w = remainder

    while remainder != 0:

        remainder = q % w
        if remainder == 0: break
        q = w
        w = remainder

    return w


def runBabyShor(initial_guess, semi_prime_to_factor):

    #run the Euclidean Algorithm first, if the only factor in common is one, go through with the rest of the process
    if(euclideanAlgo(semi_prime_to_factor, initial_guess) == 1):

        #sample some values of our modular exponentiation graph, f(x) = a^x mod I where a is our initial guess, I is our prime that want to factor
        #then run the DFT function and get back a list of complex numbers. then create a list of the magnitudes of those complex numbers
        #the period will be the index with the largest magnitude 
        func_values = computeValues(initial_guess, semi_prime_to_factor)
        dft_values = DFT(len(func_values), func_values)
        magnitude_values = calculateMagnitudes(dft_values)

        period = getLargestMagnitude(magnitude_values)
        #recursion seemed like a good idea for this algo.
        #if we don't have a period of a multiple of 2, we'll end up with weird decimal values so just run the algo again with a different guess
        if period % 2 != 0: 
            return runBabyShor(random.randrange(2, semi_prime_to_factor), semi_prime_to_factor)
        else:
            #otherwise, if we have our next best guess, run this algorithm again
            prime_factor_guess = int(math.pow(initial_guess, (period/2)) - 1)
            return runBabyShor(prime_factor_guess, semi_prime_to_factor)
    #if our euclideanAlgo gives us a result other than 1, that result is one of the factors of the semi-prime!
    elif euclideanAlgo(semi_prime_to_factor, initial_guess) != 1:
        print(euclideanAlgo(semi_prime_to_factor, initial_guess))
        return int(euclideanAlgo(semi_prime_to_factor, initial_guess))
    

print("Result: " + str(runBabyShor(80000, 86483)))