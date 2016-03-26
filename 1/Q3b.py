import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 3:
    print "Usage: python magicsquare.py <dimension> <sum>"
    sys.exit(0)


########################################################
#     Helper variables, functions, and Z3 variables     #
######################################################### 

##################  Your Code Here  #####################
dim = int(sys.argv[1])
s = int(sys.argv[2])

#########################################################
#        The actual constraints for the problem         #
#########################################################

##################  Your Code Here  #####################

# a matrix of integer variable with size of dim*dim
X = [ [ Int(" x_%s_%s" % (i+1, j+1)) for j in range (dim) ] for i in range (dim) ]

#each cell contains a value in range 1 to dim^2
cells_c = [ And (1 <= X[i][j], X[i][j] < s) 
for i in range (dim) for j in range (dim) ]

#each row has the sum of s
rows_c = [sum(X[i]) == s for i in range (dim)]

#each column has the sum of s
cols_c= [ sum ([ X[i][j] for i in range (dim) ]) == s for j in range (dim)]

#2 diagonal has the sum of s
left_diag_c = [sum( [ X[i][i] for i in range (dim)]) == s]
right_diag_c = [sum( [ X[i][dim-i-1] for i in range (dim)]) == s]
diag_c = left_diag_c + right_diag_c
#########################################################
#         Call the solver and print the answer          #
#########################################################

# The final formula going in. Change this to your actual formula
magic_square_c = cells_c + rows_c + diag_c
F = magic_square_c

# a Z3 solver instance
solver = Solver()
# add all constraints
solver.add(F)
# run Z3
isSAT = solver.check()
# print the result
if isSAT == sat:
   m = solver.model()
   r = [ [ m. evaluate (X[i][j]) for j in range (dim) ]for i in range (dim) ]
   ##############  Complete the Output  #################
   print "SAT and the matrix is"
   print_matrix (r)
else:
   print "UNSAT"

