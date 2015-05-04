'''
Written by    : Ryan Alex
Date Created  : 4/29/15

This program illustrates one way to solve the
JuggleFest problem for Yodle.

http://www.yodlecareers.com/puzzles/jugglefest.html

The list of data for this assignment consists of: 
	- 12,000 jugglers
	- 2000 circuits 

In jugglefest.txt each juggler has 10 preferences 

Given 12K jugglers and 2K cicuits, we know to assume
there will be 6 jugglers accepted into each circuit. 

'''
import re 											#import the regex package

circuits 		= []								#list to hold all the circuits
circuitCount 	= 0 								#track total circuits created
jugglerCount 	= 0 								#track total jugglers created
hazeCount    	= 0 								#track overal hazing total

class Circuit:										#Class Object for circuits

	def __init__(self, data):
		global circuitCount

		self.t = data[0]							#circuit name value
		self.h = data[1]  							#hand eye
		self.e = data[2]							#endurance
		self.p = data[3]							#pizzaz
		self.matches = []							#the 4-6 matches for this circuit
		self.hasMatch = False						#track if circuit has match
		circuitCount+=1 							#track total circuits created

	def hazeInductee(self, j):						#haze an inductee; a juggler
		global hazeCount

		hazeCount +=1
		#print "Juggler {0} entering circuit {1} with value {2}".format(j.t, self.t, j.dpsValForIndex(j.sp))
		
		if self.hasMatch:
			
			#Initially I thought that I should consider the preference
			#that each juggler had, but that is wrong. Consider this question
			#based on the example for this test. Circuit 0's highest record is
			#J5:C0:161 and it is the highest match. The trick here is what happens
			#at scale; which in this case is represented by 1997 additional circuits
			#and 19,988 addition competitors. Suppose that there are 10 more added
			#jugglers right now and a few of them first prefer C2 and are higher
			#than J6:C2:128. What will happen if J6:C0:188 is forced to find it's
			#second circuit? It will head over to C1, but let's say C1 is full and 
			#31 is too high, it heads over to C0 and guess what? It beats J5. So now
			#Circuit 0's highest juggler is J6:C0:188. 

			self.isMatch(j)
		else:
			#print "Appending first juggler {0} to enter circuit {1}".format(j.t, self.t)
			
			self.matches.append(j)					#add the first juggler to this circuit
			self.hasMatch = True					#flip the swith for has matches only run 
												    #this once per circuit match

	def insertMatch(self, j, i):
		if i == None:
			self.matches.append(j)					#append the new juggler to the list
		else:	
			self.matches.insert(i, j)				#insert the higher match, bumping the rest down 1

		if len(self.matches) > 6:					#send extra jugglers to their next preference
			tj = self.matches[-1]					#copy the juggler
			self.matches.remove(self.matches[-1])	#remove the juggler for this circuit
			self.passJuggler(tj)					#send the juggler to its next circuit

	def passJuggler(self, j):						#pass juggler to its next preference
		if not j.sp >= len(j.dps)-1:				#make sure not to pass jugglers out of bounds
			j.sp +=1 								#increment the jugglers current preferred circuit
													#for the next loop after it's passed

													#pass the juggler to next circuit
			circuits[j.dpsKeyForIndex(j.sp)].hazeInductee(j)

	def isMatch(self, j):
		notFound=True								#keep track if no match is found
		for i in range(len(self.matches)):			#compare to all index
			
			#print "Val for J {0} compared to C {1}".format(j.dpsValForIndex(j.sp), self.matches[i].dpsValForCirKey(self.t))
			
			if j.dpsValForIndex(j.sp) > self.matches[i].dpsValForCirKey(self.t):# or j.dpsValForIndex(j.sp) < self.matches[-1].dpsValForCirKey(self.t):
				
				#print "Picked Juggler {0} with value {1} compared to {2}".format(j.t, j.dpsValForIndex(j.sp), self.matches[i].dpsValForCirKey(self.t))
			
				notFound=False						#flip the switch if found
				self.insertMatch(j, i)				#start inserting the match at index
				break

		if notFound:								#if no match was found looping
			self.insertMatch(j, None)				#the match will just be appended

	def cmnt(self):									#add up the matched juggler names
		t = 0 										#this is just used at the end to 
		for j in self.matches:						#print out something pretty
			t += j.t 								#adds to the total name count
		return t 									#return the total

class Juggler:										#Class Object for jugglers
	def __init__(self, data):
		global jugglerCount

		self.t   = data[0]							#juggler name value
		self.dps = self.dotProducts(data)			#list of dot products
		self.sp  = 0 								#track the preference order
		jugglerCount+=1 							#track total jugglers created
		self.joinCircuit() 							#init join circuit
	
	def dotProducts(self, cs):						#return the computed dot product for this juggler
		return [ (c,( cs[1]*circuits[c].h)+(cs[2]*circuits[c].e)+(cs[3]*circuits[c].p) ) for c in cs[4:] ]

	def dpsValForCirKey(self, i):					#return the value for a circuit given a key
		for c in self.dps:							#loop jugglers preferences
			if i == c[0]:							#if passed in circuit number equals preferred circuit in list
				return c[1]							#return the circuit value for this preference

	def dpsValForIndex(self, i):					#return the preference value at index
		return self.dps[i][1]		

	def dpsKeyForIndex(self, i):					#return the preference key at index
		return self.dps[i][0]

	def joinCircuit(self):							#enter juggler into its first preferred cicuit.
		circuits[self.dpsKeyForIndex(self.sp)].hazeInductee(self)

	def prettyPrint(self):							#print out self data for humans to understand
		return "J"+str(self.t)+" C"+str(self.dps[0][0])+":"+str(self.dps[0][1])+" C"+str(self.dps[1][0])+":"+str(self.dps[1][1])+" C"+str(self.dps[1][0])+":"+str(self.dps[1][1])



def readFile():										#read an input file
	return open("data.txt")							#open input file

def writeFile():
	f = open('output.txt', 'w')						#write the output file
	for c in circuits:								#print out the circuits in a pretty fashin
		f.write("C"+str(c.t)+" ")					#write the circuit name once before the matches
		for i in range(len(c.matches)):				#loop the circuits matches
			f.write(c.matches[i].prettyPrint())		#conjoin our useable data back to pretty human bs
			if i < len(c.matches)-1:				#add ,'s to the end of each line, except the last
				f.write(", ")						#write , to end of jugglers dps
		f.write('\n')								#write newline
	f.close()										#close the file
 
def escapedChars(l):
 	l = re.findall(r'\d+', l)  						#replace all but number chars
 	l = [int(i) for i in l] 						#convert all chars to ints
 	return l 										#return the [int]

def openCircuit():
	f = readFile()
	t = True	   									#track the top of file
	for l in f: 									#read line in file
		if t:										#check is this the top?
			if l == '\n': 							#check for top/bottom seperator
				t = False							#flip flag for top to False
				continue							#skip the spac

			l = escapedChars(l)						#escape the bs
			circuit = Circuit(l)					#create a circuit
			circuits.append(circuit)				#add the circuit to a list
		else:
			l = escapedChars(l)						#escape the bs
			juggler = Juggler(l)					#create a juggler that starts joining circuits

def main(): 	
	global jugglerCount, circuitCount, hazeCount

	print "Welcome to the JuggleFest..."

	openCircuit()									#open the main circuit - to begin the competition
	writeFile()										#write the output file

	for c in circuits:								#print out the circuits in a pretty fashin
		print ""									#give the top a little breathing room from the results
		for m in c.matches:
													#conjoin our useable data back to pretty human bs
			print "C"+str(c.t), m.prettyPrint()+",",

	print '\n'										#THE END
	print "Thanks for playing Juggle Fest!\n{0}: Jugglers Attended {1} circuits.\nCombined they got their asses hazed {2} times".format(jugglerCount, circuitCount, hazeCount)
	print '\n'

	value = circuits[1970].cmnt()

	print "The value for circuit 1970s juggler names totalled is, {0}".format(value)
	print "Suggest emailing {0}@yodle.com".format(value)
	
	print "Here are the jugglers for circuit 1970..."
	for match in circuits[1970].matches:

		print match.prettyPrint(),

if __name__ == "__main__":
    main()