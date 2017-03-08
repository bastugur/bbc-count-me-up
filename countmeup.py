from collections import defaultdict as dd;
import pdb as debugger;
import time
import random
import pickle
import multiprocessing

from multiprocessing import Manager
from multiprocessing import Process

results = dd(int)
done=0

class User:
   def __init__(self, name):
      self.name = name
      self.votesCast = 0


def vote(user, candidateid):
	if(canVote(user)):
		results[candidateid]+=1
	else:
		print(user.name+" already voted 3 times")

def requestCount():
	for candidate in results:
		print(candidate,results[candidate])


def requestPercentage(results):
	start = time.time()
	for candidate in results:
		print candidate, 100*results[candidate]/sum(results.values())
	print "execution time", time.time() - start, "s."
	if(time.time()-start<=0):
		print("1 sec threshold satisfied")

def canVote(user):
	if user.votesCast<3:
		user.votesCast+=1
		return True;
	else:
		return False;
		
def createNewUser(name):
	return User(name);

def printSummary():

	requestPercentage()

def simulateLargeVotes():
	for x in xrange(0,10000000):
		randomCandidate = "candidate-"+str(random.randint(1, 5));
		vote( User("someone"),randomCandidate);
	with open('votes.pickle', 'wb') as handle:
	    pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

def calculateCandidate(pid,shared):
	target = ('candidate-'+str(pid+1))
	shared[pid+1]=results[target]
def requestPercentageMultiProcess():
	start = time.time()

   	jobs = []

   	manager = multiprocessing.Manager()
   	shared = manager.dict()

   	for i in range(5):
		p = multiprocessing.Process(target=calculateCandidate, args=(i,shared))
		jobs.append(p)
		p.start()
	for j in jobs:
		j.join()
	print "execution time", time.time() - start, "s."

	return shared

def main():

	#simulateLargeVotes()

	return requestPercentageMultiProcess()


results["candidate-1"]=0
results["candidate-2"]=0
results["candidate-3"]=0
results["candidate-4"]=0
results["candidate-5"]=0

results = pickle.load( open( "votes.pickle", "rb" ))
main()

