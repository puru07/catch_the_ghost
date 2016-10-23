import dcost
class state_node:
	'base class for the players state'
	total_node = 0
	def __init__(self, parent,row,col,indx,prob):
		# setting the goal coor
		self.row 	= row
		self.col 	= col
		self.indx 	= indx
		if parent == 0:
			self.pre = 0
			self.gval = prob.cost[row][col]
		else:
			self.pre = parent.indx
			self.gval = parent.gval + prob.cost[row][col]
		state_node.total_node += 1
	
	def expand(self, prob,open,w):
		return_dict = {}				#list to be returned 
		# expanding in row direction
		if self.row < prob.grid - 1:
			row_new = self.row + 1
			
			new_node= state_node(self,row_new,self.col,state_node.total_node,prob)
			return_dict.update({new_node: w*( new_node.gval)})
			
		if self.row > 0:
			row_new = self.row - 1
			
			new_node = state_node(self,row_new,self.col,state_node.total_node,prob)
			return_dict.update({new_node: w*( new_node.gval)})

		# expanding in col dir
		if self.col < prob.grid - 1:
			col_new = self.col + 1
			
			new_node = state_node(self,self.row,col_new,state_node.total_node,prob)
			return_dict.update({new_node: w*( new_node.gval)})

		if self.col > 0:
			col_new = self.col -1
	
			new_node = state_node(self,self.row,col_new,state_node.total_node,prob)
			return_dict.update({new_node: w*( new_node.gval)})
		return return_dict

def check_repeat(row,col,state_list):
	# returns  if foound reptition
	for state in state_list:
		if state.row == row and state.col == col:
			return 1
	return 0