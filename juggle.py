'''
This program illustrates one way to solve the
JuggleFest problem for Yodle.

http://www.yodlecareers.com/puzzles/jugglefest.html

The list of data for this assignment consists of: 
	- 12,000 jugglers
	- 2000 circuits 

In jugglefest.txt each juggler has 10 preferences 

Given 12K jugglers and 2K cicuits, we know to assume
there will be 6 jugglers accepted into each circuit. 

1) read the jugglers.txt line by line and convert the data
For the circuits we need to create a matrix to compute the dot
products. Then once we are getting juggler data we can start
computing the dot products right away. 

@ def readFile(file)

 
       CIRCUITS       JUGGLERS  
    ------------------------------
      H  E  P    H  E  P    PREFS
    __|__|__|____|__|__|______|____
1) | [2, 1, 1]  [3, 9 ,2, [2, 1, 0]]
2) | [2, 1, 1]  [3, 9, 2, [2, 0, 1]]
3) | [2, 1, 1]  [3, 9, 2, [1, 2, 0]]
4) | [2, 1, 1]  [3, 9, 2, [2, 0, 1]]
5) | [2, 1, 1]  [3, 9, 2, [0, 1, 2]]
'''
import sys
import re
from itertools import izip

cs = [] #circuits
cm = [] #circuits with jugglers
dp = [] # juggler dot products

def readFile(f):

 	global cs, cm, dp

	top = True

	for l in f: 

		if l == '\n':
			top = False
			continue			 

		l = re.findall(r'\d+', l) #only use the int chars
		l = [int(i) for i in l]   #convert the chars to ints

		if top:
			cs.append(l)  #puts the circuit in the list of circuits
			cm.append([]) #adds an empty array for the circuit matches
		else:

			
			#l[0] = juggler name
			#l[1] = juggler H
			#l[2] = juggler H
			#l[3] = juggler H
			#l[4:] = juggler circuit preferences
			
			#store the dot products for this juggler
			#in a list that will be passed to cm
			jglr = []
			jglr.append(l[0])   
			for c in l[4:]:

				#compute the dot product
				d = (l[1] * cs[c][1]) + (l[2] * cs[c][2]) + (l[3] * cs[c][3])
				
				#add a (circuit, product) tuple for this juggler
				jglr.append( (c, d) )

			#insert the juggler into its first preference
			#cm[l[4]].append(jglr)
			#print "inserting {0} into pref {1} ".format( jglr, l[4])
			

			dp.append(jglr)

	for d in dp:
		print d
	'''
	Loop through the dot products, preference by preference
	append the jugglers that prefer this circuit first. Before
	looping the next preference, count the current jugglers
	if we have too many, sort them and remove the ones we want
	if we have just enough, sort them and remove the all
	if we dont have enough, skip to the next preference, but 
	check that the product is not higher than the lowest one 
	we found in the first preference. Keep skipping to the
	next preference untill we have enough. Remove an selected
	jugglers

	'''
	temp = []
	dp = sorted(dp, key=circ)
	ii = 1
	attempts = 0
	expected = 4

	#we start searching for jugglers who prefer circuit 0
	#if we find 
	#while len(dp) > 0:
	for do in range(expected):
		#temp = [ temp.append(d) for d in dp if d[ii][0] == ii-1 ]

		#loop through all of the dot products
		#find jugglers who prefer this circuit 
		#the most first. then swtich to jugglers
		#who prefer this circuit second most and
		#if we still have not found enough, find
		#the jugglers who prefer this circuit third
		#most. We do this for however many circuits
		#may by allowed to prefer

		for d in dp:
			#
			if d[ii][0] == do:

				temp.append(d)
				print "Found, {0} for circuit {1}".format(d, d[ii][0]) 


		temp = sorted(temp, key=prod, reverse=True)

		#dp = [ dp.remove(e) for e in temp[:4]]

		for e in temp[:4]:

			print "Removing {0} from dp".format(e)
			dp.remove(e)
			cm[do].append(e)

		temp = []

	for d in dp:
		print d

	for z in cm:
		print z
		#[ ii+=1 else sys.exit("Fuck Off") if attempts >= 5 ii = 1 if ii >= 3 ]
		'''
		if ii >= 3:
			ii = 1
			attempts +=1
			if attempts >= 10:
				for d in dp:
					print d
				
				sys.exit("Failed to do the job mother fucker")
		else:
			ii+=1
		'''

		#print "Finished looping by circuits"
	'''
	for t in cm: 
		expected = 4

		if len(t) > expected:
			print "To many jugglers"

			# sort the list of jugglers to keep highest
			t = sorted(t, key=prod, reverse=True)

			# loop the remaining jugglers
			for u in t[expected:]:

				#move the juggler to its seecond preference

				print u

		if len(t) == expected:
			print "Need to sort jugglers"
		
		if len(t) < expected:
			print "Not enough jugglers"

		print t
	#print cm
	'''

def circ(i):
	return i[1][0] # accessing the (c, value)

def prod(i):
	return i[1][1]
'''
2) compute the dot products for each juggler

        	1st       2st       3st       

	1	[ (2, 230), (1, 123), (3, 12) ]

This result needs to be used somehow? Since the first preference is 2
we will add J1 to circuit 2, but this might change later

We continue repeating these steps until all jugglers have been put into 
the circuit they prefer first

This new matrix is only cares about the value for each juggler that matches itself. 
So for the above example, Circuit 2 has all of J1's info, but only cares
about the value 230. 

First we count how many jugglers we have in this circuit. If we have too many or just enough,
we sort the jugglers by the value we care about. For the remaining jugglers we look at their 
next preference and we move them to that circuit, but this might change again too

What if there are not enough jugglers in this circuit? 

For example lets just say that after computing the dot products, the first circuit only has 
1 juggler and we need to find the remaining jugglers that might prefer this as a second option. 
It is too early for that because the jugglers need to be grouped by their first preferences
from the start. 

My answer to the above question is simple. If there are not enough jugglers already, we 
can skip sorting and moving and just move on, but for the sake of it, we log this circuit
so that we know we need to come back to it once we have reached the end. This works
because by the time we reach the end, the circuit that was missing jugglers before, either
has too many or still not enough. We go back to these known circuits and check how many
jugglers there are. If there still aren't enough we skip it again; logging it again too. 
If there are too many we do a sort and move the remaining jugglers to their next preference. 

Finally, when we reach the end and the log is empty, we are done finding the circuits. 

Now we just need to create a file line by line containing all the circuits and selected jugglers. 

'''














def readListToDict(l, k):

	if k == 0:
		#remove the C and newline chars that start each line
		l = [ re.sub(r'(C |\n)', '', h) for h in l ]

		#split each line where there is a space
		l = [ re.split(" ", h) for h in l ] 

		for i in l: 
		# add a circuit with key:values
			circuits[i[0]] = {
						"H":int(i[1].split(":")[1]),
						"E":int(i[2].split(":")[1]),
						"P":int(i[3].split(":")[1])
					}
	else: 
		#remove the J and newline chars that start each line
		l = [ re.sub(r'(J |\n)', '', h) for h in l ]

		#split each line where there is a space
		l = [ re.split(" ", h) for h in l ] 

		#print g[0] = ['C0', 'H:7', 'E:7', 'P:10']
		for i in l:
			# add a juggler with key:values
			jugglers[i[0]] = {
						"H":int(i[1].split(":")[1]),
						"E":int(i[2].split(":")[1]),
						"P":int(i[3].split(":")[1])
						}
			for j in i[4:]:
				jugglers[i[0]]["C"] = j.split(",")

def sepList(f):
	global cList, jList

	a = [ (l.replace(" ", ","),) for l in f ]
	#print f
	#top = True;
	
		#print l.split(" "),
	#	if top:
	#		if l != '\n':
	#			cList.append(l.split())
	#		else:
	#			top = False
	#	else:
	#		jList.append(l.split())
	
	#remove the C and newline chars that start each line
	#cList = [ re.sub(r'(C|H|E|P|:|\n|)', '', h) for h in cList ]
	#jList = [ re.sub(r'(C|J|H|E|P|:|\n|)', '', h) for h in jList ]

	#cList = [ re.sub(r'()', '', h) for h in cList ]
	#jList = [ re.sub(r'()', '', h) for h in jList ]
	#jList = [ re.sub(r'(J,|\n)', '', h) for h in jList ]
	#split each line where there is a space
	#jList = [ re.split(" ", h) for h in jList ]
	#cList = [ i.pop() for i in cList ]
	#jList = [ i.pop(0) for i in jList ]

	#jList = [ y.pop(0) for x in jList for y in x]
	
	#print cList
	print a[2]
	#print jList[0][4].split(",")

def highJug():

	print dotProds

	for j in dotProds:
		if '1' in jug:
			print jug

def setDots():
	# loop by circuit count for jugglers; their all the same, use the first one for reference
	for i in range(len(jugglers['J0']['C'])):
		#loop all jugglers
		for ii in range(len(jugglers)):
			j = "J"+str(ii)

			jh = jugglers[j]['H']
			je = jugglers[j]['E']
			jp = jugglers[j]['P']
			jc = jugglers[j]['C']

			ch = circuits[jc[i]]['H']
			ce = circuits[jc[i]]['E']
			cp = circuits[jc[i]]['P']

			dot = (jh*ch)+(je*ce)+(jp*cp)

			t = i in dotProds

			if i:
				dotProds[j][i] = { jc[i] : dot }
			else:
				dotProds[j] = { i : { jc[i] : dot }}

#iterate the dot products by juggler
#keep track of how many matches have been found for this circuit
#if the first key is lacking dots, move to the next key
def matchLookup(currentCircuit, expectedMatchCount):

	global high, matchCount, currentColumn, lastMatch, match, trash
	#12,000 jugglers
	#2000 circuits 

	#each circuit takes in 4-6 matches
	#each juggler has 4-10 preferences


	#repeat 4-6 times; limits the Jugglers allowed in the Circuits
	for k in range(expectedMatchCount):

		#for each juggler; referenced by the dot product dict count
		#testing ranged from 1-10, finale goes 1-12000
		for i in range(len(dotProds)):
			j = "J"+str(i)
			c = "C"+str(currentCircuit)

			if len(trash) > 0 and c in trash: 

				last =  dotProds[trash[len(trash)-1]][currentColumn][c]

				print "Last :",last
			
			#run through all of the values for key,key,C overwriting the high score if higher
			if c in dotProds[j][currentColumn] and dotProds[j][currentColumn][c] > high and j not in trash :
				#keep overwriting the high score value
				#but wait to use it after iterating all 
				#of the dots and if colums for matches
				high = dotProds[j][currentColumn][c]
				match = j

		#This ends one of 4-10 iterations to find the best Jugglers for Circuits
		#Use the match, high that was created above. This is the first circuits, first Juggler
		print "Picked Juggler : {0}, with High Scrore of : {1} ".format(match, high)
		
		print "Match count : ", matchCount
		#do some cleanup; increment match count, reset the high score and add match to trash
		matchCount += 1
		high = 0 
		trash.append(match)
	
	#make sure a match was found
	#if we're missing a match call this function again 
	if matchCount != expectedMatchCount and matchCount != 0:
		currentColumn += 1

		print "No match found, jumping to next column"
		matchLookup(currentCircuit, expectedMatchCount)

	else:
		print "Done"


def findMatches(circuitCount, expectedMatchCount):

	for currentCircuit in range(circuitCount):
		
		matchLookup(expectedMatchCount, currentCircuit)

	cleanup(trash)

def cleanup(junk):
	# all the trash junks 
	for thing in junk:
		print "Deleting : ", thing
		del dotProds[thing]

def main(): 

	#seperate the circuits, jugglers and remove the space
	readFile(open("data.txt"))		
	#create the circuits dictionary
	#readListToDict(cList, 0)
	#create the jugglers dictionary
	#readListToDict(jList, 1)

	#setDots()

	#findMatches(3, 4)
	
if __name__ == "__main__":
    main()

