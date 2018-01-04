#########################################################################################
#
#   File:       nearestneighbor.py
#   Author:     David Weber (dwebe003)
#   Date:       05/29/2017
#   Version:    1.0
#
#########################################################################################
import sys
import math

#################################################

#Computes the distance between p and q using the Pythagorean metric
def dist(p,q): 
	
	X = math.pow(p[0]-q[0], 2)
	Y = math.pow(p[1]-q[1], 2)
	
	return math.sqrt(X + Y)

#################################################

#Compares 2 points and changes the current minPair if the distance d(p,q) is less
def comparePoints(p, q, minPair):
	
	delta = dist(p,q)
	
	if(delta < minPair[1]):
		minPair[0] = q,p
		minPair[1] = delta

##################################################

# merge two sorted lists by y-coordinate
def merge(left, right):
	
	i = 0
	j = 0
	
	while i < len(left) or j < len(right):
		
		if j >= len(right) or (i < len(left) and left[i][1] <= right[j][1]):
			yield left[i]
			i = i + 1
		else:
			yield right[j]
			j = j + 1
		#endif
		
	#endwhile

##################################################


# Find nearest neighbor recursively
def utility(points):
	
	if len(points) < 2:
		return points
	#endif
		
		
	median = len(points)/2
	
	midx = points[median][0]
	
	
	#recursion
	points = list(merge(utility(points[:median]), utility(points[median:])))

	#checks the median line
	dyn = [ p for p in points if abs(p[0] - midx) < minPair[1] ]
	
	for i in range(len(dyn)):
		
		for j in range(1,8):
			
			if i+j < len(dyn):
				comparePoints(dyn[i], dyn[i+j], minPair)
			#endif
			
		#endfor
		
	#endfor
	
	return points

###################################################

#Main function for finding the nearest neighbors
def nearestNeighbor(points, minPair):
	
	#this utilizes the built-in sort function
	points.sort()
	
	#this calls to the recursive function
	utility(points)
	
	return minPair

###################################################

# Obtains points from outside file
def getInput(points, filename):
	#import fileinput
	
	#with open("input.txt", "r") as f:
	fileinput = open(filename, "r")
	
	for line in fileinput:
		a,b = line.split()
		points.append( (float(a), float(b)) )
	#endfor
			
	print points
	#f.close()
	
###################################################

# BRUTE FORCE ALGO
def bruteForce(points, minPair):
	
	minDist = float("inf")
	
	for i in range(len(points) - 1):
		
		for j in range(i+1, len(points)):
			
			d = dist(points[i], points[j])
			if(d < minDist):
				minDist = d;
				minPair[0] = points[i],points[j]
				minPair[1] = d
			#endif
			
		#endfor
		
	#endfor
	return minDist
	
###################################################

# My own frankenstein "main"

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    

# sets up empty list of points
points = []

# Gets input from input.txt
getInput(points, sys.argv[2])

#minPair holds the data of the 2 nearest points along with the distance that 
#separates them. It is initially set to the first 2 points until acted upon.
minPair = [(points[0], points[1]), dist(points[0], points[1])]

if sys.argv[1] == '-dc':
	nearestNeighbor(points, minPair)
	print "Divide and Conquer: ", minPair[1]
	print "Points: ", minPair[0]
	
	#outputs the distance to input_distance.txt
	fileOutput = open("input_distance.txt", "rb+")
	fileOutput.write(str(minPair[1]))
	fileOutput.close()

if sys.argv[1] == '-bf':
	
	bfDist = bruteForce(points, minPair)

	print "Brute Force: ", bfDist
	print "Points: ", minPair[0]
	
	fileOutput = open("input_distance.txt", "rb+")
	fileOutput.write(str(bfDist))
	fileOutput.close()
	
if sys.argv[1] == '-both':
	nearestNeighbor(points, minPair)
	print "Divide and Conquer: ", minPair[1]
	
	bfDist = bruteForce(points, minPair)
	print "Brute Force: ", bfDist
	print "Points: ", minPair[0]
	
	#outputs the distance to input_distance.txt
	fileOutput = open("input_distance.txt", "rb+")
	fileOutput.write(str(minPair[1]))
	fileOutput.close()
