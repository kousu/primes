
"""
NOTES NOTES NOTES
BREAKTHROUGH BREAKTRHOUGH BREAKTHROUGH

The set of ps to be erased from U(2*3*...*q*p) when constructing it from U(2*3*,....q) is precisely
 the set [p*u for u in U_] (where U_ is that previous Unit group we are building up from)


FURTHER, this set can be described in an eerily simple way by doing divmod(p*u, L)
 (except for L=1, in which case the correct result is [(1,1)] becauase

>>> [divmod(7*u, 30) for u in units(30)]
[(0, 7), (1, 19), (2, 17), (3, 1), (3, 29), (4, 13), (5, 11), (6, 23)]
>>> #this tells me that
... #7 = 7*(7+0*30) is bad
... #? = (19+30) is bad
... #  = (17 + 60) is bad
... #  = (1 + 90) is a 7
... #  = (29 + 90) is a 7
... #  = 13+120 is a 7
... #  = 11+150 is a 7
... #  = 23+180 is a 7
... (23+180) % 7



With this improvement 

"""


from zns import *

state = [-1]*2+[0]*300

for u in [1]: #reasoning: 1 is the empty product. also this gives the correct result
	input(("marking u=",u,"[p=2]"))
	for i in range(2*u, len(state), 2):
		state[i] = 2
state[2]=0

for u in units(2):
	#input(("marking u=",u,"[p=3]"))
	for i in range(3*u, len(state), 2*3):
		if state[i] != 0:
			print("double marking:", i)
		state[i] = 3
state[3]=0

for u in units(2*3):
	input(("marking u=",u,"[p=5]"))
	for i in range(5*u, len(state), 2*3*5):
		if state[i] != 0:
			print("double marking:", i)
		state[i] = 5
state[5]=0


for u in units(2*3*5):
	input(("marking u=",u,"[p=7]"))
	for i in range(7*u, len(state), 2*3*5*7):
		if state[i] != 0:
			print("double marking:", i)
		state[i] = 7
state[7]=0

for u in units(2*3*5*7):
	input(("marking u=",u,"[p=11]"))
		#indeed, these are prime:
"""('marking u=', 1, '[p=11]') #well except this of course
('marking u=', 11, '[p=11]')
('marking u=', 13, '[p=11]')
('marking u=', 17, '[p=11]')
('marking u=', 19, '[p=11]')
('marking u=', 23, '[p=11]')
('marking u=', 29, '[p=11]')
('marking u=', 31, '[p=11]')
('marking u=', 37, '[p=11]')
('marking u=', 41, '[p=11]')
('marking u=', 43, '[p=11]')
('marking u=', 47, '[p=11]')
('marking u=', 53, '[p=11]')
('marking u=', 59, '[p=11]')
('marking u=', 61, '[p=11]')
('marking u=', 67, '[p=11]')
('marking u=', 71, '[p=11]')
('marking u=', 73, '[p=11]')
('marking u=', 79, '[p=11]')
('marking u=', 83, '[p=11]')
('marking u=', 89, '[p=11]')
('marking u=', 97, '[p=11]')
('marking u=', 101, '[p=11]')
('marking u=', 103, '[p=11]')
('marking u=', 107, '[p=11]')
('marking u=', 109, '[p=11]')
('marking u=', 113, '[p=11]')
...
#the group of units continues past here, in fact it hits 11**2 right next
#but from the group of units for 2*3*5*7, we were able to generate part of the units for the next set units(2*3*5*7*11)
#we 'easily' (okay we're cheating here) generated the first batch which is the set of primes from 11 to 11**2
#and then we just need to also get... also get what? well if we want to units for the next batch
#


#the basic idea was use the primes for p..p**2 to get the primes in p**2..p**3, and repeat, right?
#where did it break down?
#it broke down because we didn't have a way to skip already-done ones in p**2..p**3
 #but now we should have a way, shouldn't we? by looking at the groups of units?

question: do we really need to look at the units strictly? what if we erase primes backwards?
	#like, erase all 11s first (which also erases some 7s, 5s, 3s and 2s) and then erase all 7s that weren't 11s and so on
	#the advantage is that we only need to add to our skiplist, not subtract, which should be easier.
	#you object: but we don't have
	#ah but we *do*. our upper limit is give by the p**2 rule.
"""
	for i in range(11*u, len(state), 2*3*5*7*11):
		if state[i] != 0:
			print("double marking:", i)
		state[i] = 11
state[11]=0
#TODO: put in a limit so it doesn't do |u|s that are beyond the size of the array..

for u in units(2*3*5*7*11):
	input(("marking u=",u,"[p=13]"))
	for i in range(13*u, len(state), 2*3*5*7*11*13):
		if state[i] != 0:
			print("double marking:", i)
		state[i] = 13
state[13]=0



print(state)

print([i for i in range(len(state)) if state[i]==0])
