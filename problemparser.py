class problem:
	'base class for the particular problem'
	def __init__(self,name):
		pro_file = open(name,'r')
		pro_list = list(pro_file)
		pro_file.close()
		# finding the grid size and starting position of the player
		for nitem in range(len(pro_list)):
			pro_list[nitem] = pro_list[nitem].rstrip()
		# finging the path of the target
		marker = 5;
		target_path=[]
		while True:
			if pro_list[marker] == 'B':
				break
			else:
				target_path.append(map(int,pro_list[marker].split(',')))
				marker += 1
		
		# finding the cost of the grid
		grid_cost = []
		marker += 1
		for index in range(int(pro_list[1])):
			grid_cost.append(map(int,pro_list[index + marker].split(',')))
		
		# Defining the properties
		self.grid = int(pro_list[1])
		self.start = map(int,pro_list[3].split(','))
		self.path = target_path
		self.cost = grid_cost
