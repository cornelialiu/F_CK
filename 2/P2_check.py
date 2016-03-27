
##################Assign variables####################
move = [1,1,1] 
face = 1 #the face panel for print
##################Assign variables####################

n = 3
cube = [[[ k for i in range(n)] for j in range(n)] for k in range(6)]


surface = {0:{"top":4,"bottom":5,"left":3,"right":1},
           1:{"top":4,"bottom":5,"left":0,"right":2},
           2:{"top":4,"bottom":5,"left":1,"right":3},
           3:{"top":4,"bottom":5,"left":2,"right":0},
           4:{"top":3,"bottom":1,"left":0,"right":2},
           5:{"top":1,"bottom":3,"left":0,"right":2},
}

def print_cube(face):
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

def play(move_list):
   if move_list != []:
      rotate(move_list[0])
      play(move_list[1:])

print "play move: " + str(move)
play(move)
print "Now it looks like..."
print_cube(face)