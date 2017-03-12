from collections import defaultdict as dd;
import pdb as debugger;
import time
import random
import pickle

import multiprocessing
from multiprocessing import Manager
from multiprocessing import Process
#Parallel libraries

#user class mainly for encapsulating the voteCast variable
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
	#serial implementation. That was the first code I wrote. Not currently in use.
	start = time.time()
	for candidate in results:
		print candidate, 100*results[candidate]/sum(results.values())
	print "execution time", time.time() - start, "s."
	if(time.time()-start<=0):
		print("1 sec threshold satisfied")

def canVote(user):
	#client side check. Not really important since the first/main check happens in the server side.
	#server.py line: 63
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
	#This wont be executed. I ran this one in order to simulate the votes earlier and saved it in a file
	for x in xrange(0,10000000):
		randomCandidate = "candidate-"+str(random.randint(1, 5));
		vote( User("someone"),randomCandidate);
		#User("someone") because it does not really matter who voted what, I still keep the username field in order to make the code flexible for future requirements.
	with open('votes.pickle', 'wb') as handle:
	    pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

def calculateCandidate(pid,shared):
	target = ('candidate-'+str(pid+1))
	#pid+1 instead of pid in order to avoid confusion such as thread 0 = candidate 1
	shared[pid+1]=results[target]

def requestPercentageMultiProcess():
	start = time.time()

   	jobs = []
   	#all processes will be kept in an array
   	manager = multiprocessing.Manager()
   	shared = manager.dict()
   	#global variable

   	for i in range(5):
   		#I decided to create 5 child processes that run simultanously. Each process is responsible for one candidate.
		p = multiprocessing.Process(target=calculateCandidate, args=(i,shared))
		#Each process also utilises the global variable shared in order to save the count result
		jobs.append(p)
		#Save the child process to the array
		p.start()
	for j in jobs:
		#Join the processes when the job is finished
		j.join()
	#Since we joined all the processes that are done. We now have only a single process going on.
	#The main thread is resposible for recording one single variable the sum of all votes.
	shared["Total Votes"]=sum(results.values())
	#Print the recorded time spent in the execution
	print "execution time", time.time() - start, "s."
	return shared.copy()


#Init data
results["candidate-1"]=0
results["candidate-2"]=0
results["candidate-3"]=0
results["candidate-4"]=0
results["candidate-5"]=0

#Pre-simulated data is saved as a local file in order to save some time.
results = pickle.load( open( "votes.pickle", "rb" ))
requestPercentageMultiProcess()


