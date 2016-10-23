import operator as op
from state_node_time import state_node
from dcost import dcost
from dcost_map import dcost_map
import time
try:
	from Queue import PriorityQueue as pq
except: 
	from queue import PriorityQueue as pq

def mapping(prob,start,goal):
	return(dcost_map(prob,start,goal))
	
def astar(prob,h,start,goal,weight):
	hmap = mapping(prob,start,goal)
	print 'mapping done'

	closed_dict = {}
	start_node = state_node(h,hmap,0,start[0],start[1],0,0,prob,goal)
	open_dict = pq()
	open_dict.put(start_node.gval + start_node.hval,start_node)
	hash_dict_open = {hash_fn(start[0],start[1],0,prob.grid):(start_node.gval + start_node.hval)}
	hash_dict_closed= {}
	max_time = max([item[2] for item in goal])

	iter = 0
	while True:
			# open_dict,goal = open_dict_filter(open_dict,goal)
		if not open_dict.empty():
			node2exp = open_dict.get()
		else:
			print 'open list empty, no solutions found'
			return 0
		#node2exp = min(open_dict.items(), key=op.itemgetter(1))


		key_check =  hash_fn(node2exp.row,node2exp.col,node2exp.time,prob.grid)
		try:
			if hash_dict_open[key_check] < (node2exp.gval + node2exp.hval):
				print iters
				continue
		except:
			pass
		
		#checking if goal is reached
		if goal_check(node2exp,goal):
			closed_dict.update({node2exp.indx:node2exp})
			print 'solution found'
			return [closed_dict, node2exp]
		
		new_dict = node2exp.expand(h,hmap,prob,goal,weight)
		if new_dict ==0 :
			continue

		for item in list(new_dict):
			hash_key = hash_fn(item.row,item.col,item.time,prob.grid)
			if hash_key	not in hash_dict_closed:
				if hash_key	not in hash_dict_open:
					hash_dict_open[hash_key] = item.hval + item.gval 
					open_dict.put(item.gval + item.hval, item)
				else:
					if hash_dict_open[hash_key] > item.gval:
						hash_dict_open[hash_key] = item.gval+ item.hval
						open_dict.put(item.gval+ item.hval,item)
				
		

		closed_dict.update({node2exp.indx:node2exp})
		#print 'new member ', len(closed_dict)
		hash_dict_closed.update({hash_fn(node2exp.row,node2exp.col,node2exp.time,prob.grid):node2exp.gval + node2exp.hval})

		if len(closed_dict) > 49*len(goal):
			print len(closed_dict), ' ', len(open_dict)
		#	raw_input()
		
		iter += 1
		#if node2exp.time > max_time:
			#print 'moving on'
			
		#print 'going to iter ' , iter
		if len(open_dict) == 0:
			#sprint 'len is 0'
			return 0

def open_dict_filter(open_dict,goal):
	time_list = [item[2] for item in goal]
	max_time = max(time_list)
	open_list = list(open_dict)
	for item in open_list:
		if item.time > max_time:
			del open_dict[item]
	# open_time = [item.time for item in list(open_list)]
	# min_avail_time = min(open_time)
	# for item in goal:
	# 	if goal[2]<min_avail_time:
	# 		goal.remove(item)

	return [open_dict,goal]

def goal_check(node,goal):
	for items in goal:

		if [node.row,node.col,node.time]== items:
			return 1
	else:
		return 0 

def hash_fn(row,col,time,grid):
	id = row + col*grid  + grid*grid*time
	return id