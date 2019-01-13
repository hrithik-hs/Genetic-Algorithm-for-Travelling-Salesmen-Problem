import math
import random

class Graph:	
	def __init__(self,gdict=None):
		if gdict is None:
			gdict = {}
		self.gdict = gdict
		
		self.length=0
		self.vertex=[]
	#def __str__(self):
		
	def addVertex(self, vrtx):
		if vrtx not in self.gdict:
			self.gdict[vrtx] = {}
			self.length+=1
			self.vertex.append(vrtx)

	def addEdge(self,v1,v2,w):
		self.addVertex(v1)
		self.addVertex(v2)
		self.gdict[v1][v2]=w		
		self.gdict[v2][v1]=w

	def get_length(self):
		return self.length

	def get_vertex(self):
		return self.vertex

	def show(self):
		print (self.gdict)

def generate_vertex(n):
	lst=[]
	for i in range(n):
		x=random.uniform(0,100)
		y=random.uniform(0,100)
		#print(x,y)
		lst.append((x,y))
	return lst
	#print(lst)

def make_graph(vertices_xy):
	g=Graph()
	for i in range(len(vertices_xy)-1):
		for j in range(i+1,len(vertices_xy)):
			(x1,y1)=vertices_xy[i]
			(x2,y2)=vertices_xy[j]
			w=math.sqrt(math.pow(x2-x1,2.0)+math.pow(y2-y1,2.0))
			g.addEdge(i,j,w)
	return g

class TSP:
	def __init__(self,graph):
		self.graph=graph
		self.gen=0
		self.pop_size=1000
		self.selection_size=500
		self.child_selection_percent=0.8
		self.parent_selection_percent=0.5
		self.population=[]
		self.cross_prob=0.85
		self.mutation_prob=0.15


	def init_population(self):
		lst=self.graph.get_vertex()
		for i in range(self.pop_size):
			temp=lst[:]
			random.shuffle(temp)
			m=Member(temp)
			m.cal_fitness(self.graph)
			self.population.append(m)
		self.population.sort()
	#parent selection
	def parent_selection(self):
		for i in range(self.selection_size,self.pop_size):
			#print(len(self.population))
			#print(i)
			self.population.pop(self.selection_size)
	
	#crossover
	def crossover(self,parent1,parent2):
		child1=[]
		child2=[]
		set1=set()
		set2=set()
		index=random.randint(0,self.graph.get_length())
		#print(index)
		for i in range(index):
			child1.append(parent1.chsm[i])
			child2.append(parent2.chsm[i])
		for i in range(index,self.graph.get_length()):
			set1.add(parent1.chsm[i])
			set2.add(parent2.chsm[i])
		for i in parent2.chsm:
			if i in set1:
				child1.append(i)
		for i in parent1.chsm:
			if i in set2:
				child2.append(i)
		#print(str(parent1.chsm)+"p1")
		#print(str(parent2.chsm)+"p2")
		#print(str(child1)+"c1")
		#print(str(child2)+"c2")
		#input()
		child1=self.mutation(child1)
		child2=self.mutation(child2)
		return (Member(child1),Member(child2))	
	
	def make_edge_map(self,parent1,edge_map):
		if parent1.chsm[0] not in edge_map:
			edge_map[parent1.chsm[0]]=set()
		edge_map[parent1.chsm[0]].add(parent1.chsm[1])
		edge_map[parent1.chsm[0]].add(parent1.chsm[len(parent1.chsm)-1])
		if parent1.chsm[len(parent1.chsm)-1] not in edge_map:	
			edge_map[parent1.chsm[len(parent1.chsm)-1]]=set()
		edge_map[parent1.chsm[len(parent1.chsm)-1]].add(parent1.chsm[len(parent1.chsm)-2])
		edge_map[parent1.chsm[len(parent1.chsm)-1]].add(parent1.chsm[0])
		for i in range(1,len(parent1.chsm)-1):
			j=parent1.chsm[i]
			if j not in edge_map:
				edge_map[j]=set()
			edge_map[j].add(parent1.chsm[i+1])
			edge_map[j].add(parent1.chsm[i-1])

	def edge_recombination(self,parent1,parent2):
		edge_map={}
		self.make_edge_map(parent1,edge_map)
		self.make_edge_map(parent2,edge_map)
		#print (edge_map)
		min_len=list(edge_map)[0]
		for i in edge_map:
			if len(edge_map[min_len])>len(edge_map[i]):
				min_len=i
		start=random.randint(1,len(parent1.chsm)-1)
		child=[]
		child.append(start)
		#print(child)
		for i in edge_map[start]:
			edge_map[i].remove(start)
		del edge_map[start]
		min_len=list(edge_map)[0]
		for i in edge_map:
			if len(edge_map[min_len])>len(edge_map[i]):
				min_len=i
		#print (edge_map)
		for i in range(len(parent1.chsm)-1):
			child.append(min_len)
			for i in edge_map[min_len]:
				edge_map[i].remove(min_len)
			del edge_map[min_len]
			#print (edge_map)
			if len(edge_map)==0:
				break
			min_len=list(edge_map)[0]
			for i in edge_map:
				if len(edge_map[min_len])>len(edge_map[i]):
					min_len=i
		#print(child)

		return Member(self.mutation(child))

	def select_parent(self,p,start,end,cumulative_fitness):
		
		if p<=cumulative_fitness[start]:
			return 0
		if p>cumulative_fitness[end-1]:
			return	end
		mid=int((start+end)/2)
		if p>cumulative_fitness[mid] and p<=cumulative_fitness[mid+1]:
			return mid+1
		if p>cumulative_fitness[mid]:
			return self.select_parent(p,mid,end,cumulative_fitness)
		if p<cumulative_fitness[mid]:
			return self.select_parent(p,start,mid,cumulative_fitness)
		return mid

	def make_child_population(self):
		lst=[]
		max_fitness=self.population[0].fitness
		for i in self.population:
			if(max_fitness<i.fitness):
				max_fitness=i.fitness 
		max_fitness+=10
		cumulative_fitness=[]
		temp=0
		for i in self.population:
			temp+=(max_fitness-i.fitness)
			cumulative_fitness.append(temp)
		while (len(lst)<=self.pop_size):
			p=random.randint(0,int(temp))
			p1=self.select_parent(p,0,len(cumulative_fitness)-1,cumulative_fitness)
			#print(p1)
			parent1=self.population[p1]
			p=random.randint(0,int(temp))				
			p2=self.select_parent(p,0,len(cumulative_fitness)-1,cumulative_fitness)
			while(p1==p2):
				p=random.randint(0,int(temp))
				p2=self.select_parent(p,0,len(cumulative_fitness)-1,cumulative_fitness)
			#print(p2)
			parent2=self.population[p2]
			prob=random.random()
			if(prob<=self.cross_prob):
				child=self.edge_recombination(parent1,parent2)
				lst.append(child)
				#lst.append(child2)
		lst.sort()
		return lst

	def make_new_population(self):
		child_population=self.make_child_population()
		temp_lst=[]
		final_population=[]
		for i in range(int(self.child_selection_percent*self.pop_size)):
			temp_lst.append(child_population[i])
		for i in range(int(self.parent_selection_percent*len(self.population))):
			temp_lst.append(self.population[i])
		temp_lst.sort() 
		for i in range(self.pop_size):
			final_population.append(temp_lst[i])
		self.population=final_population
		#print(self.population)

	#mutation
	def mutation (self,child):
		prob=random.random()
		#print(prob)
		if(prob>=self.mutation_prob):
			return child
		else:
			index1=random.randint(0,len(child)-1)
			index2=random.randint(0,len(child)-1)
			while(index1==index2):
				index2=random.randint(0,len(child)-1)
			temp=child[index1]
			child[index1]=child[index2]
			child[index2]=temp
			return child
	
	def next_gen(self):
		self.gen+=1
		self.parent_selection()
		self.make_new_population()
		for mem in self.population:
			mem.cal_fitness(self.graph)
		self.population.sort()
		#print(self.population[0].fitness)

	def get_population(self):
		return self.population

	def print_pop(self):
		print("\n---------------------------")
		for i in range(10):
			print (self.population[i])
		print("---------------------------")
		for i in range(len(self.population)-10,len(self.population)):
			print (self.population[i])
		print("---------------------------")

class Member:
	def __init__(self,chsm):
		self.chsm=chsm
		self.fitness=0

	def __lt__(self, other):
		return self.fitness < other.fitness
	def __str__(self):
		return str(self.chsm)+" "+str(self.fitness)+" "

	def cal_fitness(self,graph):
		self.fitness=0
		#len(self.chsm)-1self.fitness+=graph.gdict[0][self.chsm[0]]
		for i in range(len(self.chsm)-1):
			self.fitness+=graph.gdict[self.chsm[i]][self.chsm[i+1]]
		self.fitness+=graph.gdict[self.chsm[len(self.chsm)-1]][self.chsm[0]]

class Back:
	def __init__(self):
		self.no_of_vertex=30
		self.vertex_lst=generate_vertex(self.no_of_vertex)
		self.g=make_graph(self.vertex_lst)
		#g.show()
		self.vertex_dict={}
		self.make_vertex_dict()
		self.s=TSP(self.g)
		self.s.init_population()
	def make_vertex_dict(self):
		j=0
		for i in self.vertex_lst:
			self.vertex_dict[j]=i
			j+=1
	def get_solution(self,index):
		solution=[]
		for i in self.s.population[index].chsm:
			solution.append(self.vertex_dict[i])
		return solution	
	def reset(self,n):
		self.no_of_vertex=n
		self.vertex_lst=generate_vertex(self.no_of_vertex)
		self.g=make_graph(self.vertex_lst)
		#g.show()
		self.vertex_dict={}
		self.make_vertex_dict()
		self.s=TSP(self.g)
		self.s.init_population()

	def custom_reset(self,n,lst):
		self.no_of_vertex=n
		self.vertex_lst=lst
		self.g=make_graph(self.vertex_lst)
		#g.show()
		self.vertex_dict={}
		self.make_vertex_dict()
		self.s=TSP(self.g)
		self.s.init_population()




#l=[(1,1),(1,2),(1,3),(1,4),(1,8),(2,8),(3,8),(4,8),(10,8),(10,6),(10,3),(10,1),(6,1),(6,2),(6,3),(5,3),(4,3),(4,2),(3,2),(2,2),(2,1)]

#t=TSP({})
# m1=Member([1,3,5,6,4,2,8,7])
# m2=Member([1,4,2,3,6,5,7,8])
# t.edge_recombination(m1,m2)
'''for i in range(100):
	x=int(input())
	while(x!=0):
		s.next_gen()
		x-=1
	s.print_pop()
'''