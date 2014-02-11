#dbgsieve.py
"this is the file that generates fancyfresh"

#other idea:
#ragged-edged algorithm
#multiply all the primes known so far up
#2
#2,3 -> [p,p,2,0,2*3] this tells us that 5 is prime.
#2,3,5 -> [p,p,2,p, 2*3, 0, 0, 0, 0, 0, 0, 0, 0, 3*5] -> [p,p,2,p, 2*3, 0, 2, 0, 2, 0, 2, 0, 2, 3*5]
#						    -> [p,p,2,p, 2*3, 0, 2, 3, 2, 0, 2 & 3 :(, 0, 2, 3*5]
#this tells us that 7,11,13 are prime (why? because they are less than 15 so if they have a factor their factor must be less than
#    sqrt(15) is 3 < sqrt(15) < 5 since sqrt(25) > sqrt(15) and sqrt(9) < sqrt(15)
# so in other words they must have a factor that is 2 or 3
# but we've checked all those
#do 7
#7*5 = 35
# -> [p,p,2,p, 2*3, p, 2, 3, 2, p, 2 & 3 :(, p, 2, 3*5,       0,0,0,0,0,    0, 0, 0, 0, 0, 0,        0, 0, 0, 0      0,0,0,0,       7*5]
# 2 -> [p,p,2,p, 2*3, 0, 2, 3, 2, 0, 2 & 3 :(, 0, 2, 3*5,       2,0,2,0,2,    0, 2, 0, 2, 0, 2,        0, 2, 0, 2      0,2,0,2,       7*5]
# 3 -> [p,p,2,p, 2*3, 0, 2, 3, 2, 0, 2 & 3 :(, 0, 2, 3*5,       2,0,2,0,2,    0, 2, 0, 2, 0, 2,        0, 2, 0, 2      0,2,0,2,       7*5]
  #notice: the previous one was an odd multiple of 3 (it would have to be, it can't be) and 3*3 is done and 3*5 is done.. the next one is 3*7

#so this gives us that these are prime:
#since if they have a factor it must be 2, 3 or 5 but we've covered all those mulitples already

import time

class RaggedArray(list):
	"fake out a ragged array, matlab style"
	def __setitem__(self, i, v):
		pass
		self+=[0]*(i+1 - len(self))
		list.__setitem__(self, i, v)
	def __getitem__(self, i):
		if i >= len(self):
			return 0
		return list.__getitem__(self, i)



def factor(f, p):
	return "%d*%d = %d" % (f/p, p, f)

def products(q, p):
	return "%d*%d = %d" % (q, p, q*p)

#Two algorithms calling: one where you do the entire array at once (i.e. mark all the twos, then all the threes) and one where you only do some subrange at a time (so that you needn't hold the whole array at once)
#and in both, be clever about only marking the composites you need to mark

import math

def factorbackwards(q):
	"q should be int"
	
	#print("recursing")
	if q in primes:
		return str(q)
	for p in reversed(primes): #idea: get rid of the largest factors first. this does mean all the primes larger than sqrt(N) (which is most of them!) will have to be skipped. a better algorithm filters those out first (e.g. using a binary search) but I don't want to write one
		#waiiiit, either we cull to checking sqrt(q) or we can check. the sqrt(q) check only says if q is composite it will have *a* factor <sqrt, not that all its factors are..
		#hmm.. if you take the average run time..half of all numbers are 2s, a third are 3s
		if p > q: continue #so just skip those instead
		#print(p)
		if q % p == 0:
			#print(p)
			return "%s*%d" % (factor(int(q/p)), p)
	return str(q)


def factorforwards(q):
	"q should be int"
	
	#print("recursing")
	for p in primes:
		if p**2 > q: break #so just skip those instead
		#print(p)
		if q % p == 0:
			#print(p)
			k = 0
			while q % p == 0:
				q /= p
				k += 1
			
			q = int(q) #it's important to send ints into factor
			s = "%d^%d" % (p,k) if k > 1 else "%d" % p
			if q > 1: #don't recurse if we're down to 1
				s += " * " + str(factorforwards(q))
			return s
	
	return str(q)

factor = factorforwards

def Time(f, *args):
	import time
	t0 = time.time()
	r = f(*args)
	t1 = time.time()
	return t1 - t0

def testfactoring():
	"for the current setting of primes, compute the average run time across all"
	""">>> dbgsieve.test()
	(3.7810157087481856e-05, 0.0007453257714244559)
	"""
	F, B = 0, 0
	
	for i in range(2, primes[-1]**2):
		F += Time(factorforwards, i)
		B += Time(factorbackwards, i)
	return F / (primes[-1]**2 - 1), B / (primes[-1]**2 - 1)



def sieve(N):
	state = [0]*(N+1)
	state[0:2] = [-1]*2 #fuck those guys
	
	global primes
	global fancyfresh
	primes = []
	fancyfresh = {}
	t0 = time.time()
	while not primes or primes[-1] <= math.sqrt(N):
		try:
			p = state.index(0)
		except ValueError:
			break
		state[p] = 'p'
		primes.append(p)
		print("Found %d as prime" % p)
		print(primes)
		fancyfresh[p] = []
		for i in range(p**2, N+1, p):
			if state[i] == 0:
				
				#print("Marking %d=%s" % (i, factor(i))) if p > 2 else None
				fancyfresh[p].append(i)
			#else:
			#	print(i)
			state[i] = p
		print()
	print("Done marking composites (%0.2fsecs), now collecting primes" % (time.time() - t0))
	t0 = time.time()
	initp = p
	while True:
		try:
			p = state.index(0, p) #the , p makes a huge difference, difference between O(n) and O(n^2)
		except ValueError:
			break
		primes.append(p)
		state[p] = 'p'
	#primes = [i for i,e in enumerate(state) if e=='p']
	t1 = time.time()
	print("Took %0.2fs to search %d ints" % (t1-t0, N-initp))
	return primes



sieve(50000*16)

def diffs(l):
	return [b-a for a,b in zip(l, l[1:])]

for p in [2,3,5,7,11]:
	print([x//p for x in diffs(fancyfresh[p])[:100]])

def lsieve(N):
	#hmm.. the step for this is identical to the stop condition for the normal sieve: stop once you've done up to sqrt(N), everything between there and root(n) unmarked will be prime
		#that bodes well for incremementalizing this
	state = [0]*(N+1)
	primes = [2]
	at = 0 #which prime we are crossing off right now
	state[0:2] = [-1]*2 #fuck those guys
	
	#when can we decide we've marked all the composites?
	#a number is prime if when we've crossed out all the composites
	# i is prime if we've crossed out all factors up to sqrt(i)
	# and
	# so if i in p**2 .. (p_+1)**2 then if we cross out all the primes up to sqrt(i) which is 2, 3, 5, ... p?
	# so...... we cross out all the composites and then anything left is prime
	iterators = {2: 2} #store iterators so we don't have to guess (well, compute, with modular arithmetic) where the "next k*q > p**2" is
	state[2] = 'p'
	state[3] = 'p'
	primes.append(3)
	while primes[at]**2 < N:
		at+=1
		p = primes[at]
		print("Working on p=%d" % p)
		iterators[p] = p
		
		for q in primes[:at]:
			print("  sub-prime: q=%d" % q)
			#print(iterators[q])
			#mark things as not prime
			while iterators[q]*q <= p**2 and iterators[q]*q <= N:
				if state[iterators[q]*q] != 0:
					print("    bad: [%s]" % products(iterators[q], q))
				else:
					print("    good: %s" % products(iterators[q], q))
				state[iterators[q]*q] = q
				iterators[q] += 1
			#^ all these steps above are... less than p**2? iterators[q] is never larger than it? why? oh because i told it so...
		
		print(primes)
		#collect new primes
		for i in range(primes[at-1]**2, min(primes[at]**2, N+1)):
			if state[i] == 0:
				primes.append(i)
				print("  Found %d as prime" % i)
				state[i] = 'p'

		#print(state)
		print(primes)
		
		input("[enter]")
		print()
	return primes
