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
#import the regex package
import re 											

#list to hold all the circuits
circuits = []		

#track total circuits created			
circuitCount = 0 								

#track total jugglers created
jugglerCount = 0 		

#track overal hazing total
hazeCount = 0 								

#Class Object for circuits
class Circuit:										

	def __init__(self, data):
		global circuitCount

		#circuit name value
		self.t = data[0]	

		#hand eye
		self.h = data[1]  							
		
		#endurance
		self.e = data[2]							
		
		#pizzaz
		self.p = data[3]							
		
		#the 4-6 matches for this circuit
		self.matches = []							
		
		#track if circuit has match
		self.hasMatch = False						
		
		#track total circuits created
		circuitCount+=1 							

	#haze an inductee; a juggler
	def hazeInductee(self, j):						
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
			
			#add the first juggler to this circuit
			self.matches.append(j)				

			#flip the swith for has matches only run 
			#this once per circuit match
			self.hasMatch = True					

	#insert match at index
	def insertMatch(self, j, i):

		#if there is no index
		if i == None:

			#append the new juggler to the list
			self.matches.append(j)					
		else:	

			#insert the higher match, bumping the rest down 1
			self.matches.insert(i, j)				

		#send extra jugglers to their next preference
		if len(self.matches) > 6:			

			#copy the juggler		
			tj = self.matches[-1]			

			#remove the juggler for this circuit		
			self.matches.remove(self.matches[-1])	

			#send the juggler to its next circuit
			self.passJuggler(tj)					

	#pass juggler to its next preference
	def passJuggler(self, j):	

		#make sure not to pass jugglers out of bounds					
		if not j.sp >= len(j.dps)-1:	

			#increment the jugglers current preferred circuit	
			#for the next loop after it's passed		
			j.sp +=1 								
													
			#pass the juggler to next circuit
			circuits[j.dpsKeyForIndex(j.sp)].hazeInductee(j)

	#test juggler against list for match
	def isMatch(self, j):

		#keep track if no match is found
		notFound=True								

		#compare to all index
		for i in range(len(self.matches)):			
			
			#print "Val for J {0} compared to C {1}".format(j.dpsValForIndex(j.sp), self.matches[i].dpsValForCirKey(self.t))
			
			if j.dpsValForIndex(j.sp) > self.matches[i].dpsValForCirKey(self.t):# or j.dpsValForIndex(j.sp) < self.matches[-1].dpsValForCirKey(self.t):
				
				#print "Picked Juggler {0} with value {1} compared to {2}".format(j.t, j.dpsValForIndex(j.sp), self.matches[i].dpsValForCirKey(self.t))
			
				#flip the switch if found
				notFound=False			

				#start inserting the match at index
				self.insertMatch(j, i)				

				#break out of loop
				break

		#if no match was found looping
		if notFound:							

			#the match will just be appended	
			self.insertMatch(j, None)				

	#add up the matched juggler names
	#this is just used at the end to
	#print out something pretty
	def cmnt(self):									
		t = 0 										 
		for j in self.matches:				

			#adds to the total name count		
			t += j.t 						

		#return the total		
		return t 		

#Class Object for jugglers
class Juggler:							

	def __init__(self, data):
		global jugglerCount

		#juggler name value
		self.t   = data[0]					

		#list of dot products		
		self.dps = self.dotProducts(data)		

		#track the preference order	
		self.sp  = 0 						

		#track total jugglers created		
		jugglerCount+=1 					

		#init join circuit		
		self.joinCircuit() 							
	
	#return the computed dot product for this juggler
	def dotProducts(self, cs):						
		return [ (c,( cs[1]*circuits[c].h)+(cs[2]*circuits[c].e)+(cs[3]*circuits[c].p) ) for c in cs[4:] ]

	#return the value for a circuit given a key
	def dpsValForCirKey(self, i):				

		#loop jugglers preferences	
		for c in self.dps:	

			#if passed in circuit number equals preferred circuit in list						
			if i == c[0]:							

				#return the circuit value for this preference
				return c[1]							

	#return the preference value at index
	def dpsValForIndex(self, i):					
		return self.dps[i][1]		

	#return the preference key at index
	def dpsKeyForIndex(self, i):					
		return self.dps[i][0]

	#enter juggler into its first preferred cicuit.
	def joinCircuit(self):							
		circuits[self.dpsKeyForIndex(self.sp)].hazeInductee(self)

	#print out self data for humans to understand
	def prettyPrint(self):							
		return "J"+str(self.t)+" C"+str(self.dps[0][0])+":"+str(self.dps[0][1])+" C"+str(self.dps[1][0])+":"+str(self.dps[1][1])+" C"+str(self.dps[1][0])+":"+str(self.dps[1][1])

#read an input file
def readFile():		

	#open input file			
	return open("data.txt")							

#write the output file
def writeFile():
	f = open('output.txt', 'w')						
	for c in circuits:		

		#write newline						
		f.write("C"+str(c.t)+" ")					
		for i in range(len(c.matches)):				
			f.write(c.matches[i].prettyPrint())		
			if i < len(c.matches)-1:				
				f.write(", ")						
		f.write('\n')	

	#close the file				
	f.close()										
 
#escape chars for line input
def escapedChars(l):

	#replace all but number chars
 	l = re.findall(r'\d+', l)  				

 	#convert all chars to ints		
 	l = [int(i) for i in l] 				

 	#return the [ints]		
 	return l 										

def openCircuit():
	f = readFile()

	#track the top of file
	t = True	   									
	for l in f: 									
		if t:						
			#check for top/bottom seperator				
			if l == '\n': 							
				t = False				

				#skip the space			
				continue							

			#escape the chars
			l = escapedChars(l)			

			#create a circuit			
			circuit = Circuit(l)		

			#add the circuit to a list			
			circuits.append(circuit)				
		else:

			#escape the chars
			l = escapedChars(l)						

			#create a juggler that starts joining circuits
			juggler = Juggler(l)					

def main(): 	
	global jugglerCount, circuitCount, hazeCount

	print "Welcome to the JuggleFest..."

	#open the main circuit - to begin the competition
	openCircuit()									

	#write the output file
	writeFile()										

	#print out the circuits in a pretty fashin
	for c in circuits:				

		#give the top a little breathing room from the results				
		print ""									
		for m in c.matches:
													
			#conjoin our useable data back to pretty human bs
			print "C"+str(c.t), m.prettyPrint()+",",

	#THE END
	print '\n'										
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