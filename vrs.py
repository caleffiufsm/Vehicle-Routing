from six.moves.urllib import request as req
import numpy as np
import math
import copy
import random

#=========================================================================
# Return travel distance and time between provided origin and destination
#=========================================================================
def get_time_and_dist(origin, destination,api):
    origin=origin.replace(" ","+")
    destination=destination.replace(" ","+")
    url='https://maps.googleapis.com/maps/api/distancematrix/json?origins='+origin+'&destinations='+destination+'&key='+api;

    with req.urlopen(url) as response:
        a=response.read().decode('utf-8')
        
        val=[int(s) for s in a.split() if s.isdigit()]
        if not val:
            print("Error in address of either "+origin+" or "+destination)
            return [0,0]
        
    return val
#==========================================================================
# Generate distance matrix for provided nodes
#==========================================================================
def generate_distance_matrix(vertices_ad,api):
    nodes=len(vertices_ad)
    Matrix=[[0 for x in range(nodes)] for y in range(nodes)]
    for i in np.arange(nodes):
        for j in np.arange(i+1,nodes):
            dist=get_time_and_dist(vertices_ad[i],vertices_ad[j],api)[0]
            while(dist==0):
                response=input("Enter correct address for "+vertices_ad[i]+" or type 'C' if address is correct:")
                if response!='C':
                    vertices_ad[i]=response
                    vertices[i]=vertices_ad[i]
                
                response=input("Enter correct address for "+vertices_ad[j]+" or type 'C' if address is correct:")
                if response!='C':
                    vertices_ad[j]=response
                    vertices[j]=vertices_ad[j]
                dist=get_time_and_dist(vertices_ad[i],vertices_ad[j],api)[0]
            
            Matrix[i][j]=dist
            Matrix[j][i]=Matrix[i][j]
            
    return Matrix


#==========================================================================
# Create an edge list from the distance matrix
#==========================================================================
def create_edgelist(dist_mat):
    dist_mat=copy.copy(dist_mat)
    edgelist=[]
    edges=[]
    nodes=len(dist_mat)
    for i in np.arange(nodes):
        for j in np.arange(nodes):
            if (dist_mat[i][j]!=0):
                edges.append((j,dist_mat[i][j]))
        edgelist.append(edges)
        edges=[]

    return edgelist

#==========================================================================
# Create a minimum spanning tree using Prim's Algorithm
#==========================================================================
def MST(vertices,edgelist):
    edgelist=copy.copy(edgelist)
    vertices=copy.copy(vertices)
    S=[]
    S.append(vertices[2])
    vertices.remove(2)
    A=[]
    while(len(vertices)!=0):
        mini=99999999999;
        for i in S:
            edges=edgelist[i]
            for items in edges:
                if ((items[0] not in S) and items[1]<mini):
                    mini=items[1]
                    ed=items
                    st=i
                    end=items[0]
        S.append(end)
        vertices.remove(end)
        A.append((st,ed))

    return A
        

#============================================================================
# Create a minimum weight perfect matching subgraph and return it's union
# with MST (Eulerian graph)
#============================================================================
def perfect_matching(mini_span_tree,edgelist):
    '''Creating a copy to MST and Edgelist to operate on'''
    mini_span_tree=copy.copy(mini_span_tree)
    edgelist=copy.copy(edgelist)
    
    '''count of number of edges in MST'''
    count=len(mini_span_tree)
    '''Dictionary with key=nodes and value=edges incident on the node'''
    odd_edge_nodes=dict.fromkeys(np.arange(count+1),0)
    for items in mini_span_tree:
        odd_edge_nodes[items[0]]=odd_edge_nodes.get(items[0])+1
        odd_edge_nodes[items[1][0]]=odd_edge_nodes.get(items[1][0])+1

    '''keeping nodes with only odd degree'''
    odd_edge_nodes_copy=copy.copy(odd_edge_nodes)
    for key, value in odd_edge_nodes.items():
        if (value%2==0):
            del odd_edge_nodes_copy[key]
    #print(odd_edge_nodes_copy)
    
    '''creating a subgraph of G with odd degree nodes'''
    subgraph={}
    for keys,val in odd_edge_nodes_copy.items():
        subgraph[keys]=[i for i in edgelist[keys] if i[0] in list(odd_edge_nodes_copy.keys())]
        
    #print('Subgraph of G with odd degree nodes',subgraph)

    from mwmatching import maxWeightMatching as mwm
    '''creating a list of edges in subgraph'''
    subgraph1=[]
    edges_traversed=[]
    for key,val in subgraph.items():
        for items in val:
            if (tuple(sorted((key,items[0]))) not in edges_traversed):
                edges_traversed.append(tuple(sorted((key,items[0]))))
                subgraph1.append((key,items[0],-items[1]))  #negative weight on maximum perfect matching

    #print('list of edges in subgraph',subgraph1)
    
    '''Calculating the minimum perfect matching graph'''
    min_perf_match=mwm(subgraph1,True)

    nodes_matched=[]
    matched_edges=[]
    for i in np.arange(len(min_perf_match)):
        if (min_perf_match[i]!=-1 and (min_perf_match[i] not in nodes_matched)):
            nodes_matched.append(i)
            items=edgelist[i]
            for j in items:
                if j[0]==min_perf_match[i]:
                    matched_edges.append((i,j))
                    nodes_matched.append(j[0])

    '''Taking union of matched edges and MST giving a eulerian graph'''
    eulerian_graph=matched_edges+mini_span_tree
    
    return eulerian_graph

#==========================================
# Create a Euler tour in the Eulerian graph
#==========================================
def Euler_tour(graph,nodes):
    edges=[]
    for items in graph:
        edges.append([items[0],items[1][0],items[1][1]])
    #print(edges)

    tour=[0]
    tour_len=0
    i=0
    while(len(edges)>0):
        edges_incident_at_i=[items for items in edges if (items[0]==i or items[1]==i)]
        if len(edges_incident_at_i)>1:
            next_edge=random.choice(edges_incident_at_i)
            if (valid_edge(i,next_edge,edges,nodes)):
                edges.remove(next_edge)
                n=next_edge[:-1]
                n.remove(i)
                #tour.append(i)
                #print(str(i)+'--->'+str(n[0]))
                tour.append(n[0])
                tour_len+=next_edge[2]
                i=n[0]
        elif len(edges_incident_at_i)==1:
            next_edge=edges_incident_at_i[0]
            edges.remove(next_edge)
            n=next_edge[:-1]
            n.remove(i)
            #tour.append(i)
            #print(str(i)+'--->'+str(n[0]))
            tour.append(n[0])
            tour_len+=next_edge[2]
            i=n[0]
    
    #print('tour length=',tour_len)
    return tour

#===========================================
# Check if next chosen edge in Euler tour is
# valid or not based on Fleury's algorithm
#===========================================
def valid_edge(u,edge,edges,nodes):
    '''count the number of nodes reachable
    from u using DFS'''
    count1=DFScount(nodes,edges,u)

    '''count the number of nodes reachable
    from u using DFS after removing edge (u,v)'''
    edges_=copy.copy(edges)
    edges_.remove(edge)
    count2=DFScount(nodes,edges_,u)

    
    return False if count1>count2 else True

#===========================================
# Iterative Depth First Search to count
# reachable nodes
#===========================================
def DFScount(nodes,edges,u):
    
    visited={key: False for key in list(range(nodes))}
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
def cycle(eu_tour,dist_mat,vertices):
    tour=copy.copy(eu_tour)
    cycle=[]
    visited=[]      #Keeping track of nodes already visited
    for i in np.arange(len(tour)):
        if (tour[i] not in visited and i!=len(tour)-1):
            cycle.append(tour[i])
            visited.append(tour[i])
        elif (i==len(tour)-1):
            cycle.append(tour[i])
    #print('Cycle=',cycle)

    cycle_len=0
    for i in np.arange(len(cycle)-1):
        cycle_len+=dist_mat[cycle[i]][cycle[i+1]]
    

    print('######### CHRISTOFIDES TOUR ##########')
    for nodes in cycle:
        print('\n')
        print(vertices[nodes])
    print('\nChristofides tour length=',cycle_len)
    return cycle
            
#===========================================
# Generate tour using Greedy Approach
#===========================================
def greedy_tour(dist_mat,vertices,n_nodes):
    to_be_visited=list(np.arange(n_nodes))
    cycle=[0]
    to_be_visited.remove(0)
    cycle_len=0
    i=0
    while(len(cycle)<n_nodes):
        #print(i)
        lis=dist_mat[i][:]
        lis=[lis[j] for j in to_be_visited if lis[j]>0]
        next_node=to_be_visited[lis.index(min(lis))]
        #print(next_node)
        cycle.append(next_node)
        to_be_visited.remove(next_node)
        cycle_len+=dist_mat[i][next_node]
        i=next_node
    cycle.append(0)
    cycle_len+=dist_mat[next_node][0]
    
    print('########## GREEDY TOUR #########')
    for nodes in cycle:
        print('\n')
        print(vertices[nodes])
    print('\nGreedy tour length=',cycle_len)
    return cycle




vertices=[]

ori=input("Enter Origin Address: ")
vertices.append(ori)
flag=0
count=1
while(flag==0):
    ad=input("Enter intermediate locations (Press # to finish): ")
    if (ad == '#'):
        flag=1
    else:
        vertices.append(ad)
        count=count+1

des=input("Enter Last Address: ")
vertices.append(des)
count=count+1
api=input("Enter google console API: ")


dist_mat=generate_distance_matrix(vertices,api)

edgelist=create_edgelist(dist_mat)

mst=MST(list(np.arange(count)),edgelist)
#print('MST',mst)

euler_graph=perfect_matching(mst,edgelist)
#print('Euler graph=',euler_graph)

eu_tour=Euler_tour(euler_graph,count)

cycle(eu_tour,dist_mat,vertices)

greedy_tour(dist_mat,vertices,count)
