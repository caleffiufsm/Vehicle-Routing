from urllib import request as req
import numpy as np

# Return travel distance and time between provided origin and destination
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

# Generates distance matrix for provided nodes
def generate_distance_matrix(vertices,api):
    nodes=len(vertices)
    Matrix=[[0 for x in range(nodes)] for y in range(nodes)]
    for i in np.arange(nodes):
        for j in np.arange(i+1,nodes):
            Matrix[i][j]=get_time_and_dist(vertices[i],vertices[j],api)[0]
            Matrix[j][i]=Matrix[i][j]
    print(np.matrix(Matrix))
    return Matrix





vertices=[]    
ori=input("Enter Origin Address: ")
vertices.append(ori)
flag=0
while(flag==0):
    ad=input("Enter intermediate locations (Press # to finish): ")
    if (ad == '#'):
        flag=1
    else:
        vertices.append(ad)

des=input("Enter Destination Address: ")
vertices.append(des)
api=input("Enter google console API: ")
generate_distance_matrix(vertices,api)
