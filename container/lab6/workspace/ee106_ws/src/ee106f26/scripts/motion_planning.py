from math import sqrt

def neighbors(current):
    # define the list of 4 neighbors
    neighbors = [(1,0), (0,1), (-1,0), (0,-1)]
    return [ (current[0]+nbr[0], current[1]+nbr[1]) for nbr in neighbors ]

def heuristic_distance(candidate, goal):
    #Using euclidian distance as heuristic
    return (sqrt((candidate[0]-goal[0])**2+(candidate[1]-goal[1])**2))

open_list = []
closed_list = []
nodes = []

def get_path_from_A_star(start, goal, obstacles):
    # input  start: integer 2-tuple of the current grid, e.g., (0, 0)
    #        goal: integer 2-tuple  of the goal grid, e.g., (5, 1)
    #        obstacles: a list of grids marked as obstacles, e.g., [(2, -1), (2, 0), ...]
    # output path: a list of grids connecting start to goal, e.g., [(1, 0), (1, 1), ...]
    #   note that the path should contain the goal but not the start
    #   e.g., the path from (0, 0) to (2, 2) should be [(1, 0), (1, 1), (2, 1), (2, 2)]

    open_list = [start]
    nodes.append({
        "node": start,
        "g": 0,
        "h": heuristic_distance(start, goal),
        "parent_node": "0"
    })
    
    while open_list:
        current = open_list[0]
        index_current = next((i for i, item in enumerate(nodes) if item["node"] == current), None)
        
        closed_list.append(current)
        open_list.remove(current)
        
        # If the node is the goal node, return the path
        if current == goal:
            #pending to return path
            print("goal!")
            print(nodes)
            return 0
        
        node_neighbors = neighbors(current)
        
        for nei in node_neighbors:
            # If the node is in the closed list or if the node is an obstacle, omit
            if nei in closed_list or nei in obstacles:
                continue
                
            calculate_g = nodes[index_current]["g"] + 1
            calculate_h = heuristic_distance(nei, goal)
            
            # Check if there's already a node created, if so check if the distance is lesser and replace it
            index_neighbor = next((i for i, item in enumerate(nodes) if item["node"] == nei), None)
            
            if not index_neighbor == None:
                if calculate_g < nodes[index_neighbor]["g"]:
                    nodes[index_neighbor]["g"] = calculate_g
                    #re-organize list
                    open_list.sort(key=get_f)
            else:
                # Add to nodes list
                node_data = {
                    "node": nei,
                    "g": calculate_g,
                    "h": calculate_h,
                    "parent_node": current
                }
                nodes.append(node_data)

                # Add to open list
                open_list.append(nei)
                
                #re-organize list
                open_list.sort(key=get_f)

def get_f(node):
    index_nodes_list = next((i for i, item in enumerate(nodes) if item["node"] == node), None)
    return nodes[index_nodes_list]["g"] + nodes[index_nodes_list]["h"]