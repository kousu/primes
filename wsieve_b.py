#wsieve.py
"This file is made of cheese!"
"It also is the file that first implemented a sieve that avoids multiple hits -- it marks each composite once and only once"


import db
import profile

import itertools

import time

def wsieve(N):
	state = [-1, -1] + [0]*(N - 1)
	
	primes = [2]
	prime_i = 0
	lcm = 1
	
	p = 2
	while p**2 < N:
		#t0 = time.time()
		
		primes.extend(i for i in range(state.index(0, primes[-1]+1), p**2) if state[i] == 0)

		if lcm < p**2: #oh fuck it, just hardcore the two cases
			#this case is the case in which the limit we want to put on U is smaller than p**2 (which, note, is where wher have primes up to)
			#in this case we skip putting in primes at all (since i
			U = itertools.chain([1], [i for i in range(p, min(lcm, N//p)+1) if state[i] == 0])
		else:
			U = itertools.chain([1], primes[prime_i:], (i for i in range(p**2, min(lcm, N//p)+1) if state[i] == 0))
		#so, S only gets slow when it gets large, however this A) happens rapidly
			#almost all the work is being done in generating S.
			#which is dumb because A) S doesn't need to be totally regenerated each time, we just need to cross out certain elements (which ones they are, S implies for us)
		#if lcm > N//p:
		#	U = list(U)
		#	print(lcm, U[:100])
		#	input()
		#S = list(S)
		#input(S[:400])
		next_lcm = p*lcm;
		for sortaprime in U: #hah! "sortaprime"! that's *exactly* what the unit groups are: things that are -coprime- to a specific list of things.
			for i in range(p*sortaprime, N+1, next_lcm):
				#if state[i] != 0:
				#	print("bad!", i, "is already marked as", state[i], "but we're doing it as", p, "(and m=",0,"sortaprime=",sortaprime,")")
				state[i] = p
		
		lcm = next_lcm
		prime_i += 1
		p = primes[prime_i] #state.index(0, p+1) #find the next prime in overall O(n) time since it doesn't have to search from the beginning each time
		
		#print("iteration %d took %0.2f" % (p, time.time() - t0))
	
	#input(("Proportion we actually only need to scan with prime-saving improvement", int(B/A * 10**4)/100))
	#primes += [i for i in range(primes[-1], N+1) if state[i] == 0]
	return primes


def go():
	N = int(10**6)
	t0 = time.time()
	r = wsieve(N)
	t1 = time.time()
	print("for %d took %0.4f" % (N, t1-t0))
	#print(r)
	import db
	db.ensure(r)

go()

#profile.run("go()", sort=1)
		
