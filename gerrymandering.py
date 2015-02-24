"""

Assignment 3: Gerrymandering
Students: Kara James and Joshua Weaver



This file reads in the information from the SmallNeighboorhood or LargeNeighborhood
file into a matrix composed of nodes. Each node object stores the (x,y) coordinates
and majority party for that section. All nodes are also placed into the
unallocated list; this list keeps track of which nodes have not been assigned to a
district yet.

Minimax calls the choices function, which generates all possible districts (limited
to rows, columns, squares, or chubby rows/columns) given the nodes remaining in the
unallocated list. It stores all these possible districts as tuples in the potentials
list.

Minimax then, for each option in the potentials list, continues to figure out the 
ideal moves. It uses the heuristic, which evaluates the districts to assign a score.
When minimax returns a district, the nodes in that district are removed from the
unallocated list, and that district is stored in the districts list.

For the large neighborhood, we limited the depth of minimax to four.

More details are found in the comments throughout the code in this file.

"""
import sys
import node
import ast

#general stuff
filename = sys.argv[-1]
n = 0
numR = 0
numD = 0
unallocated = list()
potentials = list()
depth = 4
district = list()


# Set the value of n
if "smallNeighborhood.txt" in filename:
    n = 4
    # Create variables to store winners of districts
    districts = [0, 0, 0, 0, 0]
elif "largeNeighborhood.txt" in filename:
    n = 8
    # Create variables to store winners of districts
    districts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    print "Warning: this will take about 20min to run depending on your hardware."
else:
    print "given file is not smallNeighborhhod.txt or largeNeighborhood.txt"


# Making the empty matrix
state = [[0 for x in xrange(n)] for x in xrange(n)]

# Minimax variables
maxvalue = -100000, state
minvalue = 100000, state


# Reading in the information from the file
with open(filename) as f:
    for i in range(n):
        for j in range(n):
            d = f.read(1)
            state[i][j] = node.make_node(d, 0) #fix to grab party
            space = f.read(1)


# Printing the matrix
print "matrix is: "
for i in range(n):
    for j in range(n):
        sys.stdout.write(state[i][j].party)
        sys.stdout.write(" ")
    print " "

# Populating list of unallocated nodes
for i in range(n):
    for j in range(n):
        if state[i][j].district is 0:
            unallocated.append(state[i][j])



def choices(state):
    # Clear the old potentials out
    del potentials[:]
    # For the small neighborhood
    if n == 4:
        # Make a list of all contiguous districts of rows, columns and squares
        # rows & columns
        for i in range(n):
            if state[i][0] in unallocated and state[i][1] in unallocated and state[i][2] in unallocated and state[i][3] in unallocated:
                potentials.append(((i,0), (i,1), (i,2), (i,3)))
            if state[0][i] in unallocated and state[1][i] in unallocated and state[2][i] in unallocated and state[3][i] in unallocated:
                potentials.append(((0,i), (1,i), (2,i), (3,i)))
        # squares
        if state[0][0] in unallocated and state[0][1] in unallocated and state[1][0] in unallocated and state[1][1] in unallocated:
            potentials.append(((0,0), (0,1), (1,0), (1,1)))
        if state[3][3] in unallocated and state[2][3] in unallocated and state[3][2] in unallocated and state[2][2] in unallocated:
            potentials.append(((3,3), (2,3), (3,2), (2,2)))
        if state[3][0] in unallocated and state[3][1] in unallocated and state[2][0] in unallocated and state[2][1] in unallocated:
            potentials.append(((3,0), (3,1), (2,0), (2,1)))
        if state[0][3] in unallocated and state[1][3] in unallocated and state[0][2] in unallocated and state[1][2] in unallocated:
            potentials.append(((0,3), (1,3), (0,2), (1,2)))
    # For the large neighborhood
    elif n == 8:
        #rows and columns
        for i in range(n):
            if state[i][0] in unallocated and state[i][1] in unallocated and state[i][2] in unallocated and state[i][3] in unallocated and state[i][4] in unallocated and state[i][5] in unallocated and state[i][6] in unallocated and state[i][7] in unallocated:
                potentials.append(((i,0), (i,1), (i,2), (i,3), (i,4), (i,5), (i,6), (i,7)))
            if state[0][i] in unallocated and state[1][i] in unallocated and state[2][i] in unallocated and state[3][i] in unallocated and state[4][i] in unallocated and state[5][i] in unallocated and state[6][i] in unallocated and state[7][i] in unallocated:
                potentials.append(((0,i), (1,i), (2,i), (3,i), (4,i), (5,i), (6,i), (7,i)))
        # chubby rows
        for i in range((n-3)):
            for j in range((n-1)):
                if state[i][j] in unallocated and state[i+1][j] in unallocated and state[i+2][j] in unallocated and state[i+3][j] in unallocated and state[i][j+1] in unallocated and state[i+1][j+1] in unallocated and state[i+2][j+1] in unallocated and state[i+3][j+1] in unallocated:
                    potentials.append(((i,j), (i+1,j), (i+2,j), (i+3,j), (i,j+1), (i+1,j+1), (i+2, j+1), (i+3,j+1)))
        # chubby columns
        for i in range((n-1)):
            for j in range((n-3)):
                if state[i][j] in unallocated and state[i][j+1] in unallocated and state[i][j+2] in unallocated and state[i][j+3] in unallocated and state[i+1][j] in unallocated and state[i+1][j+1] in unallocated and state[i+1][j+2] in unallocated and state[i+1][j+3] in unallocated:
                    potentials.append(((i,j), (i,j+1), (i,j+2), (i,j+3), (i+1,j), (i+1,j+1), (i+1, j+2), (i+1,j+3)))
    else:
        print "Choices error: n not 4 or 8"

# Populate potentials before calling minimax
choices(state)

def minimax(district, depth, maxplayer):
    global minvalue, maxvalue
    # if depth is leaf or potentials is empty
    if depth is 0 or not potentials:
        return heuristic(district), state
    if maxplayer:
        choices(state)
        for choice in potentials:
            val, temp = minimax(choice, depth-1, False)
            if maxvalue[0] < val:
                maxvalue = val, choice
        return maxvalue
    else:
        choices(state)
        for choice in potentials:
            val, temp = minimax(choice, depth-1, True)
            if minvalue[0] > val:
                minvalue = val, choice
        return minvalue

def heuristic(district):
    # Counting variables
    total = 0
    winner = 0
    # Get value for previously chosen districts:
    for i in range(n):
        if districts[i+1] is 1:
            total = total + 1
        elif districts[i+1] is -1:
            total = total - 1
        elif districts[i+1] is 0:
            total = total
        else:
            print "error 1"
    # Get value for current district
    for thing in district:
        x, y = thing
        if "R" in state[x][y].party:
            winner = winner + 1
        elif "D" in state[x][y].party:
            winner = winner - 1
        else:
            print "error 2"
    # Combine results
    if winner > 0:
        total = total + 1
    elif winner < 0:
        total = total - 1
    # Return value for this state
    return total







#variables for while loop
t = 1
#throwaway for first minimax call
districtness = ((0,0), (0,0))

#MINIMAXING TO THE MAX (OR MIN)
while unallocated:
    # For assigning winner of district
    winner = 0
    # Call minimax
    val, district = minimax(districtness, depth, True)
    # Do stuff with found district
    print "dist:", district
    for thing in district:
        x, y = thing
        # Assign each node in district a number
        state[x][y].district = t
        # Remove each node from unallocated
        unallocated.remove(state[x][y])
        # Check winner of that section
        if "R" in state[x][y].party:
            winner += 1
        elif "D" in state[x][y].party:
            winner -= 1
    # Assign winner to that district
    if winner > 0:           # Max won overall
        print "max won ",t
        districts[t] = 1
    elif winner < 0:         # Min won overall
        print "min won ",t
        districts[t] = -1
    else:                    # Tie
        print "tie ",t
        districts[t] = 0
    # Reset maxvalue, minvalue and increment t
    maxvalue = -100000, state
    minvalue = 100000, state
    t += 1
    

# Grading requirements
print "*************************************"
print "MAX = R"
print "MIN = D"
print "*************************************"

#After  the  algorithm  runs  and  districts  are  assigned,  output  the  
#cells  assigned  to  each district.
print "*************************************"
for i in range(n):
    print "District",i+1,": " #  (1,1),  (1,2),  (1,3)
    for j in range(n):
        for k in range(n):
            if state[j][k].district is (i+1):
                sys.stdout.write("(")
                sys.stdout.write(str(j))
                sys.stdout.write(",")
                sys.stdout.write(str(k))
                sys.stdout.write(")")
    print ""
            
print "*************************************"

#Also,  output  the  districts  awarded  to  each  player
print "*************************************"
for i in range(n):
    if districts[i+1] is 1:
        print "District",i+1,": R"
        numR += 1
    elif districts[i+1] is -1:
        print "District",i+1,": D"
        numD += 1
    elif districts[i+1] is 0:
        print "District",i+1,": TIE"
    else:
        print "District winner error"

print "*************************************"

#Finally,  output  who  won  the  most  districts,  and  therefore,
#won  the  election.
print "*************************************"
if numR > numD: 
    print "Election  outcome: R wins!"
elif numR < numD: 
    print "Election  outcome: D wins!"
else:
    print "The Election is a tie."
print "*************************************"

    
    
