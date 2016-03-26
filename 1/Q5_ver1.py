import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python strategy.py <input_file>"
    sys.exit(0)

# Opens the files passed in the command line for reading/writing
_in = open(sys.argv[1], "r")

# game matrix
r = []
for i in range(3):
    r = r + [eval(_in.readline())]
#########################################################
# Helper variable definitions, Z3 variables + functions #
######################################################### 

##################  Your Code Here  #####################
def find_win_A(s):
	return If(s[0] <= s[1], 1, 0)
def find_win_B(s):
	return If(s[1] <= s[0], 1, 0)

levelList = ["high", "medium", "low"]

#a matrix helps check for "better deal"
# looks lile
#[[high, 1,1,1],[medium,1,1,1],[low,1,1,1]]
X_A = [ [ Int(" x_%s_%s " % (i+1, j+1)) for j in range (3) ] for i in range (3) ]
X_B = [ [ Int(" x_%s_%s " % (i+1, j+1)) for j in range (3) ] for i in range (3) ]


#########################################################
#        The actual constraints for the problem         #
#########################################################

##################  Your Code Here  #####################

# for player A
# "check" matrix set 1 or 0 according to  game matrix. 1 for win
A_num_c = [X_A[i][j] == find_win_A(r[i][j]) for i in range (3) for j in range (3)]
# there must exist a row where num of wins >= 2
A_dom_c = [Or(sum(X_A[0][:3]) >= 2, sum(X_A[1][:3]) >= 2, sum(X_A[2][:3]) >= 2)]
# the last number will be sum of 0,1,2, to make easier for output
# A_sum_c = [X_A[i][3] == sum(X_A[i][0:3]) for i in range (3)]

#for player B
# "check" matrix set 1 or 0 according to  game matrix. 1 for win
#here r has to be read transposed because indexing only do M[0][:] not M[:][0]
B_num_c = [X_B[i][j] == find_win_B(r[j][i]) for i in range (3) for j in range (3)]
# there must exist a row where num of wins >= 2
B_dom_c = [Or(sum(X_B[0][:3]) >= 2, sum(X_B[1][:3]) >= 2, sum(X_B[2][:3]) >= 2)]
# the last number will be sum of 0,1,2, to make easier for output
# B_sum_c = [X_B[i][3] == sum(X_B[i][:3]) for i in range (3)]

#########################################################
#         Call the solver and print the answer          #
#########################################################

# The final formula going in. Change this to your actual formula
F_A = A_num_c + A_dom_c #+ A_sum_c
F_B = B_num_c + B_dom_c #+ B_sum_c

#Solver for A
# a Z3 solver instance
solver = Solver()
# add all constraints
solver.add(F_A)
# run Z3
isSAT = solver.check()
# print the result
resultA = "Player A: "
if isSAT == sat:
  resultA += "The domainant strategy is "
  # evaluate the final array from the model, and re-map the guest id's to the result
  m = solver.model()
  r = [ [ m.evaluate(X_A[i][j]) for j in range (3) ]for i in range (3) ]
  print "NEED to fix output"
  print "so we have solver matrix"
  print_matrix(r)
  print "where each cell is the same order as input"
  print "1 is for a win or tie for player A"
  ######################################################################################### NEED FIX
  # sum of r[i][:] is not returning a int but a formula
  # I guess it was because r[i][0] is not a list but a z3 object
  # need to read z3 functions to find a way either:
  # transform that to list
  # sum that element
  for i in range(3):
    buf = sum(r[i][:])
    print "but the matrix is a z3 instance and I can't sum it."
    print "if you print the sum of that row"
    print buf
    print "need to find a way extract number out and sum it up"
    if buf >= 2:
      resultA += levelList[i]
      break
   	##############  Complete the Output  #################
  print resultA
else:
  resultA += "no domainant strategy"
  print resultA
########################################## The player winning matrix for A#################
#matrix A = 
#[[1, 1, 1], #high
# [1, 1, 0], #medium
# [0, 0, 0] #low

###########################################################################################

#Solver for B
# a Z3 solver instance
solver = Solver()
# add all constraints
solver.add(F_B)
# run Z3
isSAT = solver.check()
# print the result
resultB = "Player B: "

if isSAT == sat:
  resultB += "The domainant strategy is "
  # evaluate the final array from the model, and re-map the guest id's to the result
  m = solver.model()
  r = [ [ m.evaluate(X_A[i][j]) for j in range (3) ]for i in range (3) ]
  ########################################################################################### Need Fix
  #same problem as A
  for j in range(3):
    buf = sum(r[j][0:])
    print buf
    if buf >= 2:
      resultB += levelList[j]
      break
      ##############  Complete the Output  ################
  print resultB
else:
  resultB += "no domainant strategy"
  print resultB

################################################The player winning matrix for B###########################
# matrix B
# [[0, 0, 1], #high
#  [0, 1, 1], #medium
#  [0, 1, 1]] #low

#####################################################################################################

