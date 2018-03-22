def DFS(nodes,edges,u):
    count1=0
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
    print(visited)

edges=[[1, 4, 3243721], [1, 5, 1271586],
       [5, 0, 346538], [1, 3, 3078824], [3, 4, 761089]]
DFS(7,edges,1)
