from data_extractor import DataExtractor
import networkx as nx
import matplotlib.pyplot as plt

rom = open("zelda.nes", "rb")

de = DataExtractor(rom = rom)
de.Parse()

DOORS = ["Shutter Door", "Door", "Locked Door", "Bomb Hole"]

def position(node):
    tupl, data = node
    if data["room_type"] == "T Room":
        if tupl[2] == 0:
            return (tupl[0], tupl[1]-0.4)
    elif data["room_type"] == "Horiz. Chute":
        if tupl[2] == 0:
            return (tupl[0], tupl[1]-0.4)
        elif tupl[2] == 2:
            return (tupl[0], tupl[1]+0.4)
    elif data["room_type"] == "Vert. Chute":
        if tupl[2] == 0:
            return (tupl[0]-0.4, tupl[1])
        elif tupl[2] == 2:
            return (tupl[0]+0.4, tupl[1])
    return tupl[:2]

for i in range(1,10):
    g = nx.Graph()
    edge_colors = [] #for assigning a color to each edge (which must be done in the order of each edge"s creation)
    node_colors = []
    node_sizes = []


    for room in de.data[i]: #Add each room to a node. Rooms with keys are yellow, otherwise lightblue
        g.add_node(
            (de.data[i][room]["col"], de.data[i][room]["row"], 0),
            color = "lightblue", 
            size = 800, 
            stairway = de.data[i][room]["stair_info"], 
            keys = 0,
            room_type = de.data[i][room]["room_type"],
        )

        if de.data[i][room]["item_info"] in ["Key", "D Key"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["keys"] = 1
            #working on implementing keys and items later
        
        if de.data[i][room]["room_type"] in ["T Room"]: 
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = "orange"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["size"] = 100

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1),
                color = "orange", 
                size = 100, 
                stairway = de.data[i][room]["stair_info"], 
                keys = 0,
                room_type = "T Room",
            )


        elif de.data[i][room]["room_type"] in ["Horiz. Chute"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = "purple"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["size"] = 100

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1),
                color = "purple",
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )
            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2),
                color = "purple",
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )


        elif de.data[i][room]["room_type"] in ["Vert. Chute"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = "pink"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["size"] = 100

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1),
                color = "pink",
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )
            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2),
                color = "pink",
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )


        elif de.data[i][room]["room_type"] in ["Entrance Room"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = "lime"



    for room in de.data[i]: #Add all vertical edges for rooms that are connected
        if i == 1:
            print("Room Stuff (North): ", (de.data[i][room]["col"], de.data[i][room]["row"]), de.data[i][room]["north.wall_type"] )
            print("Room Stuff (East): ", (de.data[i][room]["col"], de.data[i][room]["row"]), de.data[i][room]["east.wall_type"])

        #Check NORTH facing walls
        if de.data[i][room]["north.wall_type"] in DOORS:
            door_color = "green"
            room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],0)
            north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1,0)

            if de.data[i][room]["north.wall_type"] == "Locked Door":
                door_color = "red"

            if g.nodes[room_coords]["room_type"] in ["T Room", "Vert. Chute"]:
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],1)

            if g.nodes[north_room_coords]["room_type"] == "T Room":
                north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1,0)
            elif g.nodes[north_room_coords]["room_type"] == "Vert. Chute":
                north_room_coords = (de.data[i][room]["col"], de.data[i][room]["row"]+1,1)
                
            g.add_edge(
                room_coords,
                north_room_coords,
                color = door_color
            )


        #Check EAST facing walls
        if de.data[i][room]["east.wall_type"] in DOORS:
            door_color = "green"
            room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],0)
            east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"],0)

            if de.data[i][room]["east.wall_type"] == "Locked Door":
                door_color = "red"

            if g.nodes[room_coords]["room_type"] == "Horiz. Chute":
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],1)
            elif g.nodes[room_coords]["room_type"] in ["Vert. Chute"]:
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],2)
            elif g.nodes[room_coords]["room_type"] in ["T Room"]:
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],1)

            if g.nodes[east_room_coords]["room_type"] in ["T Room", "Horiz. Chute"]:
                east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"],1)
                
            g.add_edge(
                room_coords,
                east_room_coords,
                color = door_color
            )


    #Add additional edges for stairway connected rooms
    for u, u_stair in g.nodes(data = "stairway", default = ""):

        if(u_stair[0:3] == "Sta"):

            for v, v_stair in g.nodes(data = "stairway", default = ""):
                if(v_stair[0:3] == "Sta"):
                   
                    #if((u != v) and (u_stair != "") and (v_stair != "")): print(u_stair, v_stair)
                    if((u != v) and (u_stair == v_stair)):
                        #print(u_stair, v_stair)
                        g.add_edge(u,v, color = "magenta")
                        break #Found the stairway matches, move on to the next set

    #Color the edges (uses attributes" information to append colors to edge_colors)
    for u, v, color in g.edges(data = "color", default = "black"):
        edge_colors.append(color)
    
    #Color the nodes (uses attributes" information to append colors to node_colors)
    for u, color in g.nodes(data = "color", default = "lightblue"):
        node_colors.append(color)

    #Assign the nodes their sizes
    for u, size in g.nodes(data = "size", default = "800"):
        node_sizes.append(size)

    nx.draw(g, pos={n[0]: position(n) for n in g.nodes(True)}, with_labels=False, node_color=node_colors, node_size=node_sizes, edge_color = edge_colors, font_size = 10)
    plt.savefig(f"dungeon_level{i}.png") #save the graph in a file
    plt.cla()  # clears the plot for next iteration