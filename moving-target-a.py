import sys
from problemparser import problem
import operator as op


class state_node:
	'base class for the players state'
	total_node = 0
	def __init__(self, parent,row,col,indx,prob,igoal):
		# setting the goal coor
		goal_row = prob.path[igoal][0]
		goal_col = prob.path[igoal][1]

		self.row = row
		self.col = col
		self.indx = indx
		self.hval = ((row - goal_row)*(row - goal_row) + (col - goal_col)*(col-goal_col))**(0.5)
		if parent != 0:
			self.pre = parent.indx
			self.gval = parent.gval + prob.cost[row][col]
		else:
			self.pre = 0
			self.gval = prob.cost[row][col]


		state_node.total_node += 1
	
	def expand(self, prob, closed,open,igoal):
		return_dict = {}				#list to be returned 

		# expanding in row direction
		if self.row < prob.grid - 1:
			row_new = self.row + 1
			if not check_repeat(row_new,self.col,closed):
				new_node= state_node(self,row_new,self.col,state_node.total_node,prob,igoal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})
			
		if self.row > 0:
			row_new = self.row - 1
			if not check_repeat(row_new,self.col,closed):
				new_node = state_node(self.indx,row_new,self.col,state_node.total_node,prob,igoal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})

		# expanding in col dir
		if self.col < prob.grid - 1:
			col_new = self.col + 1
			if not check_repeat(self.row,col_new,closed):
				new_node = state_node(self.indx,self.row,col_new,state_node.total_node,prob,igoal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})

		if self.col > 0:
			col_new = self.col -1
			if not check_repeat(self.row,col_new,closed):
				new_node = state_node(self.indx,self.row,col_new,state_node.total_node,prob,igoal)
				return_dict.update({new_node: (new_node.hval + new_node.gval)})

		return return_dict
def check_repeat(row,col,state_list):
	# returns  if foound reptition
	for state in state_list:
		if state.row == row and state.col == col:
			return 1
	return 0

def astar(prob,igoal):
	closed_dict = {}
	start_node = state_node(0,prob.start[0],prob.start[1],0,prob,igoal)
	open_dict = {start_node:(start_node.gval + start_node.hval)}

	new_dict = start_node.expand(prob,closed_dict,open_dict,igoal);
	open_dict.update(new_dict)
	closed_dict.update({start_node:open_dict[start_node]})
	del open_dict[start_node]
	for item in open_dict:
		print item.indx 

# getting the problem data
print sys.argv[-1]
prob = problem(str(sys.argv[-1]))

astar(prob,-1)


