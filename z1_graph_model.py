from data_extractor import DataExtractor
import networkx as nx
import matplotlib.pyplot as plt
import sys



rom = open("zelda.nes", "rb")
de = DataExtractor(rom = rom)
de.Parse()

DOORS = ["Shutter Door", "Door", "Locked Door", "Bomb Hole"]

#for room in de.data[5]:
    #print(de.data[5][room]["room_type"])


#determine the position of nodes for drawing each graph
def position(node):
    tupl, data = node
    foo = tupl[3]

    x = ((foo - 1) % 3) * 8
    y = ((foo - 1) // 3) * 10


    if data["room_type"] == "T Room":
        if tupl[2] == 0:
            return (tupl[0] + x, tupl[1]-0.35 + y)
    elif data["room_type"] in ["Horiz. Chute", "Double Moat"]:
        if tupl[2] == 0:
            return (tupl[0] + x, tupl[1]-0.4 + y)
        elif tupl[2] == 2:
            return (tupl[0] + x, tupl[1]+0.4 + y)
    elif data["room_type"] == "Vert. Chute":
        if tupl[2] == 0:
            return (tupl[0] + x -0.4, tupl[1] + y)
        elif tupl[2] == 2:
            return (tupl[0] + x +0.4, tupl[1]+ y)
    elif data["room_type"] == "Chevy":
        if tupl[2] == 1:
            return (tupl[0] + x -0.4, tupl[1] + y)
        elif tupl[2] == 2:
            return (tupl[0] + x +0.4, tupl[1]+ y)
        elif tupl[2] == 3:
            return (tupl[0] + x, tupl[1]-0.4 + y)
        elif tupl[2] == 4:
            return (tupl[0] + x, tupl[1]+0.4 + y)
    elif data["room_type"] == "Vert. Moat":
        if tupl[2] == 1:
            return (tupl[0] + x +0.2, tupl[1]+ y)
    elif data["room_type"] == "Horiz. Moat":
        if tupl[2] == 1:
            return (tupl[0] + x, tupl[1]+0.35 + y)
    elif data["room_type"] == "Circle Moat":
        if tupl[2] == 1:
            return (tupl[0]+0.2 + x, tupl[1]+0.2 + y)
    elif data["room_type"] == "Overworld":
        return (tupl[0], tupl[1])
    return tupl[0]+ x, tupl[1] + y


#draw the graph and save it to a file
def draw_graph(g, edge_colors, node_colors, node_sizes, filename, labels, font_sizes):
    nx.draw(g, pos={n[0]: position(n) for n in g.nodes(True)}, with_labels=labels, node_color=node_colors, node_size=node_sizes, edge_color = edge_colors, font_size = font_sizes)
    plt.savefig(filename) #save the graph in a file
    plt.cla() #clears the plot for next iteration

#search the graph from a starting node
#currently just walks through the graph without conditional checks on items, keys, etc.


def search_region(G, start, visited=None, inv = []):

    if visited is None:
        visited = set()
    visited.add(start)
    print(start)

    key_count = G.nodes[start]["keys"]
    if key_count > 0:
        G.nodes[start]["keys"] = 0  # collect the keys
    print("Keys collected so far:", key_count)

    if G.nodes[start]["item_info"] != "" and (G.nodes[start]["item_info"] not in inv or G.nodes[start]["item_info"] == "Triforce"):
        inv.append(G.nodes[start]["item_info"])

    print(inv)

    locked_doors = []

    for neighbor in G.neighbors(start):
        if neighbor not in visited:  # avoid locked doors
            if G.edges[start, neighbor]["color"] == "red":
                print("Locked door encountered at edge:", start, "->", neighbor)
                locked_doors.append((start, neighbor))
            elif G.edges[start, neighbor]["color"] in ["cyan", "brown", "blue", "purple"]:
                if G.edges[start, neighbor]["color"] == "cyan":
                    if "Ladder" in inv:
                        G, _, neighbor_keys, new_locked_doors = search_region(G, neighbor, visited)
                        key_count += neighbor_keys
                        locked_doors.extend(new_locked_doors)
                if G.edges[start, neighbor]["color"] == "brown":
                    if "Recorder" in inv:
                        G, _, neighbor_keys, new_locked_doors = search_region(G, neighbor, visited)
                        key_count += neighbor_keys
                        locked_doors.extend(new_locked_doors)
                if G.edges[start, neighbor]["color"] == "blue":
                    if "Raft" in inv:
                        G, _, neighbor_keys, new_locked_doors = search_region(G, neighbor, visited)
                        key_count += neighbor_keys
                        locked_doors.extend(new_locked_doors)
                if G.edges[start, neighbor]["color"] == "purple":
                    count = 0
                    for item in inv:
                        if item == "Triforce":
                            count += 1

                    if count == 8:
                        G, _, neighbor_keys, new_locked_doors = search_region(G, neighbor, visited)
                        key_count += neighbor_keys
                        locked_doors.extend(new_locked_doors)
            else:
                G, _, neighbor_keys, new_locked_doors = search_region(G, neighbor, visited)
                key_count += neighbor_keys
                locked_doors.extend(new_locked_doors)

    #print("Locked Doors in DFS: ", locked_doors)
    return G, visited, key_count, locked_doors

def unlock_blunders(G, locked_doors, total_keys, visited):

    for room in locked_doors:

        print("Blunders: ", room)

        if total_keys > 0:
            
            if room[0] in visited and room[1] in visited:
                total_keys -= 1
                print("Blunders: Using a key to unlock door at edge:", room)
                G.get_edge_data(room[0], room[1])["color"] = "green"
                locked_doors.remove(room)
                
        else:

            return total_keys

    return total_keys

def search_graph(G, start, end_coords, total_keys, path = None, inv = []):

    if path is None:
        path = []
        path.append(start)

    G_copy = G.copy()
    inv_copy = inv.copy()

    G_copy, visited, grabbed_keys, search_locked_doors = search_region(G_copy, start, None, inv_copy)

    visited_copy = visited.copy()
    search_locked_doors_copy = search_locked_doors.copy()
    path_copy = path.copy()

    total_keys += grabbed_keys
    total_keys = unlock_blunders(G_copy, search_locked_doors_copy, total_keys, visited_copy)

    print("\nVisited:", len(visited_copy), "\nTotal Keys:", total_keys, "\nLocked Doors:", search_locked_doors)
    #print(G_copy)

    if end_coords in visited_copy:
        print("GAME OVER: NO SOFTLOCK HERE.")
        print("\nPrinting End Coord Results\nVisited:", len(visited_copy), "\nTotal Keys:", total_keys, "\nLocked Doors:", len(search_locked_doors_copy), "\nPath: ", end="")
        for p in path_copy: print(p, "--> ", end="")
        print("\n")
        return #visited_copy, total_keys, path_copy

    print("Search Locked Doors: ", len(search_locked_doors_copy))

    for room in search_locked_doors_copy:

        if total_keys > 0 or "Magical Key" in inv_copy:
            G_copy.get_edge_data(room[0], room[1])["color"] = "green"

            path_copy.append(room)
            print("Path: ", path_copy)
            
            search_graph(G_copy, start, end_coords, total_keys - 1, path_copy)

            G_copy.get_edge_data(room[0], room[1])["color"] = "red"
            path_copy.remove(room)

    if end_coords not in visited_copy and total_keys == 0 and "Magical Key" not in inv_copy:
        print("GAME OVER. SOFTLOCK DETECTED.\nPath: ", end = "")
        for p in path_copy: print(p, "--> ", end = "")
        #sys.exit("Detected Softlock --> Exiting program.")

    #print("\nVisited:", len(visited), "\nTotal Keys:", total_keys, "\nLocked Doors:", len(search_locked_doors))
    
    return #visited, total_keys, path

    


    
    
#create a world graph to combine all dungeon levels 
#and connect them via their entrances to the overworld
g_world = nx.Graph()
edge_colors_world = []
node_colors_world = ["yellow"]
node_sizes_world = [200]
g_world_entrances = []
g_world_coords = (13, -3, 0, 0)

g_world.add_node(g_world_coords, color = "yellow", size = 200, stairway = "", keys = 0, room_type = "Overworld", item_info = "")

world_keys = 0



for i in range(1,10):
    g = nx.Graph()
    edge_colors = [] #for assigning a color to each edge (which must be done in the order of each edge's creation)
    node_colors = []
    node_sizes = []

    locked_doors = 0
    total_keys = 0


    
    for room in de.data[i]: 
        #add each room to a node
        #nodes consist of x,y coordinates, special node identifiers, and dungeon level
        #rooms are split into multiple nodes if they are special room types (T Rooms, Chutes, etc.)
        #nodes also contain attributes such as color (entrance/doorway type), size (for special rooms), stairway info, keys contained, and room type 
        g.add_node(
            (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
            color = "lightblue", 
            size = 800, 
            stairway = de.data[i][room]["stair_info"], 
            keys = 0,
            room_type = de.data[i][room]["room_type"],
            item_info = de.data[i][room]["item_info"]
        )
        
        if de.data[i][room]["room_type"] in ["T Room"]: 
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "orange"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "orange", 
                size = 40, 
                stairway = de.data[i][room]["stair_info"], 
                keys = 0,
                room_type = "T Room",
                item_info = de.data[i][room]["item_info"]
            )


        elif de.data[i][room]["room_type"] in ["Horiz. Chute"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "purple"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "purple",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )
            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2, i),
                color = "purple",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )


        elif de.data[i][room]["room_type"] in ["Vert. Chute"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "pink"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "pink",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )
            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2, i),
                color = "pink",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

        
        elif de.data[i][room]["room_type"] in ["Double Moat"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "cyan"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "cyan",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2, i),
                color = "cyan",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "cyan"
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 2, i),
                color = "cyan"
            )


        elif de.data[i][room]["room_type"] in ["Chevy"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "brown"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "brown",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2, i),
                color = "brown",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 3, i),
                color = "brown",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 4, i),
                color = "brown",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "cyan"
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 2, i),
                color = "cyan"
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 3, i),
                color = "cyan"
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 4, i),
                color = "cyan"
            )


        elif de.data[i][room]["room_type"] in ["Vert. Moat"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "black"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "black",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "black"
            )


        elif de.data[i][room]["room_type"] in ["Horiz. Moat"]: 
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "navy"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "navy",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "cyan"
            )


        elif de.data[i][room]["room_type"] in ["Circle Moat"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "gray"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["size"] = 40

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "gray",
                size = 40,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
                item_info = de.data[i][room]["item_info"]
            )

            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"], 0, i),
                (de.data[i][room]["col"], de.data[i][room]["row"], 1, i),
                color = "cyan"
            )


        elif de.data[i][room]["room_type"] in ["Entrance Room"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "lime"
            g_world_entrances.append((de.data[i][room]["col"], de.data[i][room]["row"], 0, i))


        if de.data[i][room]["item_info"] in ["Key", "D Key"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["keys"] = 1
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"], 0, i)]["color"] = "gold"
            total_keys += 1
            #working on implementing keys and items later



    for room in de.data[i]: #Add all vertical edges for rooms that are connected
        # if i == 1:
        #     print("Room Stuff (North): ", (de.data[i][room]["col"], de.data[i][room]["row"]), de.data[i][room]["north.wall_type"] )
        #     print("Room Stuff (East): ", (de.data[i][room]["col"], de.data[i][room]["row"]), de.data[i][room]["east.wall_type"])

        #Check NORTH facing walls
        if de.data[i][room]["north.wall_type"] in DOORS:
            door_color = "green"
            room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 0, i)
            north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1, 0, i)

            if de.data[i][room]["north.wall_type"] == "Locked Door":
                door_color = "red"

            if g.nodes[room_coords]["room_type"] in ["T Room", "Vert. Chute", "Double Moat", "Horiz. Moat"]:
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 1, i)
            elif g.nodes[room_coords]["room_type"] == "Horiz. Chute":
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 2, i)
            elif g.nodes[room_coords]["room_type"] == "Chevy":
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 4, i)

            if g.nodes[north_room_coords]["room_type"] == "T Room":
                north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1, 0, i)
            elif g.nodes[north_room_coords]["room_type"] == "Vert. Chute":
                north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1, 1, i)
            elif g.nodes[north_room_coords]["room_type"] == "Double Moat": #this is the exact same as the T Room for Future Reference
                north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1, 0, i)
            elif g.nodes[north_room_coords]["room_type"] == "Horiz. Chute":
                north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1, 0, i)
            elif g.nodes[north_room_coords]["room_type"] == "Chevy":
                north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1, 3, i)

                
            g.add_edge(
                room_coords,
                north_room_coords,
                color = door_color
            )


        #Check EAST facing walls
        if de.data[i][room]["east.wall_type"] in DOORS:
            door_color = "green"
            room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 0, i)
            east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"], 0, i)

            if de.data[i][room]["east.wall_type"] == "Locked Door":
                door_color = "red"

            if g.nodes[room_coords]["room_type"] == "Horiz. Chute":
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 1, i)
            elif g.nodes[room_coords]["room_type"] in ["Vert. Chute"]:
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 2, i)
            elif g.nodes[room_coords]["room_type"] in ["T Room"]:
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 1, i)
            elif g.nodes[room_coords]["room_type"] in ["Double Moat"]:
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 1, i)
            elif g.nodes[room_coords]["room_type"] == "Chevy":
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 2, i)
            elif g.nodes[room_coords]["room_type"] == "Vert. Moat":
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"], 1, i)

            if g.nodes[east_room_coords]["room_type"] in ["T Room", "Horiz. Chute", "Double Moat"]:
                east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"], 1, i)
            elif g.nodes[east_room_coords]["room_type"] in ["Vert. Chute"]:
                east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"], 2, i)
            elif g.nodes[east_room_coords]["room_type"] == "Chevy":
                east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"], 1, i)
            #elif g.nodes[east_room_coords]["room_type"] in ["Vert. Moat"]:
                #east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"], 1, i)
                
            g.add_edge(
                room_coords,
                east_room_coords,
                color = door_color
            )

            


    #Add additional edges for stairway connected rooms
    for u, u_stair in g.nodes(data = "stairway", default = ""):

        #print(u,u_stair)
        if(u_stair[0:3] == "Sta"):

            for v, v_stair in g.nodes(data = "stairway", default = ""):
                if(v_stair[0:3] == "Sta"):
                   
                    #if((u != v) and (u_stair != "") and (v_stair != "")): print(u_stair, v_stair)
                    if((u != v) and (u_stair == v_stair)):
                        #print(u_stair, v_stair)
                        g.add_edge(u,v, color = "magenta")
                        break #Found the stairway matches, move on to the next set

        else:
            
            g.nodes[u]["item_info"] = u_stair

    #Color the edges (uses attributes" information to append colors to edge_colors)
    for u, v, color in g.edges(data = "color", default = "black"):
        edge_colors.append(color)
        edge_colors_world.append(color)

        if(color == "red"):
            locked_doors += 1
    
    #Color the nodes (uses attributes" information to append colors to node_colors)
    for u, color in g.nodes(data = "color", default = "lightblue"):
        node_colors.append(color)
        node_colors_world.append(color)

    #Assign the nodes their sizes
    for u, size in g.nodes(data = "size", default = "800"):
        node_sizes.append(size)
        node_sizes_world.append(size/15)

    #add the dungeon level graph to the world graph
    g_world = nx.compose(g_world, g)

    #draw the dungeon level graph
    draw_graph(g, edge_colors, node_colors, node_sizes, f"dungeon_level{i}.png", True, 10)

    #traverse/search the dungeon level graph
    if (i == 4): traversals = search_graph(g, g_world_entrances[3], end_coords = (6,8,0,4), total_keys = 0)
    #if (i == 1): traversals = search_graph(g, g_world_entrances[0], end_coords = (7,5,0,1), total_keys = 0)

    #print out key and locked door info for the current level
    #print("Keys Found in Level", i, ":", total_keys)
    #print("Locked Doors in Level", i, ":", locked_doors)

    #print out item data for each room
    # for u, item_info in g.nodes(data = "item_info", default = "idk"):
    #     print(u, ": ", item_info)

    #update available keys for player use in the entire world
    world_keys += total_keys - locked_doors
    #print("World Keys Available After Level[",i,"]:", world_keys)



#print("World Keys Available:", world_keys)

for entrance in g_world_entrances:
    g_world.add_edge(g_world_coords, entrance, color = "yellow")
    edge_colors_world.insert(0, "yellow")

draw_graph(g_world, edge_colors_world, node_colors_world, node_sizes_world, f"dungeon_world.png", False, 10)

#traversals = search_graph(g_world, g_world_coords, end_coords = (7,5,0,1), total_keys = 0)