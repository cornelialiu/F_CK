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

def is_dom(row):
  row_c = sum(row) >= 2
  solver = Solver()
  solver.add(row_c)
  if solver.check() == sat: 
    return sat
  else:
    return unsat

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

#for player B
# "check" matrix set 1 or 0 according to  game matrix. 1 for win
#here r has to be read transposed because indexing only do M[0][:] not M[:][0]
B_num_c = [X_B[i][j] == find_win_B(r[j][i]) for i in range (3) for j in range (3)]
# there must exist a row where num of wins >= 2
B_dom_c = [Or(sum(X_B[0][:3]) >= 2, sum(X_B[1][:3]) >= 2, sum(X_B[2][:3]) >= 2)]


#########################################################
#         Call the solver and print the answer          #
#########################################################

# The final formula going in. Change this to your actual formula
F_A = A_num_c + A_dom_c 
F_B = B_num_c + B_dom_c 

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
  # print "A matrix is"
  # print_matrix(r)
  for i in range(3):
    
    if is_dom(r[i]) == sat:
      resultA += levelList[i]
      break
    ##############  Complete the Output  #################
  print resultA
else:
  resultA += "no domainant strategy"
  print resultA

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
  # print " B matrix is"
  # print_matrix(r)
  for i in range(3):
    if is_dom(r[i]) == sat:
      resultB += levelList[i]
      break
    ##############  Complete the Output  #################
  print resultB
else:
  resultB += "no domainant strategy"
  print resultB