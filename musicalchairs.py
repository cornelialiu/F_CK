import sys
import ast

from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python musicalchairs.py <input_file>"
    sys.exit(0)

# Opens the files passed in the command line for reading/writing
_in = open(sys.argv[1], "r")


#########################################################
# Helper variable definitions, Z3 variables + functions #
######################################################### 

##################  Your Code Here  #####################
total = _in.readline()
total = total.rstrip()
step = _in.readline()
step = step.rstrip()
people = _in.readline()
people = people.rstrip()
#above are all str, needs to conver
move = ast.literal_eval(people) #translate string back to list
n = int(total)
s = int(step)
#and we need people that not suppose to move
l = list(range(n))
not_move = set(l) - set(move)
not_move = list(not_move)
not_move.sort()
# and we need define abs() function
def abs(x):
    return If(x >= 0,x,-x)
#########################################################
#        The actual constraints for the problem         #
#########################################################

##################  Your Code Here  #####################

# a matrix of integer variable with size of 2*n
X = [ [ Int(" x % s %s" % (i+1, j+1)) for j in range (2) ] for i in range (n) ]


# each column has to be disctinct as 0,1
col_c= [ Distinct([ X[i][j] for i in range (n) ]) for j in range (2) ]

# the first col(for chair num) has to be sorted as 0,...,n-1
col_sort_c= [ X[i+1][0] - X[i][0] == 1 for i in range (n-1) ] 

# each number of chair and person have to be a number from 0 to n-1
num_c = [And (0 <= X[i][j], X[i][j] <= n-1) for i in range(n) for j in range(2)]

#all input people has to move
move_c = [ X[i][0] - X[i][1] != 0 for i in move ]

#all people not in the list [people] should remain the same
not_move_c = [ X[i][0] - X[i][1] == 0 for i in not_move ]

#all input people has to move and the step has to be <= step
step_c = [Or( abs(X[i][0] - X[i][1]) <= s, (n - abs(X[i][0] - X[i][1])) <= s ) for i in move]

#########################################################
#         Call the solver and print the answer          #
#########################################################

# The final formula going in. Change this to your actual formula
F = col_c + col_sort_c + num_c + not_move_c + move_c + step_c 

# a Z3 solver instance
solver = Solver()
# add all constraints
solver.add(F)
# run Z3
isSAT = solver.check()
# print the result
if isSAT == sat:   
   m = solver.model()
   r = [ [ m. evaluate (X[i][j]) for j in range (2) ]for i in range (n) ]
   ##############  Complete the Output  #################
   print "SAT and the matrix is"
   print_matrix (r)
else:
   print "no solution possible"

