
import zns

#unitssieve: instead of actually sieving ourselves, just generate unit groups and use the fact that they always start with primes

#this is a more promising less sucky unitssieve:
#the trick is to check when the *end* of U is past the limit, instead of the start (guaranteeing that the limit-prime we need, the max prime < sqrt(N), is in the list)
 #then just 

#but a way in which it doesn't suck: *because* it blows up to quick, I sieve to a quintillion! (10**3)**5

#   
#...so it's going to blow up way too quick?
#once we know

#idea: instead of *actually* generating each U group and storing in memory, only store those that are skipped. Then to actually scan through any U group you will need ...k? steps checking back through the previous runs for what to avoid? maybe that's not any faster...

def sieve(N):
	k = 0
	U = zns.kunits(k)
	primes = [2, 3]
	while U[-1]**2 < N:
		k+=1
		U = zns.kunits(k)
		print(k, "~", len(U))
	print(U[0], U[-1])
	return U[1:U.index(U[1]**2)]

print("start")
P = sieve(1000000000000000)
print("done")
print(P)
