from AdjMatGraph import Graph
from queue import Queue 
import numpy as np

INPUT_FILENAME = 'inputPS4.txt'
OUTPUT_FILENAME = 'outputPS4.txt'
PROMPTS_FILENAME = 'promptsPS4.txt'

class FrieghtBooking:
	def readCityTrainfile(self, inputfile):
		# Calculating number of vertices (unique cities)
		f = open(INPUT_FILENAME)
		city_names = set()

		for line in f:
			currentLine = line.split('/')
			for word in currentLine[1:]:
				city_names.add(word.strip())
		f.close()

		no_of_vertices = len(city_names) 
		# print(no_of_vertices)

		# creating graph object with no. of vertices
		G =Graph(no_of_vertices)

		# Setting vertex name to unique city names
		
		for i, city_name in enumerate(city_names, 0):
			G.set_vertex(i, str(city_name))

		# Setting edges (train routes) which are undirected edges
		f = open(INPUT_FILENAME)
		for line in f:
			currentLine = line.split('/')
			train_number = currentLine[0].strip()

			for i, word in enumerate(currentLine[1:-1], 1):
				G.set_edge(word.strip(), currentLine[i + 1].strip(), train_number)
		f.close()

		return G

	def showAll(self, G):
		f = open(OUTPUT_FILENAME, 'w')
		f.write('--------Function showAll --------\n')

		train_names = set()
		for train_name in G.get_edges():
			train_names.add(train_name[2])

		f.write('Total no. of freight trains: ' + str(len(train_names)) + '\n')
		f.write('Total no. of cities: ' + str(G.numvertex) + '\n')
		f.write('List of Freight trains: \n')

		for train_name in train_names:
			f.write(str(train_name) + '\n')

		f.write('\nList of cities: \n')
		for city_name in G.get_vertex():
			f.write(city_name + '\n')

		f.write('---------------------------------------\n\n\n')
		f.close()

	def displayTransportHub(self, G):
		f = open(OUTPUT_FILENAME, 'a')
		adjMatrix = G.adjMatrix
		numvertex = G.numvertex

		max = 0
		vertix_num = 0
		
		for i in range (numvertex):
			count = 0
			for j in range (numvertex):
				if (adjMatrix[i][j]!=-1):
					count += 1
			if count > max :
				max = count
				vertix_num = i

		f.write('--------Function displayTransportHub --------\n')
		f.write('Main transport hub: ' + str(G.get_vertex()[vertix_num]) + '\n')

		no_of_trains = 0
		list_of_trains = ''
		for i in range (numvertex):
			if (adjMatrix[vertix_num][i]!=-1):
				list_of_trains = list_of_trains + str(adjMatrix[vertix_num][i]) + '\n'
				no_of_trains += 1

		f.write('Number of trains visited: ' + str(no_of_trains) + '\n')
		f.write('List of Freight trains:\n' + list_of_trains)
		f.write('-----------------------------------------\n\n\n')
		f.close()

	def displayConnectedCities(self, G, train_to_search):

		'''
		Iterating through all edges and saving the stations which have that train in a set(hashmap) 
		And then printing them
		'''
		f = open(OUTPUT_FILENAME, 'a')
		station_names = set()

		for train in G.get_edges():
			if train[2] == train_to_search:
				station_names.add(train[0])
				station_names.add(train[1])

		f.write('--------Function displayConnectedCities --------\n')
		f.write('Freight train number: ' + train_to_search + '\n')

		if len(station_names) == 0:
			f.write('********     TRAIN NOT FOUND     ***** ' + '\n')
		else:
			f.write('Number of cities connected: ' + str(len(station_names)) + '\n')
			f.write('List of cities connected directly by ' + train_to_search + ':\n')
			for station_name in station_names:
				f.write(str(station_name) + '\n')

		f.write('-----------------------------------------\n\n\n')
		f.close()

	def displayDirectTrain(self, G, city_a, city_b):
		'''
		Iterating through all edges and returning the one with the source and destination 
		cities in it, which will give the train connected to it directly.
		'''
		f = open(OUTPUT_FILENAME, 'a')
		direct_train_name = ''

		f.write('--------Function displayDirectTrain --------\n')
		f.write('City A: ' + city_a + '\n')
		f.write('City B: ' + city_b + '\n')

		for train in G.get_edges():
			if train[0] == city_a and train[1] == city_b:
				direct_train_name = train[2]
				break
		
		if direct_train_name == '':
			f.write('Package can be sent directly: No, there is no direct train' + '\n')
		else:
			f.write('Package can be sent directly: Yes, ' + train[2] + '\n')


		f.write('-----------------------------------------\n\n\n')
		f.close()

	def printpath(self, G, path): 
		path_string = 'Can the package be sent: Yes, '
		length = len(path)
		for i in range(length-1): 
			if i == 0:
				path_string = path_string + path[i] + ' > '
			for train in G.get_edges():
				if train[0] == path[i] and train[1] == path[i + 1]:
					path_string = path_string + train[2]
					break   
			path_string = path_string + ' > ' + path[i + 1] + ' > '
		
		return path_string[:-3] + '\n'

	# Utility function to check if current 
	# vertex is already present in path 
	def isNotVisited(self, x, path): 
		for i in path:  
			if i == x: 
				return 0
		return 1

	def findServiceAvailable(self, G, city_a, city_b):
		'''
		We have implemented this using Breadth-First Search (BFS)
		Algorithm:
			create a queue which will store path(s) in a list
			initialise the queue with first path starting from src

			Now run a loop till queue is not empty
			   get the frontmost path from queue
			   check if the lastnode of this path is destination
				   if true then print the path
			   run a loop for all the vertices connected to the
			   current vertex i.e. lastnode extracted from path
				  if the vertex is not visited in current path
					 a) create a new path from earlier path and 
						 append this vertex
					 b) insert this new path to queue
		'''
		f = open(OUTPUT_FILENAME, 'a')

		f.write('--------Function findServiceAvailable --------\n')
		f.write('City A: ' + city_a + '\n')
		f.write('City B: ' + city_b + '\n')


		isPossible = 0

		q = Queue()
		path = []
		path.append(city_a)
		q.put(path)


		while not q.empty():
			path = q.get() 
			last = path[len(path) - 1]

			#if last vertex is the desired destination, print path 
			if last == city_b:
				f.write(self.printpath(G, path))
				isPossible = 1
				break

			# traverse to all the nodes connected to  
			# current vertex and push new path to queue 
			g = G.get_matrix()
			v = G.get_vertex()
			x= int(v.index(last))

			for i in range(len(g[x])):
				if g[x][i]!=-1:
					if self.isNotVisited(v[i], path): 
						newpath = path[:] 
						newpath.append(v[i]) 
						q.put(newpath) 
			
		if isPossible == 0:
			f.write('Can the package be sent: No, there is no possible way' + '\n')

		f.write('-----------------------------------------\n\n\n')
		f.close()


	def main(self):

		G = self.readCityTrainfile(INPUT_FILENAME)
		self.showAll(G)

		f = open(PROMPTS_FILENAME)
		for line in f:
			currentLine = line.split(':')
			function_to_run = currentLine[0].strip()

			if function_to_run == 'searchTransportHub':
				self.displayTransportHub(G)
			elif function_to_run == 'searchTrain':
				self.displayConnectedCities(G, currentLine[1].strip())
			elif function_to_run == 'searchCities':
				self.displayDirectTrain(G, currentLine[1].strip(), currentLine[2].strip())
			elif function_to_run == 'ServiceAvailability':
				self.findServiceAvailable(G, currentLine[1].strip(), currentLine[2].strip())

		f.close()

		'''self.displayTransportHub(G)
		self.displayConnectedCities(G, 'T1122')
		self.displayConnectedCities(G, 'T007')
		self.displayDirectTrain(G, 'Calcutta','New Delhi')
		self.displayDirectTrain(G, 'Chennai','Hyderabad')
		self.findServiceAvailable(G, 'Calcutta', 'Nagpur')
		self.findServiceAvailable(G, 'Calcutta', 'Mumbai')
		self.findServiceAvailable(G, 'Nagpur', 'Vishakhapatnam')

		print("Vertices of Graph")
		print(G.get_vertex())
		print("Edges of Graph")
		print(G.get_edges())
		print("Adjacency Matrix of Graph")
		print(G.get_matrix())
		print(np.matrix(G.get_matrix()))'''

if __name__=="__main__":
	FrieghtBooking().main()