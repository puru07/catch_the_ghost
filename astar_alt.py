import operator as op
from state_node_alt import state_node
def astar(prob,h,start,goal,weight):
	pointA = start
	pointB = goal[0]
	closed_dict = {}
	start_node = state_node(h,0,start[0],start[1],0,0,prob,goal)
	open_dict = {start_node:(start_node.gval + start_node.hval)}
	iter = 0
	while True:
		#print(iter)
		iter += 1
		# checking if any viable node is left in open dict:
		open_dict,goal = open_dict_filter(open_dict,goal)
		if len(open_dict) == 0:
			return 0
		node_to_expand = min(open_dict.items(), key=op.itemgetter(1))
		#checking if goal is reached
		if goal_check(node_to_expand[0],goal):
			closed_dict.update({node_to_expand[0]:node_to_expand[1]})
			print 'solution found'
			return [closed_dict, node_to_expand[0]]
		del open_dict[node_to_expand[0]]
		
		new_dict = node_to_expand[0].expand(h,prob,closed_dict,open_dict,goal,weight,pointA,pointB)
		open_dict.update(new_dict)
		closed_dict.update({node_to_expand[0]:node_to_expand[1]})

def open_dict_filter(open_dict,goal):
	time_list = [item[2] for item in goal]
	max_time = max(time_list)
	open_list = list(open_dict)
	for item in open_list:
		if item.time > max_time:
			del open_dict[item]
	open_time = [item.time for item in list(open_list)]
	min_avail_time = min(open_time)
	for item in goal:
		if item[2]< min_avail_time:
			goal.remove(item)

	return [open_dict,goal]

def goal_check(node,goal):
	for items in goal:

		if [node.row,node.col,node.time]== items:
			return 1
	else:
		return 0 

