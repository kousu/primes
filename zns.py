#zns.py
#by <nick@kousu.ca> 2011.11.18
#
#unfinished code, but useful so I'm posting it
#Do whatever you want with it, but standard no
#warranty and you-must-credit-me terms apply.
#(and if you do anything interesting, I'd appreciate being told!)
"""
 stuff to do with Z_n* = U(n), the group of elements coprime to n, mod n.
  if you don't know what this is, see http://wikipedia.org/wiki/Multiplicative_group_of_integers_modulo_n
 and a certain subset of those groups: those which are on a product of primes U(2*3*5*...*p)

 This code is based on an observation about prime sieves:
  If you have crossed out everything that is a multiple of the first k-1 primes,
  then when crossing out the multiples of the next prime you can skip everything that,
    e.g. when doing p=5 (k=3), you skip 10, 15, 20, 30, 40, ... because 10=2*5, 15=3*5, 20=2*10, 30=3*10, 40=2*20, ... so they've already been done
    more generally, say you are crossing off p. in the basic prime sieve you go:
	p, 2p, 3p, 4p, ..., pp, (p+1)p, (p+2)p, (p+3)p, .....
	but you needn't do 2p, 3p, 4p....(p-1)p, because by the theorem about factor checking (you only have to do up to the sqrt)
        all multiples of 2, 3, 4, ... p-1 have already been marked (if a number has factors at least one is less than the sqrt of it, so if any number less than p**2 has a factor its factor will be less than p, all of which have already been sieved out by design)
	so the list is just
	1p, pp, (p+1)p, (p+2)p, (p+3)p, ...
	(I'm leaving in the 1p for a reason that only becomes clear as I explain what's going on)
 	but! there's more! some of the (p+i)s will have already been done as well. For example, a first refinement might be to skip every other one:
		1p, pp, (p+2)p, (p+4)p, (p+6)p, ... since the 2s have already been marked off ((lemma: in this case, p>2 so p is an odd prime so p+1, p+3, p+5, ... are even (and can be erased)))
		in fact, we should also be able to skip the 3s, 5s, 7s, ....
		but what is the system here?
      Let's look at instead of what we're crossing out, what we are crossing in, e.g. for p=5 again we only do:
	5x1, 5x5, 5x7, 5x11, 5x13, 5x17, 5x19, 5x23, 5x25, 5x29, 5x31, 5x35, 5x37, 5x41, 5x43, 5x47, 5x49
	your first guess might be "look! primes!" which is tantalizing, and it was mine too, but
	some aren't, e.g. 5**3, 5**2*7,5*7**2    (there is another pattern here, which is that the only new ones are ones of primes larger than, but that doesn't help much in sieving since we don't know those primes 'yet' (or maybe we do, up to a point))
      But take another look, there's an easy two-beat pattern going on: 1+4=5, 5+2=7. 7+4=11, 11+2=13, .... 31+4=35, 35+2=37
       So here is what is actually going on: these numbers are members (or, technically, 'representatives') of
       the unit group U(2*3) = {[1],[5]}, which is all numbers in Z_6 (that is, the integers mod 6) that are *coprime* (i.e. are not a multiple of) 2 or 3
        In mod 6 (i.e. mod 2*3)
         [1] = {...,-11,-5,1, 7,13,19,25,31,37,43,49,...} and
         [5] = {..., -7,-1,5,11,17,23,29,35,41,47,51,...}
	and these (well the positive side anyway) are exactly the multiples of 5 that will have been unmarked once we get to 5.
	the reason for this is that there is a clock-tick problem (which should translate immediately for you into least-common-multiples, if it doesn't email me and I'll try to point you on the right path :D)
           going on here. we tick off all the 2s, then all the 3s, then all the 5s, ... but at the product of all of these they meet up like planets aligning..and then trottle off again and swing around, until the next time they all meet up which is exactly the next multiple up. Further, the ones they miss in the first cycle (which is what U(2*3*...*[k-1th prime]) is defined as) will be the ones they miss in the second cycle, but shifted by the lcm of the primes.
	
   So that is where the line "lcm = pfac" comes from. And some other stuff. Does any of this make sense?

   To try this out you will need a source of primes (this is my test code, not my prime sieve code),
    which is this file: http://kousu.ca/software/100000primes.pickle   
"""

import time

def units(N):
	"compute U(N) directly"
	if N == 1: return [1] #special case bug patch. don't use!
	return [i for i in range(N+1) if coprime(N, i)]

def coprime(a,b):
	"return whether a and b are coprime"
	"two numbers are coprime if they have no common divisor (except 1, since 1 is a common divisor for everything"
	#there's gotta be a more efficient way to do this
	return gcd(a,b)==1

def gcd(a,b):
	"compute the greatest common divisor of a and b"
	#BUG: gcd(1,0) = 1
	if a>b:
		a,b = b,a
	if a==0: return 0
	
	while a>0:
		if a>b:
			a,b = b,a
		a,b = b-a, a
		#print(a,b)
	
	return b
	


import db
primes = db.primes

def pfac(k):
	"compute the product of the first k primes"
	#this should probably be memoized, but meh
	if k <= 0: #product of nothing is 1
		return 1
	return primes[k-1] * pfac(k-1) #primes[k-1] because the 0th prime is the 1st prime

lcm = pfac


def ephi(k):
	"compute euler's phi function on pfac(k)."
	"If this code is right, ephi(k) == len(kunits(k))"
	if k == 0:
		return 1
	return (primes[k-1]-1) * ephi(k-1) #primes[k-1] because the 0th prime is the 1st



kunits_memo = {}
def kunits(k):
	"generate U(lcm(k))"
	"notation: X_ means 'previous value of X'"
	
	if k in kunits_memo: return kunits_memo[k]
	
	#this should probably be memoized, but meh
	if k == 0: #p=2 => U(2) = {[1]}
		return [1]
	
	p = primes[k-1]
	U_ = kunits(k-1)
	
	#print("p:", p, "U_:",U_)
	#take the previous one and multiply it out until we win?
	L = lcm(k)
	#we need to get to L
	#we have
	L_ = lcm(k-1)
	#so we need to multiply out
	#actually we need to multiply out exactly primes[k] times
	#okay, so now we need to filter intelligently
	#it will only
	
	#print("(%d) U_:" % p, U_, L_) 
	Uish = [(u_ + k*L_) for k in range(p) for u_ in U_] #reasoning: multiply U_ out (exactly p times!) to get all elements between 0 and 2*3*...*p_*p that are coprime to 2*3*...*p_
	
	#then erase those elements which are exactly multiples of p and no other
	#(which for some reason are generated by U_ as well?????_
	#whores = [(u_,k) for k in range(p) for u_ in U_ if (u_+k*L_) % p == 0]
	#print("(%d) whores:" % p, whores)
	#ps = [x for x in Uish  if x%p==0]
	
	#there is very much structure here...
	
	#oh dear, a bad case: p=2 has lcm=2. in all other cases p!=lcm but here it does so it FUCKS UP SHIT GOOD
	
	#bad = [(u_*p % L_, u_*p // L_) for u_ in U_] #...where did this come from? why does this coincide?
	#print("(%d) bad:" % p, bad)
	
	#indexes = [1]
		
	#t0 = time.time()
	#for u_ in U_:
	#	Uish.remove(p*u_)
	#t_rem = time.time() - t0
	#print("took %0.9fs for getting rid of %d %ds" % ((t_rem), len(U_), p))
		
	#instead of doing that shit..
	D = weirdfunction(k-1) #XXX totally inefficient #definitely k-1
	U = []
	#pp(D) #D should be the same as whores and bad
	
	#take the list of things to cross, which are p*u for u in U_ (last U-nit group)
	
	#t0a = time.time()
	U = []
	#for base in range(0, p*L_, L_):
	#	Ux = U_[:] #clone
	#	for bad in D.get(base // L_, []):
	#		Ux.remove(bad) #<-- quadratic!!!!!
	#	U.extend(u+base for u in Ux)	
	U = [u+level*L_ for level in range(p) for u in sorted(set(U_)-set(D.get(level,[])))]
	#hmm, the set-tiness sometimes misorders things.. so we need to sorted()
	#t_cons = time.time() - t0a
	#print("Took %0.9fs to construct U" % (t_cons))
	#print("ratio:", t_rem/t_cons, t_rem > t_cons)
	#for level in range(p):
	#	print("\tU_:", U_)
	#	#print("\tD[%d]:" % level, D[level])
	#	S = sorted(list(set(U_)-set(D.get(level,[]))))
	#	print("\t", level, S)
	#	U += [u+level*L_ for u in S]
	#	print()
	
	#print("U:", U)
	#print("Uish:", Uish)
	#assert sorted(U) == sorted(Uish)
	
	#segment U(2*3*5*7) into sections mod 11
	#then these sections correspond to thingsies:
	#if thing is a mod 11, then it is a mod 
	
	#U = []
	#print(indexes)
	#for j in range(len(indexes)):
	#	U += Uish[indexes[j]-1:indexes[j+1]]
	#U = Uish
	#print("-"*50)
	if k-1 in kunits_memo: del kunits_memo[k-1] #HACK: delete the previous memoization to save memory
	kunits_memo[k] = U
	return U
	

def weirdfunction(k):
	"split the unit group in a weird way that seems to have applications to sorting out"
	if k == 0: #patch. in case for the first thing, lcm=1 which makes divmod behave badly. It writes 2=2*1 + 0 when I want it to write 2=1*1 + 1
		return {1: [1]}
	#(1,1) corresponds to 1*(1+1) = 2*1 + 0 ~= (2,0)
	#U = units(lcm(k))
	U = kunits(k)
	D = {}
	for u in U:
		q,r = divmod(primes[k]*u, lcm(k))
		if q not in D:
			D[q] = []
		D[q].append(r)
	return D
		

def pp(D):
	for d in D:
		print(d, "=>", D[d])

def ppl(l,n=200):
	"format a list, truncated"
	"takes prints the first 3/4s of the result from the front, the last quarter from the back"
	if len(l) < n:
		return str(l)
	else:
		front = l[:n*3//4]
		back = l[len(l)-(n*1//4):]
		#
		join = lambda l: str.join(", ", map(str,l))
		dots = int(100/5*(1 - n/len(l))) #one dot for every 5 percent of elements skipped
		#we skip
		#(len(l) - n) / len(l)
		#or, 1-n/len(l)
		return "[%s, %s, %s]" % (join(front), "."*dots, join(back))

def ppfac(k):
	"'pretty' p-fac of k. give a string that is the multiplication done to get lcm(k)"
	if k == 0: return "1"
	return str.join("*", map(str, primes[:k]))

if __name__ == '__main__':
	#for k in range(7):
	#	print(lcm(k), ephi(k))

	for k in range(11):
		l = lcm(k)
		input("[%d] Ready to compute U(%d)]" % (k, l))
		t0 = time.time()
		a = kunits(k)
		print("took %0.4fs to kunits" % (time.time() - t0))
		b = units(l)
		
		print(" "*2 + "Computed unit group by a) kunits(), b) brute force search:")
		print(" "*4, "U(%s) =" % ppfac(k), ppl(a))
		print(" "*4, "U(%s) =" % ppfac(k), ppl(b))
		print(" "*4, "Lengths:", len(a), len(b))
		print("Do the two match? %s" %  ["**NO**", "yes"][a == b])
		print() #print a newline
