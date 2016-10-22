import sys
from problemparser import problem
import operator as op
import math

class state_node:
	'base class for the players state'
	total_node = 0
	def __init__(self, parent,row,col,time,indx,prob,goal):
		# setting the goal coor
		goal_row 	= goal[0]
		goal_col 	= goal[1]
		goal_time 	= goal[2]
		self.row 	= row
		self.col 	= col
		self.time 	= time
		self.indx 	= indx
		self.hval = math.fabs(row-goal_row) + math.fabs(col - goal_col) + (goal_time - time)
		#self.hval	= ((row - goal_row)**(2) + (col - goal_col)**(2) + (time - goal_time)**(2))**(0.5)
		#self.hval 		= ((row - goal_row)**(2) + (col - goal_col)**(2))**(0.50)
		if parent == 0:
			self.pre = 0
			self.gval = prob.cost[row][col]
		else:
			self.pre = parent.indx
			self.gval = parent.gval + prob.cost[row][col]


		state_node.total_node += 1
	
	def expand(self, prob, closed,open,goal):
		return_dict = {}				#list to be returned 
		time = self.time + 1
		# retaining the same pos on grid
		if not check_repeat(self.row,self.col,time,closed):
			new_node= state_node(self,self.row,self.col,time,state_node.total_node,prob,goal)
			return_dict.update({new_node: (new_node.hval + new_node.gval)})
		# expanding in row direction
		if self.row < prob.grid - 1:
			row_new = self.row + 1
			if not check_repeat(row_new,self.col,time,closed):
				new_node= state_node(self,row_new,self.col,time,state_node.total_node,prob,goal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})
			
		if self.row > 0:
			row_new = self.row - 1
			if not check_repeat(row_new,self.col,time,closed):
				new_node = state_node(self,row_new,self.col,time,state_node.total_node,prob,goal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})

		# expanding in col dir
		if self.col < prob.grid - 1:
			col_new = self.col + 1
			if not check_repeat(self.row,col_new,time,closed):
				new_node = state_node(self,self.row,col_new,time,state_node.total_node,prob,goal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})

		if self.col > 0:
			col_new = self.col -1
			if not check_repeat(self.row,col_new,time,closed):
				new_node = state_node(self,self.row,col_new,time,state_node.total_node,prob,goal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})

		return return_dict
def check_repeat(row,col,time,state_list):
	# returns  if foound reptition
	for state in state_list:
		if state.row == row and state.col == col and state.time == time:
			return 1
	return 0

def astar(prob,start,goal):
	closed_dict = {}
	start_node = state_node(0,start[0],start[1],0,0,prob,goal)
	open_dict = {start_node:(start_node.gval + start_node.hval)}
	iter = 0
	while True:
		#print(iter)
		iter += 1
		# checking if any viable node is left in open dict:
		open_dict = open_dict_filter(open_dict,goal)
		if len(open_dict) == 0:
			return 0
		node_to_expand = min(open_dict.items(), key=op.itemgetter(1))
		
		if [node_to_expand[0].row,node_to_expand[0].col,node_to_expand[0].time] == goal:
			closed_dict.update({node_to_expand[0]:node_to_expand[1]})
			print 'solution found'
			return [closed_dict, node_to_expand[0]]
		del open_dict[node_to_expand[0]]
		
		new_dict = node_to_expand[0].expand(prob,closed_dict,open_dict,goal);
		open_dict.update(new_dict)
		closed_dict.update({node_to_expand[0]:node_to_expand[1]})

def open_dict_filter(open_dict,goal):
	total_time = goal[2]
	open_list = list(open_dict)
	for item in open_list:
		if item.time > total_time:
			del open_dict[item]

	return open_dict

def backtrack(list_nodes,goal_node):
	next_node = goal_node
	tree = [[next_node.row,next_node.col,next_node.time,next_node.gval]]
	indx = goal_node.pre
	while True:
		# find the next node
		if len(list_nodes) !=0 :
			if next_node.time == 0:
				return tree
			for item in list_nodes:
				if item.indx == indx:
					next_node = item
					indx = next_node.pre
					list_nodes.remove(next_node)
					new_data = [next_node.row,next_node.col,next_node.time,next_node.gval]
					
					tree.append(new_data)
					break
		else:
			return tree




# getting the problem data
print sys.argv[-1]
prob = problem(str(sys.argv[-1]))
plan = []
goal_time = 0
print 'total number of goals ', len(prob.path)
for starts in  prob.path:
	print 'going for goal ', goal_time
	start = [starts[0],starts[1]]  
	goal = [prob.start[0], prob.start[1], goal_time]
	astar_out = astar(prob,start,goal)
	if astar_out != 0:
		plan.append(backtrack(list(astar_out[0]),astar_out[1]))
	goal_time += 1

for item in plan:
	print item[0][3]
	




