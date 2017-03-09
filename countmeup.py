from collections import defaultdict as dd;
import pdb as debugger;
import time
import random
import pickle
import multiprocessing

from multiprocessing import Manager
from multiprocessing import Process

class User:
   def __init__(self, name):
      self.name = name
      self.votesCast = 0

results = dd(int)
users = dd(User)

done=0



def getUser(email):
	for user in users:
		if user.name == email:
			return user

def createUser(email):
	newUser = User(email)
	users[randomword(20)]=newUser
	print users
	return newUser

def vote(user, candidateid):
	if(canVote(user)):
		results["candidate-"+str(candidateid)]+=1
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


import random, string

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

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
	shared["Total Votes"]=sum(results.values())
	print "execution time", time.time() - start, "s."
	return shared.copy()



results["candidate-1"]=0
results["candidate-2"]=0
results["candidate-3"]=0
results["candidate-4"]=0
results["candidate-5"]=0

results = pickle.load( open( "votes.pickle", "rb" ))
requestPercentageMultiProcess()


