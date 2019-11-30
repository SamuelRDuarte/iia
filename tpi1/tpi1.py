# Samuel Rodrigues Duarte nmec:89222
# durante a execução deste trabalho discuti ideias com:
#   Pedro Valente, 88858
#   Pedro Almeida, 89205
#   Dario Matos, 89288
#   André Alves, 88811
from tree_search import *
import math

class MyTree(SearchTree):

    
    def __init__(self,problem, strategy='breadth',max_nodes=None): 
        self.problem = problem
        self.strategy = strategy
        self.max_nodes = max_nodes
        self.root = SearchNode(problem.initial, None) 
        self.root.cost = 0
        self.root.depth = 0
        self.root.evalfunc = self.problem.domain.heuristic(problem.initial, problem.goal)
        self.root.children = None
        self.open_nodes = [self.root]
        self.solution_cost = 0
        self.solution_length = 0
        self.total_nodes = 0
        self.terminal_nodes = 1
        self.non_terminal_nodes = 0

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes = sorted(self.open_nodes+lnewnodes, key=lambda node: node.evalfunc)

    def effective_branching_factor(self):
        bf = math.pow(self.total_nodes,(1/self.solution_length))   #http://ozark.hendrix.edu/~ferrer/courses/335/f11/lectures/effective-branching.html
        return self.get_branching_factor(bf,1)

    def get_branching_factor(self,bf,error):
        nodes = 1
        for i in range(self.solution_length+1):
            nodes += math.pow(bf,i)
        if nodes - self.total_nodes > error:
            return self.get_branching_factor(bf-0.001,error)
        elif self.total_nodes - nodes > error:
            return self.get_branching_factor(bf+0.001,error)
        elif abs(nodes - self.total_nodes) <= error:
            return bf


    def update_ancestors(self,node):
        if node.children !=[] and node.children is not None:  
            evaluations = [n.evalfunc for n in node.children]
            evaluations.sort(key=lambda x: x)
            node.evalfunc = evaluations[0]
        
        if node.parent == None:
            return
        return self.update_ancestors(node.parent)
        


    def discard_worse(self):
        lista = []
        for n in self.open_nodes: #ver quais são os nodes terminais e adicionar o parent à lista
            if n.children == [] or n.children == None:
                lista.append(n.parent)
        
        for p in lista: #ver da lista dos quais são os "avos" e remove-los
            for c in p.children:
                if c.children != [] and c.children is not None:
                    lista.remove(p)
                    break            

        node_max = max(lista,key=lambda node: node.evalfunc)

        for c in node_max.children:
            if c in self.open_nodes:
                self.open_nodes.remove(c)
                self.terminal_nodes -=1
        node_max.children = None
        self.open_nodes.append(node_max)
        self.non_terminal_nodes -=1
        self.terminal_nodes +=1
        


    def search2(self):
        lista = []
        while self.open_nodes != []:
            if self.max_nodes != None:
                while (self.terminal_nodes+self.non_terminal_nodes) > self.max_nodes:
                    self.discard_worse()
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution_cost = node.cost
                self.total_nodes = len(lista)+1 
                self.solution_length = self.get_number_of_states(node)
                return self.get_path(node)
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                self.solution_cost += self.problem.domain.cost(node.state,a)
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    newnode = SearchNode(newstate,node) 
                    newnode.cost = node.cost+self.problem.domain.cost(node.state,a) 
                    newnode.depth = node.depth+1
                    newnode.evalfunc = newnode.cost + self.problem.domain.heuristic(newstate,self.problem.goal)
                    newnode.children = None
                    if node.children == None:
                        node.children = [newnode]
                    else:
                        node.children.append(newnode)
                    lista.append(newnode)
                    lnewnodes.append(newnode)
            if len(lnewnodes):
                self.terminal_nodes += len(lnewnodes)
                self.non_terminal_nodes += 1
            self.terminal_nodes -=1
            self.add_to_open(lnewnodes)
            self.update_ancestors(node)
        return None


    def get_number_of_states(self,node):
        if node.parent == None:
            return 0
        return 1+self.get_number_of_states(node.parent)
        

    # shows the search tree in the form of a listing
    def show(self,heuristic=False,node=None,indent=''):
        if node==None:
            self.show(heuristic,self.root)
            print('\n')
        else:
            line = indent+node.state
            if heuristic:
                line += (' [' + str(node.evalfunc) + ']')
            print(line)
            if node.children==None:
                return
            for n in node.children:
                self.show(heuristic,n,indent+'  ')


