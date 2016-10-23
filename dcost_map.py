import state_node_d
from state_node_d import state_node
import operator as op

def dcost_map(prob,start,goal):
	map_dji =  dji(prob,goal)
	#print len(map_dji)
	return map_dji

def dji(prob,goal):
	weight = 1
	open_dict = {}
	hash_dict_open = {}
	hash_dict_closed = {}
	for item in goal:
		start_node = state_node(0,item[0],item[1],0,prob)
		open_dict.update({start_node:start_node.gval})
		hash_dict_open[hash_fn(item[0],item[1],prob.grid)] = prob.cost[item[0]][item[1]]
	#print len(open_dict)
	i = 0
	while True:
		# checking if any viable node is left in open dict:

		node2exp = min(open_dict.items(), key=op.itemgetter(1))

		del open_dict[node2exp[0]]
		
		new_dict = node2exp[0].expand(prob,open_dict,weight)
		
		for item in list(new_dict):
			hash_key = hash_fn(item.row,item.col,prob.grid)
			if hash_key not in hash_dict_closed:
				if hash_key not in hash_dict_open:
					hash_dict_open[hash_fn(item.row,item.col,prob.grid)] = item.gval
					open_dict.update({item:item.gval})
				else:
					if hash_dict_open[hash_key] > item.gval:
						hash_dict_open[hash_fn(item.row,item.col,prob.grid)] = item.gval
						open_dict.update({item:item.gval})

		hash_dict_closed.update({hash_fn(node2exp[0].row,node2exp[0].col,prob.grid): node2exp[0].gval})
		if len(hash_dict_closed)%10000 == 0:
			print len(hash_dict_closed)
		if len(open_dict) == 0:
			return hash_dict_closed

def hash_fn(row,col,grid):
	id = row + col*grid
	return id

def goal_check(node,goal):
	for items in goal:

		if [node.row,node.col]== items:
			return 1
	else:
		return 0 


