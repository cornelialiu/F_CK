import sys

# This code is meant to read in a list of moves for a rubik's cube and generate code that solves the cube. 

# To minimize the number of moves, only a surface panel can be turned, and only right.
# So no rotation of central panels, and no left turns. Both achievable from right
# turns of surface panels. Hence the input is simple a list of integers in 0..5
# where an integer represents the panel being turned. 

#Each panel of the cube is numbered 0..5 with 4 being the top and 5 the bottom.
#Here is a graphical representation
#
#       4 4 4
#       4 4 4
#       4 4 4 
# 0 0 0 1 1 1 2 2 2 3 3 3
# 0 0 0 1 1 1 2 2 2 3 3 3
# 0 0 0 1 1 1 2 2 2 3 3 3
#       5 5 5
#       5 5 5 
#       5 5 5 
###########################Helper function to print cube in this view##########
def print_cube(face):
  '''
  face : panel index 
  print cube in the graphical representation of :
        top
  left  face    right   opposite
        bottom

  '''
  oppo = find_oppo(face)
  top = surface[face]['top']
  bottom = surface[face]['bottom']
  right = surface[face]['right']
  left = surface[face]['left']
  #organize output
  output = '\n'
  output = output + '         '+ str(cube[top][0]).strip('[]') +'              ' +'\n'
  output = output + '         '+ str(cube[top][1]).strip('[]') +'              ' +'\n'
  output = output + '         '+ str(cube[top][2]).strip('[]') +'              ' +'\n'

  output = output + str(cube[left][0]).strip('[]') + '  ' + str(cube[face][0]).strip('[]') + '  ' + str(cube[right][0]).strip('[]') + '  ' + str(cube[oppo][0]).strip('[]') + '\n'
  output = output + str(cube[left][1]).strip('[]') + '  ' + str(cube[face][1]).strip('[]') + '  ' + str(cube[right][1]).strip('[]') + '  ' + str(cube[oppo][1]).strip('[]') + '\n'
  output = output + str(cube[left][2]).strip('[]') + '  ' + str(cube[face][2]).strip('[]') + '  ' + str(cube[right][2]).strip('[]') + '  ' + str(cube[oppo][2]).strip('[]') + '\n'

  output = output + '         '+ str(cube[bottom][0]).strip('[]') +'              ' +'\n'
  output = output + '         '+ str(cube[bottom][1]).strip('[]') +'              ' +'\n'
  output = output + '         '+ str(cube[bottom][2]).strip('[]') +'              ' +'\n'


  output = output.replace(',', ' ')
  print output



def find_oppo(face):
  cubelist=[0,1,2,3,4,5]
  keys = ['top','bottom','right','left']
  for key in keys:
    cubelist.remove(surface[face][key])
  cubelist.remove(face)
  return cubelist[0]
  ################################################################################

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python rubik.py <input_file>"
    sys.exit(0)

# Opens the file passed in the command line for reading
_in = open(sys.argv[1], "r")

# read the list
moves = eval(_in.readline())

n = 3
#the rubik's cube in its initial solved state. 
cube = [[[ k for i in range(n)] for j in range(n)] for k in range(6)]

#The relationship of the panels to each-other is encoded in this dictionary
surface = {0:{"top":4,"bottom":5,"left":3,"right":1},
           1:{"top":4,"bottom":5,"left":0,"right":2},
           2:{"top":4,"bottom":5,"left":1,"right":3},
           3:{"top":4,"bottom":5,"left":2,"right":0},

           4:{"top":3,"bottom":1,"left":0,"right":2},
           5:{"top":1,"bottom":3,"left":0,"right":2},
}


# rotate a face (0..5) of the rubik's cube
def rotate(face):
   '''  
   turn right just once for face as surface panel 
   change matrix according to relationship
    ========= panel relationship tale =========
        top      right    bottom    left    
    0   [i][0]   [i][0]   [i][0]   [i][2]   
    1   [2]      [i][0]   [0]      [i][2]   
    2   [i][2]   [i][0]   [i][2]   [i][2]   
    3   [0]      [i][0]   [2]      [i][2]   
    4   [0]      [0]      [0]      [0]      
    5   [2]      [2]      [2]      [2]      
    ===========================================
    in the order of this shift:
    top >> right >> bottom >> left >> top
   '''
   buf = []
   if face == 0:
    buf = place_col(surface[0]['top'], 0)
    buf = place_col(surface[0]['right'], 0, buf)
    buf = place_col(surface[0]['bottom'], 0, buf)
    buf = place_col(surface[0]['left'], 2, buf)
    buf = place_col(surface[0]['top'], 0, buf)
   elif face == 1:
    buf = place_row(surface[1]['top'], 2)
    buf = place_col(surface[1]['right'], 0, buf)
    buf = place_row(surface[1]['bottom'], 0, buf)
    buf = place_col(surface[1]['left'], 2, buf)
    buf = place_row(surface[1]['top'], 2, buf)
   elif face == 2:
    buf = place_col(surface[2]['top'], 2)
    buf = place_col(surface[2]['right'], 0, buf)
    buf = place_col(surface[2]['bottom'], 2, buf)
    buf = place_col(surface[2]['left'], 2, buf)
    buf = place_col(surface[2]['top'], 2, buf)
   elif face == 3:
    buf = place_row(surface[3]['top'], 0)
    buf = place_col(surface[3]['right'], 0, buf)
    buf = place_row(surface[3]['bottom'], 2, buf)
    buf = place_col(surface[3]['left'], 2, buf)
    buf = place_row(surface[3]['top'], 0, buf)
   elif face == 4:
    buf = place_row(surface[4]['top'], 0)
    buf = place_row(surface[4]['right'], 0, buf)
    buf = place_row(surface[4]['bottom'], 0, buf)
    buf = place_row(surface[4]['left'], 0, buf)
    buf = place_row(surface[4]['top'], 0, buf)
   elif face == 5: 
    buf = place_row(surface[5]['top'], 2)
    buf = place_row(surface[5]['right'], 2, buf)
    buf = place_row(surface[5]['bottom'], 2, buf)
    buf = place_row(surface[5]['left'], 2, buf)
    buf = place_row(surface[5]['top'], 2, buf)

########helper function for rotate#################

def place_col(panel, col_index, left=None):
  '''
  get a col from a panel in cube,
  if a replace is included, 
  place a col into panel matrix
  return the list of num that was replaced
  '''
  buf = []
  i = 0
  for row in cube[panel]:
    buf.append(row[col_index])
    if left != None:
      row[col_index] = left[i]
      i += 1
  return buf

def place_row(panel, row_index, left=None):
  '''
  get a row from a panel in cube
  if a num is included,
    place that row with num
  '''
  buf = []
  buf = cube[panel][row_index]
  if left != None:
    cube[panel][row_index] = left
  return buf


###################################################

#play a series of moves
def play(move_list):
   if move_list != []:
      rotate(move_list[0])
      play(move_list[1:])

# play the input moves
play(moves)

# ------- create the code ----------- #

linebreak = lambda a,b: a+"\n"+b
instance = cube

# module declaration and variable declaration
main = """MODULE main
VAR
    tiles : array 0..{0} of array 0..{0} of array 0..5;
ASSIGN""".format(n-1)

# the initialization of variables to the instance
init = reduce(linebreak, ["    init(tiles[{0}][{1}][{2}]) := {3};".format(x,y,z, cube[x][y][z]) for x in range(6) for y in range(n) for z in range(n)])
    
    #i means i-th index
    # ========= panel relationship tale =========
    #           index of the row to the right
    # panel    top      right    bottom    left    
    # 0        4[i][0]  5[i][0]  3[i][0]   1[i][2]   
    # 1        4[2][i]  5[i][0]  0[0]      2[i][2]   
    # 2        4[i][2]  5[i][0]  1[i][2]   3[i][2]   
    # 3        4[0]     5[i][0]  2[2]      0[i][2]   
    # 4        3[0]     1[0]     0[0]      2[0]      
    # 5        1[2]     3[2]     0[2]      2[2]      
    # ===========================================
    #     in the order of this shift:
    # top >> right >> bottom >> left >> top

    # I'm not sure if SMV need a buffer. Most likely not.
def edit_tail(condition, tail, changeTo):
  '''
  helper function to change tail character in parsed condition 
  eg. 
  "    next(tiles[1][1][2]) := tiles[4][1][0] &" 
  =>"    next(tiles[1][1][2]) := tiles[4][1][0] ,"

  '''
  condition = condition[:-1]
  condition += changeTo
  return condition

# if rotate panel 0
panel_0_top = reduce(linebreak, ["    next(tiles[4][{0}][0]) := tiles[5][{0}][0] &".format(a) for a in range(n)])
panel_0_right =reduce(linebreak, ["    next(tiles[5][{0}][0]) := tiles[3][{0}][0] &".format(i) for i in range(n)])
panel_0_bottom = reduce(linebreak, ["    next(tiles[3][{0}][0]) := tiles[1][{0}][2] &".format(i) for i in range(n)])
#last one can't be done by reduce a for loop because it's not same format. ; at the last one not &
panel_0_left = reduce(linebreak, ["    next(tiles[1][{0}][2]) := tiles[4][{0}][0] &".format(i) for i in range(n)])
panel_0_left = edit_tail(panel_0_left, "&","|")
panel_0 = reduce(linebreak, [panel_0_top, panel_0_right, panel_0_bottom, panel_0_left])


# if rotate panel 1
panel_1_top = reduce(linebreak, ["    next(tiles[4][2][{0}]) := tiles[5][{0}][0] &".format(a) for a in range(n)])
panel_1_right =reduce(linebreak, ["    next(tiles[5][{0}][0]) := tiles[0][0][{0}] &".format(i) for i in range(n)])
panel_1_bottom = reduce(linebreak, ["    next(tiles[0][0][{0}]) := tiles[2][{0}][2] &".format(i) for i in range(n)])
panel_1_left = reduce(linebreak, ["    next(tiles[2][{0}][2]) := tiles[4][2][{0}] &".format(i) for i in range(n)])
panel_1_left = edit_tail(panel_1_left, "&","|")
panel_1 = reduce(linebreak, [panel_1_top, panel_1_right, panel_1_bottom, panel_1_left])

# if rotate panel 2
panel_2_top = reduce(linebreak, ["    next(tiles[4][{0}][2]) := tiles[5][{0}][0] &".format(a) for a in range(n)])
panel_2_right =reduce(linebreak, ["    next(tiles[5][{0}][0]) := tiles[1][{0}][2] &".format(i) for i in range(n)])
panel_2_bottom = reduce(linebreak, ["    next(tiles[1][{0}][2]) := tiles[3][{0}][2] &".format(i) for i in range(n)])
panel_2_left = reduce(linebreak, ["    next(tiles[3][{0}][2]) := tiles[4][{0}][2] &".format(i) for i in range(n)])
panel_2_left = edit_tail(panel_2_left, "&","|")
panel_2 = reduce(linebreak, [panel_2_top, panel_2_right, panel_2_bottom, panel_2_left])

# if rotate panel 3
panel_3_top = reduce(linebreak, ["    next(tiles[4][0][{0}]) := tiles[5][{0}][0] &".format(a) for a in range(n)])
panel_3_right =reduce(linebreak, ["    next(tiles[5][{0}][0]) := tiles[2][2][{0}] &".format(i) for i in range(n)])
panel_3_bottom = reduce(linebreak, ["    next(tiles[2][2][{0}]) := tiles[0][{0}][2] &".format(i) for i in range(n)])
panel_3_left = reduce(linebreak, ["    next(tiles[0][{0}][2]) := tiles[4][0][{0}] &".format(i) for i in range(n)])
panel_3_left = edit_tail(panel_3_left, "&","|")
panel_3 = reduce(linebreak, [panel_3_top, panel_3_right, panel_3_bottom, panel_3_left])

# if rotate panel 4
panel_4 = reduce(linebreak, [
  "    next(tiles[3][0]) := tiles[1][0] &",
  "    next(tiles[1][0]) := tiles[0][0] &",
  "    next(tiles[0][0]) := tiles[2][0] &",
  "    next(tiles[2][0]) := tiles[3][0] |"])

# if rotate panel 5
panel_5 = reduce(linebreak, [
  "    next(tiles[1][2]) := tiles[3][2] &",
  "    next(tiles[3][2]) := tiles[0][2] &",
  "    next(tiles[0][2]) := tiles[2][2] &",
  "    next(tiles[2][2]) := tiles[1][2] ;"])

tiles = reduce(linebreak, [panel_0, panel_1, panel_2,panel_3,panel_4,panel_5]) 

#define the solve condition
cube_solved = reduce(linebreak, [
  "        tiles[{0}][{1}][{2}]) = {0} &".format(x,y,z, cube[x][y][z]) for x in range(6) for y in range(n) for z in range(n)])
cube_solved = edit_tail(cube_solved, "&", ";")
define = reduce(linebreak, ["DEFINE",
  "    solved := ", cube_solved])
spec = "SPEC !EF solved" 

# put it all together
print reduce(linebreak, [main,init,tiles,define,spec])

