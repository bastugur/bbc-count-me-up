from collections import defaultdict as dd;
import pdb as debugger;
import time
import random
import pickle
from multiprocessing import Process


results = dd(int)


class User:
   def __init__(self, name):
      self.name = name
      self.votesCast = 0


def vote(user, candidateid):
	if(canVote(user)):
		results[candidateid]+=1;
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


def main():
	#simulateLargeVotes()
   	results = pickle.load( open( "votes.pickle", "rb" ))

   	
   	requestPercentage(results)
	'''
	ugur = User("Ugur")
	notugur = User("Not Ugur")

	vote(ugur,'candidate-1')
	vote(ugur,'candidate-2')
	vote(ugur,'candidate-1')
	vote(ugur,'candidate-1')
	vote(notugur,'candidate-5')
	vote(notugur,'candidate-5')
	vote(notugur,'candidate-5')
	'''

if __name__ == '__main__':
	results["candidate-1"]=0
	results["candidate-2"]=0
	results["candidate-3"]=0
	results["candidate-4"]=0
	results["candidate-5"]=0

	main()

