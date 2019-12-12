
# Modulo: tree_search
# 
# Fornece um conjunto de classes para suporte a resolucao de 
# problemas por pesquisa em arvore:
#    SearchDomain  - dominios de problemas
#    SearchProblem - problemas concretos a resolver 
#    SearchNode    - nos da arvore de pesquisa
#    SearchTree    - arvore de pesquisa, com metodos para 
#                    a respectiva construcao
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2018,
#  Inteligência Artificial, 2014-2018

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal_state):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    '''
    def goal_test(self, state):
        return state == self.goal
    '''
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,depth,cost,heuristic, action): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.media_detph = 0
        self.action = action
    
    def in_parent(self,state):
        if self.parent == None:
            return False
        return self.parent.state == state or self.parent.in_parent(state)

    def __str__(self):
        return f"no({self.state},{self.parent},{self.depth}, {self.media_detph})"
        #return "no(" + str(self.state) + "," + str(self.parent) + ")"
    
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None,0,0,self.problem.domain.heuristic(problem.initial,problem.goal),None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.length = 0
        self.terminal = 1
        self.non_terminal = 0
        self.ramification = 0
        self.cost = 0
        self.lista_cost = []
        self.media_detph = 0
        self.plan = []

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        #return node     #ver a profundidade
        if node.parent == None:
            return [node.state], []
        path, plan = self.get_path(node.parent)
        path += [node.state]
        plan += [node.action]
        return path, plan

    # procurar a solucao
    def search(self, limit=10):
        maior_custo = 0
        lista = []
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            self.length +=1
            self.cost += node.cost
            total = 0
            lista.append(node)
            for k in lista:
                total += k.depth
            node.media_detph = total/len(lista)
            if node.cost > maior_custo:
                self.lista_cost = [node]
            if node.cost == maior_custo:
                self.lista_cost.append(node)
            if self.problem.goal_test(node.state):
                self.ramification = (self.non_terminal + self.terminal -1)/self.non_terminal
                return self.get_path(node) , node.cost
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if not node.in_parent(newstate) and node.depth < limit:
                    lnewnodes += [SearchNode(newstate,node,node.depth+1, node.cost + 
                            self.problem.domain.cost(node.state,a),self.problem.domain.heuristic(newstate,self.problem.goal),a)]
                if len(lnewnodes):
                    self.terminal += len(lnewnodes)
                else:
                    self.non_terminal += 1
                self.terminal -=1
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.heuristic + node.cost)

