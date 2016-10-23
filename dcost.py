import state_node_d
from state_node_d import state_node
import operator as op

def dcost(prob,start,goal):
	dji_out = dji(prob,start,goal)
	if dji_out != 0:
		return dji_out[1].gval
	else :
		return 0

def dji(prob,start,goal):
	weight = 1
	closed_dict = {}
	start_node = state_node(0,start[0],start[1],0,prob)
	open_dict = {start_node:(start_node.gval)}

	while True:
		# checking if any viable node is left in open dict:

		if len(open_dict) == 0:
			return 0
		node_to_expand = min(open_dict.items(), key=op.itemgetter(1))
		#checking if goal is reached
		if goal_check(node_to_expand[0],goal):
			closed_dict.update({node_to_expand[0]:node_to_expand[1]})
			
			return [closed_dict, node_to_expand[0]]
		del open_dict[node_to_expand[0]]
		
		new_dict = node_to_expand[0].expand(prob,closed_dict,open_dict,weight)
		open_dict.update(new_dict)
		closed_dict.update({node_to_expand[0]:node_to_expand[1]})



def goal_check(node,goal):
	for items in goal:

		if [node.row,node.col]== items:
			return 1
	else:
		return 0 
def check_repeat_open(new_dict,open_dict):
	for item in list(open_dict):
		for new_item in list(new_dict):
			if [item.row,item.col] == [new_item.row,new_item.col]:
				if item.gval >= new_item.gval:
					del open_dict[item]
					open_dict.update({new_item:new_item.gval})
				else:
					del new_dict[new_item]
	return [new_dict,open_dict]

