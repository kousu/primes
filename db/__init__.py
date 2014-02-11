
import os
import pickle

primes = pickle.load(open(os.path.join(*(__path__ + ["10000000primes.pickle"])),"rb"))


def ensure(pr):
	"make sure the given list of primes is correct, as far as we can tell"
	ln = min(len(primes), len(pr))
	assert primes[:ln] == pr[:ln]
