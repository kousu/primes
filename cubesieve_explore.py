
#better cube sieve

#do cube sieveing!!!!1iodmoweksldjmgoilerfkdjmgijokldfjgnmijkdlmngd

#todo: some sort of skip-list structure. the Us are all the same but with some elements successively removed. can this be recorded efficiently somehow? like, for the runs that bits share, just say that it defaults to moving down?

import zns

from db import primes as RealPrimes

def sieve(N):
	primes = [2]
	state = [-1]*2 + [0]*(N)
	prime_i = 0
	p = 2
	upto = 2 #upto is one more than what has been sieved to
	while p**2 < N:
		#sieve up to square. 
		print(" -- %d -- " % p)
		#since everything up to p is already done, and everything up to the square is marked
		#everything unmarked up to the square is prime.
		for i in range(primes[prime_i-1]**2 if prime_i else p+1, p**2):
			if state[i] == 0:
				print("new ^2 prime:", i)
				primes.append(i)
		
		#goal Study regions:
		#p**3 < lcm < N <-- is this a real region? In the very lower end, lcm < p**3, e.g. for 2, 6 < 27, 30 < 125, ?
		#p**3 < N < lcm
		#N < p**3 < lcm <-- this is a real region, because lcm grows so fast
		
		#sieve up to p**3
		print(" -- %d**2 -- " % p)
		for e,q in enumerate(primes[:prime_i]):
			l = zns.lcm(e)

			for i in range(upto + (q - (upto % q)), min(p**3, N+1), q):
				#print(i)
				if state[i] == 0:
					#*missing note: ones from the pattern correspond to the ones taken out when generating the next unit group
					if q > 3:
						print("  %d] new: %d = %d*(%d[%d])  {[%d] <-- missing note}" % (q,i,q,l,(i//q) % l, (i//q) % l % (zns.lcm(e-1)) )) 
				#else:
				#	print("  %d| BAD: %d" % (q,i)) if q > 0 else None
				state[i] = q
			if q > 3:
				print()
			else:
				print("  %d] ...\n" % q)
		
		
		#efficiency: mark only multiples of primes!
		for q in primes[prime_i:]:
			l = q*p
			if q > p**2:
				print("uh oh, breaking because while marking cubethm composites got a %d > %d" % (q, p**2))
				break
			if l > N:
				continue
			assert l < p**3
			if state[l] == 0:
				print("  [%d*%d = %d]" % (p,q,l))
			state[l] = p
		
		
		#mark p**3 as not prime (it seems like this should naturally be marked some other place, the way p**2 is.., but it's not obvious to me where that should be)
		if p**3 < N:
			print("  [%d**3 = %d]" % (p, p**3))
			state[p**3] = p
		
		upto = p**3
		
		print(" -- %d**3 -- " % p)
		prime_i += 1
		p = primes[prime_i]
		print("-"*22)
		
		#print(primes)
		assert RealPrimes[:len(primes)] == primes or len(primes) > len(RealPrimes)
		#print("we know",len(primes),"primes") #if we get here the assertion passed



sieve(15000)
