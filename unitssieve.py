
import zns

#this method sucks
#because, like I thought, U blows up wayyyyyyyyyyyyy too quick

def sieve(N):
	k = 4
	U = zns.kunits(k)
	while U[1]**2 < N:
		k+=1
		#print(U[:50])
		print(len(U))
		print(U[1:U.index(U[1]**2)])
		U = zns.kunits(k)
		print()
	return U[1:U.index(U[1]**2)]


print(sieve(1000))
