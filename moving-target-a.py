import sys
from problemparser import problem
import operator as op
import math
from astar_dmap import astar
from state_node_time import state_node

def backtrack(list_nodes,goal_node):
	next_node = goal_node
	print 'cost of path ' , goal_node.gval
	print 'total number of expansions ', goal_node.indx 
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
goal = []
for goals in prob.path:
	goal_temp = [goals[0],goals[1],goal_time]
	goal.append(goal_temp)
	goal_time += 1

start = [prob.start[0],prob.start[1]]
h = 4 # heuristic function
weight = 1
astar_out = astar(prob,h,start,goal,weight)
if astar_out != 0:
	plan = backtrack(list(astar_out[0]),astar_out[1])
print 'the path \n'
for item in plan:
	print (item[0], item[1])





