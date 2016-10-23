import operator as op
from state_node_time import state_node
from dcost import dcost
from dcost_map import dcost_map

def mapping(prob,start,goal):
	return(dcost_map(prob,start,goal))
	
def astar(prob,h,start,goal,weight):
	hmap = mapping(prob,start,goal)
	print 'mapping done'

	closed_dict = {}
	start_node = state_node(h,hmap,0,start[0],start[1],0,0,prob,goal)
	open_dict = {start_node:(start_node.gval + start_node.hval)}
	hash_dict_open = {hash_fn(start[0],start[1],0,prob.grid):(start_node.gval + start_node.hval)}
	hash_dict_closed= {}
	max_time = max([item[2] for item in goal])

	iter = 0
	while True:
			# open_dict,goal = open_dict_filter(open_dict,goal)
		node2exp = min(open_dict.items(), key=op.itemgetter(1))
		del open_dict[node2exp[0]]

		key_check =  hash_fn(node2exp[0].row,node2exp[0].col,node2exp[0].time,prob.grid)
		try:
			if hash_dict_open[key_check] < (node2exp[0].gval + node2exp[0].hval):
				print iters
				continue
		except:
			pass
		
		#checking if goal is reached
		if goal_check(node2exp[0],goal):
			closed_dict.update({node2exp[0]:node2exp[1]})
			print 'solution found'
			return [closed_dict, node2exp[0]]
		
		new_dict = node2exp[0].expand(h,hmap,prob,closed_dict,open_dict,goal,weight,hash_dict_closed)
		if new_dict ==0 :
			continue

		for item in list(new_dict):
			hash_key = hash_fn(item.row,item.col,item.time,prob.grid)
			if hash_key	not in hash_dict_closed:
				hash_dict_open[hash_key] = item.hval + item.gval 
				open_dict.update({item: (item.gval + item.hval)})
			else:
				continue

		if len(hash_dict_closed) != 0:
			if hash_fn(node2exp[0].row,node2exp[0].col,node2exp[0].time,prob.grid) in hash_dict_closed:
				# print 'caught'
				continue
		
		open_dict,goal = open_dict_filter(open_dict,goal)

		closed_dict.update({node2exp[0]:node2exp[1]})
		#print 'new member ', len(closed_dict)
		hash_dict_closed.update({hash_fn(node2exp[0].row,node2exp[0].col,node2exp[0].time,prob.grid):node2exp[1]})

		if len(closed_dict) > 49*len(goal):
			print len(closed_dict), ' ', len(open_dict)
		#	raw_input()
		
		iter += 1
		#if node2exp[0].time > max_time:
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