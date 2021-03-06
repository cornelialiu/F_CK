import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python perfectsquare.py <input>"
    sys.exit(0)

x = int(sys.argv[1])

#########################################################
#     Helper variables, functions, and Z3 variables     #
######################################################### 

##################  Your Code Here  #####################

a = Int('a')

#########################################################
#        The actual constraints for the problem         #
#########################################################

##################  Your Code Here  #####################

# The final formula going in. Change this to your actual formula
F = (a > 0, a*a == x)

#########################################################
#         Call the solver and print the answer          #
#########################################################

# a Z3 solver instance
solver = Solver()
# add all constraints
solver.add(F)
# run Z3
isSAT = solver.check()
# print the result
if isSAT == sat:
   m = solver.model()

   ##############  Complete the Output  #################
   print "SAT the square root is", m[a]

else:
   print "UNSAT"

