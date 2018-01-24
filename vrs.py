from urllib import request as req

# Return travel distance and time between provided origin and destination
def get_time_and_dist(origin, destination,api):
    origin=origin.replace(" ","+")
    destination=destination.replace(" ","+")
    url='https://maps.googleapis.com/maps/api/distancematrix/json?origins='+origin+'&destinations='+destination+'&key='+api;

    with req.urlopen(url) as response:
        a=response.read().decode('utf-8')
        val=[int(s) for s in a.split() if s.isdigit()]
        if not val:
            print("Please provide proper address!!!!!")
        else:
            for line in a.splitlines():
                if (line.find('destination')!=-1 or line.find('origin')!=-1):
                    print(line)
            print('Distance= '+str(val[0])+'\nTime= '+str(val[1]))
	

    
        
ori=input("Enter Origin Address: ")
des=input("Enter Destination Address: ")
api=input("Enter google console API: ")
get_time_and_dist(ori,des,api);
