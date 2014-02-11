#wsieve.py
"This file is made of cheese!"
"It also is the file that first implemented a sieve that avoids multiple hits -- it marks each composite once and only once"

import profile

import time

def mul(p,k,sortaprime):
	"split this into a function so the profiler times it"
	return p*(k + sortaprime)

def mul2(a,b):
	return a*b;

def owsieve(N):
	state = [0]*(N + 1)
	state[0] = -1 #fuck that guy
	state[1] = -1
	
	primes = []
	lcm = 1
	S = [1]
	
	#things in the list state[lastlimit:lcm] that 
	
	#[1] <-- 2
	#[1] <-- 3
	#[1,5] <-- 5
	#[1, 7, 11, 13, 17, 19, 23, 29] <-- 7 ( things in the list that are unmarked between 7 and lcm)
	
	
	while not primes or primes[-1]**2 < N:
		t0 = time.time()
		#print(primes[-1])
		#print(state[:50])
		p = state.index(0, primes[-1] if primes else 2)
		#print("found",p,"as prime")
		#at each step, we remove the first non-zero S, and add all unmarked terms in p**2..lcm
		#note: lcm might be less than p**2, but that only happens on.. p=2? because for p=3, p**2 = 9 and lcm = 6 and then it just keeps growing
		c_ache = len(S)

		S = [1] + [i for i in range(p, min(lcm, N//p)+1) if state[i] == 0]
		#so, S only gets slow when it gets large, however this A) happens rapidly
			#almost all the work is being done in generating S.
			#which is dumb because A) S doesn't need to be totally regenerated each time
		print("length to scan:", min(lcm, N//p)+1 - p)
		#print(len(S))

		
		#PREVIOUS LIMIT WHORES <-- what?
		
		#input(("p=",p,"lcm=",lcm))
		#input(("S=",S,))
		#input(state[:100])
		#input(primes)
		
		#i feel like this would be faster with judicious use of squares
		
		#if you unroll the first loop you can also be scanning for the new bitches there
		
		#todo: unroll the first and last iterations of the loop. we don't want to mark the prime (k=0 and sortaprime=1) and we don't want to be checking for if we've run over the edge all the time
		
		tokill = []

		
		for k in range(0, (N+1) // p, lcm):
			#input(k) if len(primes) > 3 else None
			for sortaprime in S:
			#	print("k=",k, "sortaprime=",sortaprime)
				#i = p*(k + sortaprime)
				i = mul(p, k, sortaprime)
			#	print(i) if i < 100 else None
				if i >= N+1: #make this faster by loop unrolling, since this check only matters for the last iteration
			#		print("breaking, p=",p,"k=",k,"sortaprime=",sortaprime)
					break
								
				if state[i] != 0:
					print("bad!", i, "is already marked as", state[i])
				state[i] = p
			#print()
			
		#the ones to kill should be [p*s for s in S where s < lcm//p], i.e. one for each entry in S that is under the limit lcm//p (note lcm = product of all primes up to but NOT including p)
		#lcm // 
		#input(("tokill=",tokill))
		#S = [e for i,e in enumerate(S) if i not in tokill]
		#if p == 2:
		#	S = [
		
		#for i,e in enumerate(tokill):
		#	del S[e-i]
		#input(((min(lcm,N) - p**2)/p, len(tokill)))
		#S += [i for i in range(lcm, min(lcm*p, N)+1) if state[i] == 0] if primes else []
		
		#input("END OF LOOP") if p not in [3,5] else None
		
		#assert state[p] == p, "This is wrong, but it's how the algorithm is programmed right now"
		state[p] = 'x' #So set it right
		primes.append(p) #append after the main loop ftw
		lcm*=p
		
		print("loop %d took %0.2f" % (p, time.time() - t0))
	
	
	#print(primes[-1], N+1)
	primes += [i for i in range(primes[-1], N+1) if state[i] == 0]
	return primes

def wsieve(N):
	state = [0]*(N + 1)
	state[0] = -1 #fuck that guy
	state[1] = -1
	
	primes = []
	lcm = 1
	S = [1]
	
	#things in the list state[lastlimit:lcm] that 
	
	#[1] <-- 2
	#[1] <-- 3
	#[1,5] <-- 5
	#[1, 7, 11, 13, 17, 19, 23, 29] <-- 7 ( things in the list that are unmarked between 7 and lcm)
	
	#so something we know about S:
	#it goes [1] + prms + rest
	#where prms is the set of primes between p and p**2 (which we can snag immediately by the sqrt factor-checking theorem)
	#oo the thing is, S is bounded by N//p, so once we cross there we can stop scanning
	#EXCEPT if lcm < p**2
	#whcih is if p is 2, 3, 5 7
	#and uh for 2.. what is S? S is exactly [1] (i.e. no prime component, so
	#for 2, 2**2 = 4 > 1 = *  [empty product]
	#for 3, 3**2 = 9 > 2 = 2
	#for 5, 5**2 = 25 > 6=2*3
	#for 7, 7**2 = 49 > 30=2*3*5
	#but for 11, 11**2 = 121 < 210=30*7
	#
	#induction hypothesis: p**2 < lcm(p-1) for the previous ps
	#11**2 < 7*5*3*2
	#does this imply that the next one is too?
	#13**2 > 11**2
	#11**3 < 11*7*5*3*2
	#so we have 13**2 < 11**3 < lcm(13)
	#Does that hold in general?
	
	#49 > 30
	#7**3 > 7*30
	
	#in general... 2*3 > 5
	#2*3*5 > 2*3 > 5
	#2*3*5*7 > 2*3*5 > 5
	
	#lcm(p') = lcm(p)*p'
	#in which case there is no rest and S is just [1] + a subset of primes
	
	p = 0
	A = 0 #sum
	B = 0 #sum
	while p**2 < N:
		#t0 = time.time()
		
		#print(state[:50])
		p = state.index(0, p+1) #find the next prime in O(n) time
		#print(p)
		#print("found",p,"as prime")
		#at each step, we remove the first non-zero S, and add all unmarked terms in p**2..lcm
		#note: lcm might be less than p**2, but that only happens on.. p=2? because for p=3, p**2 = 9 and lcm = 6 and then it just keeps growing
		#c_ache = len(S)
		
		#idea: we can know the primes up to p**2 when we're at p, and the first entries of S will be all primes that are larger than our current one but less than p**2 (after that the guarantee is lost)
		#nb: range(p, N//p) ... <-- S is things that will be multiplied by p later, so p actually means p**2..N, or p**2 .. lcm*p???
		S = [1] + [i for i in range(p, min(lcm, N//p)+1) if state[i] == 0]
		#so, S only gets slow when it gets large, however this A) happens rapidly
			#almost all the work is being done in generating S.
			#which is dumb because A) S doesn't need to be totally regenerated each time
		A+=min(lcm, N//p)+1 - p
		#print("length to scan:", min(lcm, N//p)+1 - p)
		B+=max(min(lcm, N//p)+1 - p**2, 0)
		#print("length to scan with improvement:", max(min(lcm, N//p)+1 - p**2, 0))
		#print(len(S))
		
		#print()
		#input(("p=",p,"lcm=",lcm))
		#input(primes)
		#zx = [s for s in S if s < p**2]
		#input(("zx =",zx,len(zx)))
		#input(("S=",S[:100],))
		#input(state[:100])
		
		
		#i feel like this would be faster with judicious use of squares
		
		#if you unroll the first loop you can also be scanning for the new bitches there
		
		#todo: unroll the first and last iterations of the loop. we don't want to mark the prime (k=0 and sortaprime=1) and we don't want to be checking for if we've run over the edge all the time
		
		#up to a certain point, S is all primes?
		
		#state[p] = 'p'
		#for sortaprime in S[1:]: #skip [1], because that's the prime
		#	state[sortaprime] = p
		for sortaprime in S:
			for i in range(p*sortaprime, N+1, p*lcm):
				#print("p=",p,"i=",i, "sortaprime=",sortaprime)
				#i = mul2(p, m) #theory: multiplication is slower than addition, better to step step by step by step
				
				#if state[i] != 0:
				#	print("bad!", i, "is already marked as", state[i], "but we're doing it as", p, "(and m=",0,"sortaprime=",sortaprime,")")
				#	input()
				state[i] = p
		
		#assert state[p] == p, "This is wrong, but it's how the algorithm is programmed right now"
		state[p] = 'x' #So set it right
		#state[p] = 0 #So set it right XXX this will break the generation of S
		primes.append(p) #append after the main loop ftw
		lcm*=p

		#print("loop %d took %0.2f" % (p, time.time() - t0))
	
	
	#print(primes[-1], N+1)
	#input(("Proportion we actually only need to scan with prime-saving improvement", int(B/A * 10**4)/100))
	primes += [i for i in range(primes[-1], N+1) if state[i] == 0]
	return primes
	#return [i for i in range(2, N+1) if state[i] == 0]


def go():
	N = 10**6
	r = wsieve(N)
	#import pickle
	#pickle.dump(r, open("%dprimes.pickle" % N, "wb"))
	#print(r)

profile.run("go()", sort=1)
		
