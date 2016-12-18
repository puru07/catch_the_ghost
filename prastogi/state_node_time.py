
import math
class state_node:
	'base class for the players state'
	total_node = 0
	def __init__(self,h, hmap,parent,row,col,time,indx,prob,goal):
		# setting the goal coor
		self.row 	= row
		self.col 	= col
		self.time 	= time
		self.indx 	= indx
		hval = []
		if h ==1 :
			for ngoal in goal:
				hval_temp = math.fabs(row-ngoal[0]) + math.fabs(col - ngoal[1]) + (ngoal[2] - time)
				if hval_temp > 0:
					hval.append(hval_temp)
			self.hval = min(hval)
		elif h==2:
			hval_temp = math.fabs(row-ngoal[0]) + math.fabs(col - ngoal[1]) 
			hval.append(hval_temp)
			self.hval = min(hval)
		elif h==3:
			hval_temp = 1.0/(ngoal[2] - time)
			if hval_temp > 0:
				hval.append(hval_temp)
			self.hval = min(hval)
		
		
		elif h ==4:
			
			hash_key = hash_fn(row,col,prob.grid)
			self.hval = hmap[hash_key]
			# print self.hval
		
		#self.hval	= ((row - goal_row)**(2) + (col - goal_col)**(2) + (time - goal_time)**(2))**(0.5)
		#self.hval 		= ((row - goal_row)**(2) + (col - goal_col)**(2))**(0.50)
		if parent == 0:
			self.pre = 0
			self.gval = prob.cost[row][col]
		else:
			self.pre = parent.indx
			self.gval = parent.gval + prob.cost[row][col]

		#print state_node.total_node
		state_node.total_node += 1
	
	def expand(self,h, hmap,prob,goal,w):
		return_dict = {}				#list to be returned 
		max_time = len(prob.path)
		time = self.time + 1
		if time > max_time:
			return 0
		
		# retaining the same pos on grid
		
		new_node= state_node(h,hmap,self,self.row,self.col,time,state_node.total_node,prob,goal)
		return_dict.update({new_node: w*(new_node.hval + new_node.gval)})
		# expanding in row direction
		if self.row < prob.grid - 1:
			row_new = self.row + 1
			
			new_node= state_node(h,hmap,self,row_new,self.col,time,state_node.total_node,prob,goal)
			return_dict.update({new_node: w*(new_node.hval + new_node.gval)})
			
		if self.row > 0:
			row_new = self.row - 1
			
			new_node = state_node(h,hmap,self,row_new,self.col,time,state_node.total_node,prob,goal)
			return_dict.update({new_node: w*(new_node.hval + new_node.gval)})

		# expanding in col dir
		if self.col < prob.grid - 1:
			col_new = self.col + 1
			
			new_node = state_node(h,hmap,self,self.row,col_new,time,state_node.total_node,prob,goal)
			return_dict.update({new_node: w*(new_node.hval + new_node.gval)})

		if self.col > 0:
			col_new = self.col -1
			
			new_node = state_node(h,hmap,self,self.row,col_new,time,state_node.total_node,prob,goal)
			return_dict.update({new_node: w*(new_node.hval + new_node.gval)})
		return return_dict

def check_repeat(row,col,time,hash_dict_closed,grid):
	# returns  if foound reptition
	if hash_fn_3d(row,col,time,grid) in hash_dict_closed:
			return 1
	return 0

def hash_fn(row,col,grid):
	id = row + col*grid  
	return id

def hash_fn_3d(row,col,time,grid):
	id = row + col*grid  + grid*grid*time
	return id