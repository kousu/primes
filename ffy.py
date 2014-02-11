

import time, math

def pp(X):
    "determine if X is a prime power (i.e. X = p**k for some k), and if so what prime it is. Depends on having a list of primes called prms"
    for p in prms:
        if X % p == 0:
            while X % p == 0:
                    X /= p
            if X == 1:
                    return p
            else:
                    return None

import sys
from itertools import islice

def sieveComposites(N):
    composite = [False]*(N+1) #marked True if they known to be composite
    for s in range(2, N+1):
        if not composite[s]:
            for e in range(s**2, N+1, s):
                composite[e] = True
    return [i for i in range(2, N+1) if not composite[i]]

def sievePrimes(N):
    prime = [True]*(N+1) #marked True if they known to be composite
    for s in range(2, N+1):	
        if prime[s]:
            #t0 = time.time()
            for e in range(s**2, N+1, s):
                prime[e] = False
            #print("loop %d took %0.2f" % (s,time.time() - t0)) if s < 10 else None
    return [i for i in range(2, N+1) if prime[i]]

sieve = sievePrimes

#wtf supersieve is FASTER than sieve? but it's the same code but with more!?

def supersieve(N):
    "produce a sieve that contains *primes* and *prime powers*"
    #print("supersieve: ", N)
    ints = [0] * (N+1) #note: [0,1] are in there to make programming easier. DON'T USE THEM.
        # -1 means fail, 0 means untouched.
    for s in range(2, N+1):
        if ints[s]: continue
        ints[s] = s
        for e in range(s+s, N+1, s): #can this be s**2?
            if ints[e] == 0:
                ints[e] = s
            else: #elif ints[e] > 0:
                ints[e] = -1
    #return
    #return ints #notice: this algorithm could be trivially extended to count *which* power of p each found power is, by tracking the current count in a hashtable on the side 
    #another thing that would be superuseful is a quick way of producing what the primes actually are
    d = dict((i, e) for i, e in enumerate(ints) if i>=2 and e > 0) 
    #for n in sorted(d.keys()):
    #    print("%d is a power of %d" % (n, d[n]))
    return d

def supersieve2(N):
    "produce a sieve that contains *primes* and *prime powers*"
    #print("supersieve: ", N)
    ints = [0] * (N+1) #note: [0,1] are in there to make programming easier. DON'T USE THEM.
        # -1 means fail, 0 means untouched.
    rt = int(math.sqrt(N))
    for s in range(2, rt+1):
        if ints[s]: continue
        ints[s] = s
        for e in range(s+s, N+1, s): #can this be s**2?
            if ints[e] == 0:
                ints[e] = s
            else: #elif ints[e] > 0:
                ints[e] = -1
    
    #for s > sqrt(N), everything that is composite (by that theorem about that) has already been marked composite 
    #so any multiple of anything must be a bad composite
    for s in range(rt+1, N+1):
        if ints[s]: continue
        ints[s] = s
        for e in range(s+s, N+1, s): #can this?
            ints[e] = -1
    #... this provides a very very very modest speedup. dang.
    #return
    #return ints #notice: this algorithm could be trivially extended to count *which* power of p each found power is, by tracking the current count in a hashtable on the side 
    #another thing that would be superuseful is a quick way of producing what the primes actually are
    d = dict((i, e) for i, e in enumerate(ints) if i>=2 and e > 0) 
    #for n in sorted(d.keys()):
    #    print("%d is a power of %d" % (n, d[n]))
    return d


def supersieve_original(N):
    "produce a sieve that contains *primes* and *prime powers*"
    ints = [False] * (N+1) #note: [0,1] are in there to make programming easier. DON'T USE THEM.
        # -1 means fail, 0 means untouched.
    for s in range(2, N+1):
        if ints[s]:
            continue
        #p = s #s is prime if it's untouched when we reach it in the outer loop
        for e in range(s+s, N+1, s):
            #cases: 0 -> untouched, so mark it as a multiple of s
            #       s -> oh, another prime got here first. it must be bad.
            #       -1 -> marked composite already, so fuck it
            if ints[e] == 0:
               ints[e] = s
            elif ints[e] > 0:
               ints[e] = -1
        #print(i, ints)
    #notice: this algorithm could be trivially extended to count *which* power of p each found power is, by tracking the current count in a hashtable on the side 
    #another thing that would be superuseful is a quick way of producing what the primes actually are
    return ints #returning the ints is better for my other alg
    #d = dict((i, e) for i, e in enumerate(ints) if i>=2 and e > 0) 
    #for n in sorted(d.keys()):
    #    print("%d is a power of %d" % (n, d[n]))
    #return d

def supersieve_hash(N):
    "produce a sieve that contains *primes* and *prime powers*"
    "uses a hashtable intermediately"
    #composite = [False] * (N+1) #note: [0,1] are in there to make programming easier. DON'T USE THEM.
    powers = dict((s, None) for s in range(2,N+1))
    for s in range(2, N+1):
        if powers.get(s, False) is not None:
            #print("%d is composite" % s)
            continue
        #p = s #s is prime if it's untouched when we reach it in the outer loop
        #input("%d is prime" % s)
        powers[s] = s
        #input("GOING INTO INNER LOOP WITH S=%d" % s)
        for e in range(s+s, N+1, s):
            #composite[e] = True #seen. so not prime.
            if e not in powers: continue
            #we know s is composite if powers[s] is not None (except for the primes themselves, but I think we're skipping them so it's okay?)
            #cases: 0 -> untouched, so mark it as a multiple of s
            #       s -> oh, another prime got here first. it must be bad.
            #       -1 -> marked composite already, so fuck it
            #if e == 99999:
            #    print("at 99999")
            #    print(powers.get(e, "not found"))
            #    #input()
            if powers[e] is None:
                powers[e] = s
            else:
                #if s == 
                #print(e, powers[e])
                #input()
                del powers[e]
                #print(e)
            #if ints[e] == 0:
            #   ints[e] = s
            #elif ints[e] > 0:
            #   ints[e] = -1
        #print(i, ints)
        #print(powers)
    #notice: this algorithm could be trivially extended to count *which* power of p each found power is, by tracking the current count in a hashtable on the side 
    #another thing that would be superuseful is a quick way of producing what the primes actually are
    return powers #returning the ints is better for my other alg
    d = dict((i, e) for i, e in enumerate(ints) if i>=2 and e > 0) 
    #for n in sorted(d.keys()):
    #    print("%d is a power of %d" % (n, d[n]))
    return d


def Time(F, *args, **kwargs):
    t0 = time.time()
    r = F(*args, **kwargs)
    t1 = time.time()
    #print("%s%s took %.2fseconds" % (F.__name__, args, t1 - t0))
    return t1 - t0


def TimingAverage(F, rounds, *args, **kwargs):
    return sum(Time(F, *args, **kwargs) for s in range(rounds)) / rounds

print("Hello?")
Sieve = {}
Supersieve = {}
import csv
#f = open("sieves.dat", "w")
#w = csv.writer(f)

#for n in [2**i for i in range(1, 28)]:
#    print(n)
#    Sieve[n] = TimingAverage(sieve, 3, n)
#    Supersieve[n] = TimingAverage(supersieve, 3, n)
    #(Time(sieve, n))
    #Time(supersieve, n)
    #(Time(supersieve_hash, n))
    #input("[Enter]: ")
#    w.writerow((n, 10**6 * Sieve[n], 10**6 * Supersieve[n]))
#    f.flush()
    
#f.close()

#print(Sieve)
#print(Supersieve)
#print(TimingAverage(supersieve, 3, 10**6))
#input()


def ffffv2(N):
    print(N)
    d0 = time.time()
    S = supersieve(N)
    d1 = time.time()
    print("supersieve took: %2f" % (d1 - d0))
    factorization = {}
    for k in range(1, N//2):
      #block = S[N//(k+1)+1:N//k+1]
      Range = (N//(k+1)+1, N//k+1)
      if Range[0] == Range[1]: continue
      #jif block:
      #    print(k)
      for i in range(*Range):
          p = S[i] #[p for p in block if p > 0]:
          if p <= 0: continue
          if k < math.sqrt(N):
              print(i,p)
          factorization[p] = factorization.get(p, 0) + k

    return factorization

def ffffv3(N):
    d0 = time.time()
    S = supersieve(N)
    d1 = time.time()
    print("supersieve took: %2f" % (d1 - d0))
    factorization = {}
    
    #important fucking line:
    #also, magical fucking line.
    #k is a bucket index, (N//(k+1), N//k] is a bucket interval for bucket k. but many buckets are lamely empty,
    #however these lines compute *only* the nonempty buckets
    bits = [N//k for k in range(1, int(math.sqrt(N)))] #<-- actual buckets
    bits += [g for g in range(bits[-1]-1, 0, -1)]      #<-- single elements
    bits.reverse()
    
    for i,k in enumerate(bits[:-2]):
      
      #block = S[N//(k+1)+1:N//k+1]
      Range = bits[-(i+1)-1], bits[-(i+1)]
      
      for i in range(*Range):
          p = S[i] #[p for p in block if p > 0]:
          if p <= 0: continue
          #if k < math.sqrt(N):
          #    print(i,p)
          factorization[p] = factorization.get(p, 0) + k

    return factorization

ffff = ffffv3

def mu(f):
    t = 1
    for p in f:
            t*=p**f[p]
    return t



import time
d0 = time.time()
#r = (ffff(1000000))
d1 = time.time()
print(d1 - d0)
#print(r)
#print(mu(r))
import math
#print(math.factorial(39))
