from urllib import request as req
import numpy as np
import math
import copy

#=========================================================================
# Returns travel distance and time between provided origin and destination
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
            print("Please provide proper address!!!!!")
        '''else:
            for line in a.splitlines():
                if (line.find('destination')!=-1 or line.find('origin')!=-1):
                    print(line)
            print('Distance= '+str(val[0])+'\nTime= '+str(val[1]))'''
    return val
#==========================================================================
# Generates distance matrix for provided nodes
#==========================================================================
def generate_distance_matrix(vertices,api):
    nodes=len(vertices)
    Matrix=[[0 for x in range(nodes)] for y in range(nodes)]
    for i in np.arange(nodes):
        for j in np.arange(i+1,nodes):
            Matrix[i][j]=get_time_and_dist(vertices[i],vertices[j],api)[0]
            Matrix[j][i]=Matrix[i][j]
    print(np.matrix(Matrix))
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
                if (not(items[0] in S) and items[1]<mini):
                    mini=items[1]
                    ed=items
                    st=i
                    end=items[0]
        S.append(end)
        vertices.remove(end)
        A.append((st,ed))

    return A
        

#===========================================================================
# Create a minimum weight perfect matching subgraph
#===========================================================================
def perfect_matching(mini_span_tree,edgelist):
    mini_span_tree=copy.copy(mini_span_tree)
    edgelist=copy.copy(edgelist)
    
    count=len(mini_span_tree)
    odd_edge_nodes=dict.fromkeys(np.arange(count+1),0)
    for items in mini_span_tree:
        odd_edge_nodes[items[0]]=odd_edge_nodes.get(items[0])+1
        odd_edge_nodes[items[1][0]]=odd_edge_nodes.get(items[1][0])+1

    for key, value in odd_edge_nodes.items():
        if (value%2==0):
            del odd_edge_nodes[key]
    
    subgraph={}
    for keys,val in odd_edge_nodes.items():
        subgraph[keys]=edgelist[keys]

    subgraph1={}
    nodes_traversed=[]
    for key,val in subgraph.items():
        if (key not in nodes_traversed):
            nodes_traversed.append(key)
            mini=9999999999
            for items in val:
                if (items[1]<mini):
                    mini=items[1]
                    node=items[0]
                    tup=items
            nodes_traversed.append(node)
            subgraph1[key]=tup


    return subgraph1

    

'''    
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

des=input("Enter Destination Address: ")
vertices.append(des)
count=count+1
api=input("Enter google console API: ")

edgelist=create_edgelist(generate_distance_matrix(vertices,api))
print(edgelist)
print(MST(list(np.arange(count)),edgelist))
'''
print(perfect_matching([(2, (0, 1780)), (0, (1, 662)), (0, (3, 3554))],[[(1, 662), (2, 1780), (3, 3554)], [(0, 662), (2, 1943), (3, 3711)], [(0, 1780), (1, 1943), (3, 4152)], [(0, 3554), (1, 3711), (2, 4152)]]))
