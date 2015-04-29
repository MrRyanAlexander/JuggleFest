
import re
from itertools import izip

'''
a = ['hello','world','1','2']

b = dict(zip(a[0::2], a[1::2]))

i = iter(a)
b = dict(zip(i, i))

b['hello'] = 'world'
b['1'] = '2'

'''

def main(): 
	f = open("data.txt")
	g = f.readlines()
	g = [ re.sub(r'(C(.*) |C |J |\n)', '', h) for h in g ]

	#split by spaces
	g = [ re.split(" ", h) for h in g ]

	#['C0', 'H:7', 'E:7', 'P:10']	

	for h in g: 

		#h[0] returns a Circuit or Juggler Number; i.e. C0 or J0

		#h[1] returns the H:value
		#h[2] returns the E:value
		#h[3] returns the P:value


		print h[0]

	#i = iter(g[0])
	#j = dict(zip(i, i))

	#print j['C0']

	'''
	['C0 H:7 E:7 P:10', 
	'C1 H:2 E:1 P:1', 
	'C2 H:7 E:6 P:4', 
	'', 
	'J0 H:3 E:9 P:2 C2,C0,C1', 
	'J1 H:4 E:3 P:7 C0,C2,C1', 
	'J2 H:4 E:0 P:10 C0,C2,C1', 
	'J3 H:10 E:3 P:8 C2,C0,C1', 
	'J4 H:6 E:10 P:1 C0,C2,C1', 
	'J5 H:6 E:7 P:7 C0,C2,C1', 
	'J6 H:8 E:6 P:9 C2,C1,C0', 
	'J7 H:7 E:1 P:5 C2,C1,C0', 
	'J8 H:8 E:2 P:3 C1,C0,C2', 
	'J9 H:10 E:2 P:1 C1,C2,C0', 
	'J10 H:6 E:4 P:5 C0,C2,C1', 
	'J11 H:8 E:4 P:7 C0,C1,C2']


	c = {
	'CO': {'H':7, 'E':7, 'P':10}, 
	'C1': {'H':2, 'E':1, 'P':1}, 
	'C2': {'H':7, 'E':6, 'P':4} 
	}

	c['C4'] = {'H':17, 'E':16, 'P':14}
   	'''
   	#print c['C4']['P']


if __name__ == "__main__":
    main()

