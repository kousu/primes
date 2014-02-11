#!/usr/bin/env python3
#factoring factorials

import math
import time
from time import sleep
from functools import reduce

def product(lst):
	return reduce(lambda a,b: a*b, lst, 1)


def ffc(N):
	start = time.time()
	#print("Starting with", n)
	print("Constructing N+1 array")
	t0 = time.time()
	factors = [[] for i in range(N+1)] #must construct the list this way because otherwise it's one giant shared list of all the factors of everything (which leads to a Zero Division)
	T = time.time() - t0
	print("Done constructing array, took %02f" % T)
	
	t0 = time.time()
	for s in range(2, N+1):
		G = s//product(factors[s])
		#print("Going to be sticking %ds in" % G)
		if G == 1:
			#print("%d has no factors for us, skipping" % s)
			continue
		for i in range(s, N+1, s):
			factors[i].append(G)
		#	print("editing", i, factors[i])
	T = time.time() - t0	
	print("done factoring, took %2f" % T)	
	t0 = time.time()
	counts = {}
	for n in factors:
		for f in n:
			counts[f] = counts.get(f, 0)+1
	T = time.time() - t0
	print("done counting, took %2f" % T)
	print("Done counting factors, took %2f" % T)
	print("ffc: %2f" % (time.time() - start)) 
	return counts


TIMINGS = {}

def fff(N):
	"fast factorial factoring"
	start = time.time()
	def c(b):
		"count the number of powers of b in N!"
		m = int(math.log(N, b))
		return sum(N//b**j for j in range(1, m+1))
	#prime sieve
	print("Begin constructing prime sieve list")
	t0 = time.time()
	prms = [True]*(N+1)
	T = time.time() - t0
	print("Done constructing prime sieve list, took %02f" % T)
	t0 = time.time()
	for s in range(2, N+1):
		if prms[s]:
			for e in range(s+s, N+1, s):
				prms[e] = False
	prms = [i for i in range(2, N+1) if prms[i]]
	print("Done sieving, took %2f to get %d primes" % (time.time() - t0, len(prms)))
	
	#I can save some time (maybe?) by dividing out factors as I find them--it'll make bigint work less hard.
	#count prime factors
	t0 = time.time()
	d =  dict((p, c(p)) for p in prms)
	T = time.time() - t0
	print("Done counting factors, took %2f" % T)
	print("fff: %2f" % (time.time() - start)) 
	return d

def ffffv1(N):
	"fucking fast factorial factoring"
	start = time.time()
	#ideas:
	#exploit binary computer to count the number of 2s directly (look at the number of 0 bits)
	#-> and then bitshift those off. shouuld have the same factors
	#exploit the fact that the exponents are sorted, somehow?
	#--exploit that primes > n/2 necessarily only appear once--
	#For k < sqrt(N) - 1:
	rt = int(math.sqrt(N))
	#primes above rt are squarefree
	#primes below are sexy
	#further: if we bucket into (N/k+1, N/k], squarefree elements in bucket k have k powers
	#AND buckets 1..rt have the property that they are entirely squarefree 
	#bucket rt+1....might be partially squarefree
	#buckets above are definitely not squarefree
	#so we can bucket off the top primes in ...a place. #all primes above N/(k+1) where k=floor(sqrt(N))
	
	print("Begin constructing prime sieve list")
	t0 = time.time()
	prms = [True]*(N+1)
	T = time.time() - t0
	print("Done constructing prime sieve list, took %02f" % T)
	t0 = time.time()
	for s in range(2, N+1):
		if prms[s]:
			for e in range(s+s, N+1, s):
				prms[e] = False
	print("Took %02f to sieve" % (time.time() - t0))
	buckets = {}
	for k in range(1, int(math.sqrt(N))): #NB: only goes up to sqrt(N)-1
		bounds = (N//(k+1), N//k)
		#print("(%d, %d]" % bounds)
		buckets[k] = [i for i in range(bounds[0]+1, bounds[1]+1) if prms[i]]	
		
	def c(b):
		"count the number of powers of b in N!"
		m = int(math.log(N, b))
		return sum(N//b**j for j in range(1, m+1))
	
	prms = [i for i in range(2, int(math.sqrt(N))+1) if prms[i]]
	d =  dict((p, c(p)) for p in prms)
	for k in buckets:
		for e in buckets[k]:
			d[e] = k
	print("ffffv1: %2f" % (time.time() - start)) 
	return d

def ffffv1v2(N):
	"fucking fast factorial factoring -- edit"
	rt = int(math.sqrt(N))

	prms = [True]*(N+1)

	prms = sieve(N)
	
	bits = [N//k for k in range(1, int(math.sqrt(N))+1)] #<-- actual buckets
	#bits.reverse()
	#print(bits)
	#buckets = {}
	d = {}
	for k in range(len(bits)-1): #NB: only goes up to sqrt(N)-1
		#print("(%d, %d]" % bounds)
		for i in range(bits[k+1]+1, bits[k]+1):
			if prms[i]:
				d[i] = k+1
		#buckets[k+1] = [i for i in  if prms[i]]	
	
	#print(buckets)
	def c(b):
		"count the number of powers of b in N!"
		m = int(math.log(N, b))
		return sum(N//b**j for j in range(1, m+1))
	
	for i in range(2, int(math.sqrt(N))+1):
		if prms[i]:
			d[i] = c(i)
	#for k in buckets:
	#	for e in buckets[k]:
	#		d[e] = k
	return d

def ffffv2(N):
	raise "Not yet"

from ffy import sieve

def sievePrimes(N):
    prime = [True]*(N+1)
    for s in range(2, N+1):
        if prime[s]:
            for e in range(s**2, N+1, s):
                prime[e] = False
    return prime

sieve = sievePrimes

def ffffv4(N):
    S = sieve(N)
    factorization = {}

    #important fucking line:
    #also, magical fucking line.
    #k is a bucket index, (N//(k+1), N//k] is a bucket interval for bucket k. but many buckets are lamely empty,
    #however these lines compute *only* the nonempty buckets
    bits = [N//k for k in range(1, int(math.sqrt(N)))] #<-- actual buckets
    bits += [g for g in range(bits[-1]-1, 0, -1)]      #<-- single elements
    bits.reverse()  
    #print(bits)
    for i,k in enumerate(bits[:-1]):

     
      Range = bits[-(i+1)-1]+1, bits[-(i+1)]+1
      #print(i, k, Range)
      #block = S[Range[0]:Range[1]]
      #print("=>", block)

      for i in range(*Range):
          p = i #S[i] #[p for p in block if p > 0]:
          if not S[p]: continue
          #if k < math.sqrt(N):
          #    print(i,p)
          factorization[p] = factorization.get(p, 0) + k

    #print(prettyprint(factorization))

    def c(b):
        "count the number of powers of b in N!"
        m = int(math.log(N, b))
        return sum(N//b**j for j in range(2, m+1))
    
    i = 0
    for i in range(2, int(math.sqrt(N))+1):
        if S[i]:
            factorization[i] += c(i)
	#prms = [i for i in range(2, int(math.sqrt(N))+1) if prms[i]]
    #print(prettyprint(factorization))
    return factorization
#    d = dict((p, c(p)) for p in prms)
#    for k in buckets:
#        for e in buckets[k]:
#            d[e] = k
#	return d
	

ffff = ffffv1
#ffff = ffffv2
ffff = ffffv4

def choose(n,k):
	"fast algorithm for computing n-choose-k"
	raise NotImplemented

def prettyprint(counts):
	def pg(p):
		e = counts[p]
		if e == 1:
			return "%d" % p
		else:
			return "%d**%d" % (p, e)
	return " * ".join([pg(p) for p in sorted(counts.keys())])

if __name__ == '__main__':
	n = int(input("Enter n: "));
	if n < 2:
		raise ValueError("Fuck you hater")
	print("-"*17)
	cts = ffc(n)
	print("-"*17)
	cts2 = fff(n)
	print("-"*17)
	cts3 = ffff(n)
	print("-"*17)
	print("%d! = %s" % (n, prettyprint(cts)))
	print("%d! = %s" % (n, prettyprint(cts2)))
	print("%d! = %s" % (n, prettyprint(cts3)))
	import math
	est = n / math.log(n)
	est = (int(est), int(1.25506 * est))
	#input("hit [Enter]")
	print("There should be approximately %s primes in that list (actual: %d)" % (est, len(cts)))
	print("There should be approximately %s primes in that list (actual: %d)" % (est, len(cts2)))
	c = fff(13131313191117151443222212121212121212121222112345678970987654327626726472647264726472647264726427649218726675453687290348769852304)
	#print (f)
	#print()
	print(c)
