from state_node_time import state_node
#from dcost import dcost
from dcost_map import dcost_map
import time
try:
	from Queue import PriorityQueue as pq
except: 
	from queue import PriorityQueue as pq

def mapping(prob,start,goal):
	return(dcost_map(prob,start,goal))
	
def astar(prob,h,start,goal,weight):
	print 'creating the heuristic map'
	hmap = mapping(prob,start,goal)
	print 'mapping done, begining a*'
	t= time.time()
	goal_hash = [hash_fn(item[0],item[1],item[2],prob.grid) for item in goal]
	closed_dict = {}
	start_node = state_node(h,hmap,0,start[0],start[1],0,0,prob,goal)
	open_dict = pq()
	open_dict.put(((start_node.gval + weight*start_node.hval),start_node))
	hash_dict_open = {hash_fn(start[0],start[1],0,prob.grid):(start_node.gval + weight*start_node.hval)}
	hash_dict_closed= {}
	max_time = max([item[2] for item in goal])

	iter = 0
	while True:
			# open_dict,goal = open_dict_filter(open_dict,goal)
		if not open_dict.empty():
			node2exp = open_dict.get()
			node2exp = node2exp[1]
		else:
			print 'open list empty, no solutions found'
			return 0

		key_check =  hash_fn(node2exp.row,node2exp.col,node2exp.time,prob.grid)
		if key_check in hash_dict_open:
			if hash_dict_open[key_check] < (node2exp.gval + weight*node2exp.hval):
				# print iter
				continue
		
		#checking if goal is reached
		if goal_check(node2exp,goal_hash,prob.grid):
			closed_dict.update({node2exp.indx:node2exp})
			print 'solution found'
			elasp = time.time() - t
			print ' time used for searching ' , elasp
			return [closed_dict, node2exp]
		
		new_dict = node2exp.expand(h,hmap,prob,goal,weight)
		if new_dict ==0 :
			#print 'caught'
			continue

		for item in list(new_dict):
			hash_key = hash_fn(item.row,item.col,item.time,prob.grid)
			if hash_key	not in hash_dict_closed:
				if hash_key	not in hash_dict_open:
					hash_dict_open[hash_key] = (weight*item.hval + item.gval) 
					open_dict.put(((item.gval + weight*item.hval), item))
				else:
					if hash_dict_open[hash_key] > item.gval:
						hash_dict_open[hash_key] = (item.gval+ weight*item.hval)
						open_dict.put(((item.gval+ weight*item.hval),item))

		closed_dict.update({node2exp.indx:node2exp})
		#print 'new member ', len(closed_dict)
		hash_dict_closed.update({hash_fn(node2exp.row,node2exp.col,node2exp.time,prob.grid):(node2exp.gval + weight*node2exp.hval)})

		if len(hash_dict_closed) > prob.grid*prob.grid*len(goal):
			print len(closed_dict), ' '
			raw_input()
		iter += 1
		#if node2exp.time > max_time:
			#print 'moving on'

def goal_check(node,goal_hash,grid):

	if hash_fn(node.row,node.col,node.time,grid) in goal_hash:
		return 1
	else:
		return 0 

def hash_fn(row,col,time,grid):
	id = row + col*grid  + grid*grid*time
	return id