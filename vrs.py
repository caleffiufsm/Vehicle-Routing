from __future__ import print_function
from six.moves.urllib import request as req
import numpy as np
import math
import copy
import random
import sys

class my_Tour:

    def __init__(self):
        self.vertices=[]    #Creating a list of address to be visited

        '''If running on Python 2'''
        if sys.version_info[:2]<=(2,7):
            origin=raw_input("Enter Origin Address: ")
            self.vertices.append(origin)
            flag=0
            self.node_count=1
            while(flag==0):
                next_node=raw_input("Enter intermediate locations (Press # to finish): ")
                if (next_node == '#'):
                    flag=1
                else:
                    self.vertices.append(next_node)
                    self.node_count+=1
            last_address=raw_input("Enter Last Address: ")
            self.vertices.append(last_address)
            self.node_count+=1
            self.api_key=raw_input("Enter google console API: ")

            '''If running on Python 3'''
        else:
            origin=input("Enter Origin Address: ")
            self.vertices.append(origin)
            flag=0
            self.node_count=1
            while(flag==0):
                next_node=input("Enter intermediate locations (Press # to finish): ")
                if (next_node == '#'):
                    flag=1
                else:
                    self.vertices.append(next_node)
                    self.node_count+=1
            last_address=input("Enter Last Address: ")
            self.vertices.append(last_address)
            self.node_count+=1
            self.api_key=input("Enter google console API: ")

        print("Enter 'your-tour-name.run() to find an efficient delivery route")

    #=================================
    # Run christofides
    #=================================
    def run(self):
        self.create_distance_matrix()
        self.create_edgelist()
        self.create_MST()
        self.create_eulerian_graph()
        self.create_euler_tour()
        self.create_hamiltonian_cycle()
        self.create_greedy_tour()

    #=============================================
    # Generates distance matrix for provided nodes
    #=============================================
    def create_distance_matrix(self):
        '''Creating a distance matrix as list of lists'''
        self.Matrix=[[0 for x in range(self.node_count)] for y in range(self.node_count)]

        for i in np.arange(self.node_count):
            for j in np.arange(i+1,self.node_count):
                distance=self.get_time_and_distance(i,j)[0]

                '''If returned distance is zero, update incorrect address'''
                while(distance==0):
                    if sys.version_info[:2]<=(2,7):
                        response=raw_input("Enter correct address for "+self.vertices[i]+" or type 'C' if address is correct:")
                    else:
                        response=input("Enter correct address for "+self.vertices[i]+" or type 'C' if address is correct:")
                    if response!='C':
                        self.vertices[i]=response

                    if sys.version_info[:2]<=(2,7):
                        response=raw_input("Enter correct address for "+self.vertices[j]+" or type 'C' if address is correct:")
                    else:
                        response=input("Enter correct address for "+self.vertices[j]+" or type 'C' if address is correct:")
                    if response!='C':
                        self.vertices[j]=response

                    distance=self.get_time_and_distance(i,j)[0]

                '''Assuming objective is to minimize the total distance travelled'''
                self.Matrix[i][j]=distance

                '''Assuming undirected graph'''
                self.Matrix[j][i]=self.Matrix[i][j]

    
    #============================================================
    # Return travel distance and time between provided address id
    #============================================================
    def get_time_and_distance(self,address1_id,address2_id):
        address1=self.vertices[address1_id].replace(" ","+")
        address2=self.vertices[address2_id].replace(" ","+")
        url='https://maps.googleapis.com/maps/api/distancematrix/json?origins='+address1+'&destinations='+address2+'&key='+self.api_key;
        response_json= req.urlopen(url)
        response_decoded=response_json.read().decode('utf-8')

        values=[int(line) for line in response_decoded.split() if line.isdigit()]
        if not values:
            print("Error in address of either "+origin+" or "+destination)
            return [0,0]

        return values

    #=============================================
    # Create an edge list from the distance matrix
    #=============================================
    def create_edgelist(self):
        self.edgelist=[]
        edges=[]
        for i in np.arange(self.node_count):
            for j in np.arange(self.node_count):
                if (self.Matrix[i][j]!=0):
                    edges.append((j,self.Matrix[i][j]))
            self.edgelist.append(edges)
            edges=[]

    #======================================================
    # Create a minimum spanning tree using Prim's Algorithm
    #======================================================
    def create_MST(self):
        '''List of unseen vertices'''
        vertices_id=range(self.node_count) 
        S=[]
        '''Initialize a tree with a single vertex'''
        S.append(vertices_id[2])
        vertices_id.remove(2)
        self.MST=[]

        '''Until all the vertices have been seen'''
        while(len(vertices_id)!=0):
            mini=99999999999;

            '''Greedily add minimum weight edge incident on current tree'''
            for i in S:
                edges=self.edgelist[i]
                for items in edges:
                    if ((items[0] not in S) and items[1]<mini):
                        mini=items[1]
                        ed=items
                        st=i
                        end=items[0]
            S.append(end)
            vertices_id.remove(end)
            self.MST.append((st,ed))


    #===============================================
    # Create a union of minimum weight perfect matching subgraph
    # and minimum spanning tree
    #===============================================
    def create_eulerian_graph(self):
        '''count of number of edges in MST'''
        count=len(self.MST)
        
        '''Dictionary with key=nodes and value=edges incident on the node'''
        odd_edge_nodes=dict.fromkeys(range(count+1),0)
        for items in self.MST:
            odd_edge_nodes[items[0]]=odd_edge_nodes.get(items[0])+1
            odd_edge_nodes[items[1][0]]=odd_edge_nodes.get(items[1][0])+1

        '''keeping nodes with only odd degree'''
        odd_edge_nodes_copy=copy.copy(odd_edge_nodes)
        for key, value in odd_edge_nodes.items():
            if (value%2==0):
                del odd_edge_nodes_copy[key]

        '''creating a subgraph of G with odd degree nodes'''
        subgraph={}
        for keys,val in odd_edge_nodes_copy.items():
            subgraph[keys]=[i for i in self.edgelist[keys] if i[0] in list(odd_edge_nodes_copy.keys())]

        from mwmatching import maxWeightMatching as mwm
        '''creating a list pf edges in subgraph'''
        subgraph1=[]
        edges_traversed=[]
        for key,val in subgraph.items():
            for items in val:
                if (tuple(sorted((key,items[0]))) not in edges_traversed):
                    edges_traversed.append(tuple(sorted((key,items[0]))))
                    subgraph1.append((key,items[0],-items[1]))  #negative weight on maximum perfect matching

        '''Calculating the minimum perfect matching graph'''
        min_perf_match=mwm(subgraph1,True)

        nodes_matched=[]
        matched_edges=[]
        for i in np.arange(len(min_perf_match)):
            if (min_perf_match[i]!=-1 and (min_perf_match[i] not in nodes_matched)):
                nodes_matched.append(i)
                items=self.edgelist[i]
                for j in items:
                    if j[0]==min_perf_match[i]:
                        matched_edges.append((i,j))
                        nodes_matched.append(j[0])

        '''Taking union of matched edges and MST giving a eulerian graph'''
        self.eulerian_graph=matched_edges+self.MST

    #==========================================
    # Create a Euler tour in the Eulerian graph
    #==========================================
    def create_euler_tour(self):
        edges=[]
        for items in self.eulerian_graph:
            edges.append([items[0],items[1][0],items[1][1]])

        self.tour=[0]
        tour_len=0
        i=0
        while(len(edges)>0):
            edges_incident_at_i=[items for items in edges if (items[0]==i or items[1]==i)]
            if len(edges_incident_at_i)>1:
                next_edge=random.choice(edges_incident_at_i)
                if (self.valid_edge(i,next_edge,edges)):
                    edges.remove(next_edge)
                    n=next_edge[:-1]
                    n.remove(i)
                    #self.tour.append(i)
                    #print(str(i)+'--->'+str(n[0]))
                    self.tour.append(n[0])
                    tour_len+=next_edge[2]
                    i=n[0]
            elif len(edges_incident_at_i)==1:
                next_edge=edges_incident_at_i[0]
                edges.remove(next_edge)
                n=next_edge[:-1]
                n.remove(i)
                #self.tour.append(i)
                #print(str(i)+'--->'+str(n[0]))
                self.tour.append(n[0])
                tour_len+=next_edge[2]
                i=n[0]

        
    #============================================
    # Check if next chosen edge in Euler tour
    # is valid or not based on Fleury's algorithm
    #============================================
    def valid_edge(self,u,edge,edges):
        '''count the number of nodes reachable
        from u using DFS'''
        count1=self.DFScount(edges,u)

        '''count the number of nodes reachable
        from u using DFS after removing edge (u,v)'''
        edges_=copy.copy(edges)
        edges_.remove(edge)
        count2=self.DFScount(edges_,u)

        
        return False if count1>count2 else True

    #===========================================
    # Iterative Depth First Search to count
    # reachable nodes
    #===========================================
    def DFScount(self,edges,u):
        
        visited={key: False for key in list(range(self.node_count))}
        stack=[]
        stack.append(u)
        while(len(stack)>0):
            w=stack.pop()
            if not visited[w]:
                visited[w]=True
                for items in edges:
                    if items[0]==w:
                        stack.append(items[1])
                    elif items[1]==w:
                        stack.append(items[0])
        return sum(visited.values())

    #===========================================
    # Create a Hamiltonian cycle from Euler tour
    #===========================================
    def create_hamiltonian_cycle(self):
        self.cycle=[]
        '''keeping track of vertices already visited'''
        visited=[]
        for i in range(len(self.tour)):
            if (self.tour[i] not in visited and i!=len(self.tour)-1):
                self.cycle.append(self.tour[i])
                visited.append(self.tour[i])
            elif (i==len(self.tour)-1):
                self.cycle.append(self.tour[i])

        self.cycle_length=0
        for i in range(len(self.cycle)-1):
            self.cycle_length+=self.Matrix[self.cycle[i]][self.cycle[i+1]]

        print('######### CHRISTOFIDES TOUR ##########')
        for nodes in self.cycle:
            print('\n')
            print(self.vertices[nodes])
        print('\nChristofides tour length=',self.cycle_length)


    #===========================================
    # Generate tour using Greedy Approach
    #===========================================
    def create_greedy_tour(self):
        to_be_visited=range(self.node_count)
        self.greedy_cycle=[0]
        to_be_visited.remove(0)
        self.greedy_cycle_length=0
        i=0
        while(len(self.greedy_cycle)<self.node_count):
            #print(i)
            lis=self.Matrix[i][:]
            lis=[lis[j] for j in to_be_visited if lis[j]>0]
            next_node=to_be_visited[lis.index(min(lis))]
            #print(next_node)
            self.greedy_cycle.append(next_node)
            to_be_visited.remove(next_node)
            self.greedy_cycle_length+=self.Matrix[i][next_node]
            i=next_node
        self.greedy_cycle.append(0)
        self.greedy_cycle_length+=self.Matrix[next_node][0]
        
        print('########## GREEDY TOUR #########')
        for nodes in self.greedy_cycle:
            print('\n')
            print(self.vertices[nodes])
        print('\nGreedy tour length=',self.greedy_cycle_length)


if __name__=="__main__":
    print("Create your routing object by typing 'your-tour-name'=my_Tour()")
