#Juggle Fest

This is my solution to the Juggle Fest problem; found @ http://www.yodlecareers.com/puzzles/jugglefest.html

Taking this challeng taught me about how not to sort big lists and that simple problems
hide behind complexity. 

I went from writing a non-solution that would have had upwards of 5 million iterations to 
this simple solution here which has just over 20K and these iterations are part of the
read in of a file line by line, not individual loops. 

The difference between iterating a list for matches and simply working off of an insert 
at index if (k,v) > (k,v) else append has me quite amazed at the change this presented. 

In any case, this is my final solution. After 3 trying days and many long hours working through this manually, I persited to this point. I am satisfied with the result. 

Clone this repo

''' bash

git clone https://github.com/MrRyanAlexander/JuggleFest.git

'''

You will need to have [Python]("https://www.python.org/downloads/") installed on your machine to run this. 

''' bash

python juggle.py

'''

