# Samuel Duarte nmec:89222
#troquei ideias com:
#   Pedro Almeida nmec: 89205
#   Pedro Valente nmec: 88858
#   Renato Valente nmec: 89077   
#   Dário Matos nmec:89288
from semantic_network import *
from bayes_net import *



class MySN(SemanticNetwork):


    def query_dependents(self,entity): 
        tmp = self.get_dependents(entity)
        lista = tmp
        for item in tmp:   #buscar os subtipos e as dependencias para cada item
            subtipos = self.get_subtipos(item)
            if subtipos !=[]:
                lista.remove(item)
            lista += subtipos + self.query_dependents(item)

        subtipos = self.get_subtipos(entity)
        for item in subtipos: #buscar as dependencias para cada subtipo
            lista += self.query_dependents(item)

        return list(set(lista)) #retirar elementos repetidos
        

    def get_subtipos(self, entity,trasverse=True):
        if trasverse:
            return list(d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype) and d.relation.entity2 == entity)
        else:
            return list(d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype) and d.relation.entity1 == entity)
    
    def get_dependents(self,entity, trasverse=True):
        if trasverse:
            return list(d.relation.entity1 for d in self.declarations if isinstance(d.relation, Depends) and d.relation.entity2 == entity)
        else:
            return list(d.relation.entity2 for d in self.declarations if isinstance(d.relation, Depends) and d.relation.entity1 == entity)

    def query_causes(self, entity):
        lista = self.get_dependents(entity, False)
        tmp = lista + self.get_subtipos(entity, False)

        if tmp == []:
            return []

        for item in tmp: #buscar as dependencias para cada item e as suas causas
            deps = self.get_dependents(item, False)
            lista += deps + self.query_causes(item)

        return list(set(lista)) #retirar elementos repetidos

    def query_causes_sorted(self,entity):
        debugs = self.query_local(rel='debug_time') #buscar todas associações com o nome 'degug time'
        lista = []
        for cause in self.query_causes(entity):#para cada causa, buscar os tempos e calcular a media
            tmp = [d.relation.entity2 for d in debugs if d.relation.entity1 == cause]
            lista.append((cause,sum(tmp)/len(tmp)))
        return sorted(lista,key=lambda x: (x[1], x[0])) 

class MyBN(BayesNet):

    def markov_blanket(self,var):
        final = [d[0] for d in list(list(self.dependencies[var])[0])] #buscar os pais de var
        children = []
        for k in self.dependencies:#ver na listas dos pais de cada um, se o var está lá e adicionar
            [children.append(k) for d in list(list(self.dependencies[k])[0]) if var == d[0]]
        final +=children
        for c in children:#buscar os pais dos filhos
            [final.append(d[0]) for d in list(list(self.dependencies[c])[0]) if var != d[0]]
        return final
        
            
        


