from data_extractor import DataExtractor
import networkx as nx
import matplotlib.pyplot as plt

rom = open("zelda.nes", "rb")

de = DataExtractor(rom = rom)
de.Parse()

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
    edge_colors = [] #for assigning a color to each edge (which must be done in the order of each edge's creation)
    node_colors = []
    node_sizes = []


    for room in de.data[i]: #Add each room to a node. Rooms with keys are yellow, otherwise lightblue
        g.add_node(
            (de.data[i][room]["col"], de.data[i][room]["row"], 0),
            color = 'lightblue', 
            size = 800, 
            stairway = de.data[i][room]["stair_info"], 
            keys = 0,
            room_type = de.data[i][room]["room_type"],
        )

        if de.data[i][room]["item_info"] in ["Key", "D Key"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["keys"] = 1
            #working on implementing keys and items later
        
        if de.data[i][room]["room_type"] in ["T Room"]: 
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = "red"
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["size"] = 100

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1),
                color = 'red', 
                size = 100, 
                stairway = de.data[i][room]["stair_info"], 
                keys = 0,
                room_type = "T Room",
            )


        elif de.data[i][room]["room_type"] in ["Horiz. Chute"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = 'purple'
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["size"] = 100

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1),
                color = 'purple',
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )
            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2),
                color = 'purple',
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )


        elif de.data[i][room]["room_type"] in ["Vert. Chute"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = 'pink'
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["size"] = 100

            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 1),
                color = 'pink',
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )
            g.add_node(
                (de.data[i][room]["col"], de.data[i][room]["row"], 2),
                color = 'pink',
                size = 100,
                stairway = de.data[i][room]["stair_info"],
                keys = 0,
                room_type = de.data[i][room]["room_type"],
            )


        elif de.data[i][room]["room_type"] in ["Entrance Room"]:
            g.nodes[(de.data[i][room]["col"], de.data[i][room]["row"],0)]["color"] = 'lime'



    for room in de.data[i]: #Add all vertical edges for rooms that are connected
        if i == 1:
            print("Room Stuff (North): ", (de.data[i][room]["col"], de.data[i][room]["row"]), de.data[i][room]["north.wall_type"] )

        #Check north facing walls
        if de.data[i][room]["north.wall_type"] == "Shutter Door":
            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"],0),
                (de.data[i][room]["col"], de.data[i][room]["row"]+1,0),
                color = 'green'
            )

        elif de.data[i][room]["north.wall_type"] == "Locked Door":
            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"],0),
                (de.data[i][room]["col"], de.data[i][room]["row"]+1,0),
                color = 'red'
            )

        elif de.data[i][room]["north.wall_type"] == "Door":
            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"],0),
                (de.data[i][room]["col"], de.data[i][room]["row"]+1,0),
                color = 'green'
            )

        elif de.data[i][room]["north.wall_type"] == "Bomb Hole":
            g.add_edge(
                (de.data[i][room]["col"], de.data[i][room]["row"],0),
                (de.data[i][room]["col"], de.data[i][room]["row"]+1,0),
                color = 'green'
            )



        if i == 1:
            print("Room Stuff (East): ", (de.data[i][room]["col"], de.data[i][room]["row"]), de.data[i][room]["east.wall_type"])

        #Check east facing walls
        DOORS = ["Shutter Door", "Door", "Locked Door", "Bomb Hole"]
        if de.data[i][room]["east.wall_type"] in DOORS:
            door_color = 'green'
            room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],0)
            if de.data[i][room]["room_type"] == "Horiz. Chute":
                room_coords = (de.data[i][room]["col"], de.data[i][room]["row"],1)
            if de.data[i][room]["east.wall_type"] == "Locked Door":
                door_color = 'red'
            east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"],0)
            if g.nodes[east_room_coords]["room_type"] in ["T Room", "Horiz. Chute"]:
                east_room_coords = (de.data[i][room]["col"]+1, de.data[i][room]["row"],1)
                
            g.add_edge(
                room_coords,
                east_room_coords,
                color = door_color
            )





    # def check_splits(g, i, room):
    #     if de.data[i][room]["room_type"] in ["T Room"]: #T Room has 3 possible entrances for 1 new node. Add an edge for each, remove the originals.
    #         if g.has_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]+1, de.data[i][room]["row"])):
    #             g.add_edge((de.data[i][room]["col"]+0.30, de.data[i][room]["row"]+0.30), (de.data[i][room]["col"]+1, de.data[i][room]["row"]),
    #             color = 
    #                        g.edges[(de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]+1, de.data[i][room]["row"])]["color"])
    #             g.remove_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]+1, de.data[i][room]["row"]))

    #         if g.has_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]+1)):
    #             g.add_edge((de.data[i][room]["col"]+0.30, de.data[i][room]["row"]+0.30), (de.data[i][room]["col"], de.data[i][room]["row"]+1), color = 
    #                        g.edges[(de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]+1)]["color"])
    #             g.remove_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]+1))

    #         if g.has_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]-1, de.data[i][room]["row"])):
    #             g.add_edge((de.data[i][room]["col"]+0.30, de.data[i][room]["row"]+0.30), (de.data[i][room]["col"]-1, de.data[i][room]["row"]), color = 
    #                        g.edges[(de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]-1, de.data[i][room]["row"])]["color"])
    #             g.remove_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]-1, de.data[i][room]["row"]))

    #     elif de.data[i][room]["room_type"] in ["Vert. Chute"]: #Vertical Chute has 2 possible new entrances for 2 new nodes. Add an edge for each, remove the originals.
    #         if g.has_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]+1, de.data[i][room]["row"])):
    #             g.add_edge((de.data[i][room]["col"]+0.40, de.data[i][room]["row"]+0.35), (de.data[i][room]["col"]+1, de.data[i][room]["row"]), color = 
    #                        g.edges[(de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]+1, de.data[i][room]["row"])]["color"])
    #             g.remove_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]+1, de.data[i][room]["row"]))

    #         if g.has_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]-1, de.data[i][room]["row"])):
    #             g.add_edge((de.data[i][room]["col"]-0.40, de.data[i][room]["row"]-0.35), (de.data[i][room]["col"]-1, de.data[i][room]["row"]), color = 
    #                        g.edges[(de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]-1, de.data[i][room]["row"])]["color"])
    #             g.remove_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]-1, de.data[i][room]["row"]))

    #     elif de.data[i][room]["room_type"] in ["Horiz. Chute"]: #Horizontal Chute has 2 possible new entrances for 2 new nodes. Add an edge for each, remove the originals.
    #         if g.has_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]+1)):
    #             g.add_edge((de.data[i][room]["col"]+0.35, de.data[i][room]["row"]+0.40), (de.data[i][room]["col"], de.data[i][room]["row"]+1), color = 
    #                        g.edges[(de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]+1)]["color"])
    #             g.remove_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]+1))

    #         if g.has_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]-1)):
    #             g.add_edge((de.data[i][room]["col"]-0.35, de.data[i][room]["row"]-0.40), (de.data[i][room]["col"], de.data[i][room]["row"]-1), color = 
    #                        g.edges[(de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]-1)]["color"])
    #             g.remove_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]-1))

    #     return g

    # #Perform the node splits (for T Room, Horiz. Chute, Vert. Chute)
    # for room in de.data[i]:
    #     g = check_splits(g, i, room)

    #Add additional edges for stairway connected rooms
    for u, u_stair in g.nodes(data = 'stairway', default = ''):

        if(u_stair[0:3] == "Sta"):

            for v, v_stair in g.nodes(data = 'stairway', default = ''):
                if(v_stair[0:3] == "Sta"):
                   
                    #if((u != v) and (u_stair != '') and (v_stair != '')): print(u_stair, v_stair)
                    if((u != v) and (u_stair == v_stair)):
                        #print(u_stair, v_stair)
                        g.add_edge(u,v, color = 'magenta')
                        break #Found the stairway matches, move on to the next set

    #Color the edges (uses attributes' information to append colors to edge_colors)
    for u, v, color in g.edges(data = 'color', default = 'black'):
        edge_colors.append(color)
    
    #Color the nodes (uses attributes' information to append colors to node_colors)
    for u, color in g.nodes(data = 'color', default = 'lightblue'):
        node_colors.append(color)

    #Assign the nodes their sizes
    for u, size in g.nodes(data = 'size', default = '800'):
        node_sizes.append(size)

    nx.draw(g, pos={n[0]: position(n) for n in g.nodes(True)}, with_labels=True, node_color=node_colors, node_size=node_sizes, edge_color = edge_colors, font_size = 10)
    plt.savefig(f"dungeon_level{i}.png") #save the graph in a file
    plt.cla()  # clears the plot for next iteration























'''
def build_dungeon_graph(level_data):
    G = Graph()
    grid_size = 4  # 4x4 grid
    room_count = 18
    room_size = 15

    # Doorway types are encoded in byte 0 of each room block
    # Bits: 0x01 = up, 0x02 = down, 0x04 = left, 0x08 = right
    # These bits are set for ANY doorway (bombable, locked, etc.)

    directions = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0)
    }
    bit_flags = {
        'up': 0x01,
        'down': 0x02,
        'left': 0x04,
        'right': 0x08
    }

    for room_index in range(room_count):
        x = room_index % grid_size
        y = room_index // grid_size
        room_id = (x, y)
        G.add_node(room_id)

        room_offset = room_index * room_size
        doorway_byte = level_data[room_offset]  # Byte 0 = doorway flags

        for direction, (dx, dy) in directions.items():
            if doorway_byte & bit_flags[direction]:
                neighbor_x = x + dx
                neighbor_y = y + dy
                if 0 <= neighbor_x < grid_size and 0 <= neighbor_y < grid_size:
                    neighbor_id = (neighbor_x, neighbor_y)
                    G.add_edge(room_id, neighbor_id)

    return G



if __name__ == "__main__":
    import io

    with open("zelda.nes", "rb") as f:
        rom_data = io.BytesIO(f.read())

    reader = RomReader(rom_data)

    level_data = reader.GetLevelInfo(level_num=1)
    print("Level data length:", len(level_data))
    print("Level data sample:", level_data[:17])


    print("Building dungeon graph...")
    G = build_dungeon_graph(level_data)
    print("Graph built with", len(G.nodes), "nodes and", len(G.edges), "edges")


    # Draw using a grid layout
    pos = {(x, y): (x, -y) for (x, y) in G.nodes()}
    nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', node_size=800)
    plt.title("Dungeon Level 1")
    plt.savefig("dungeon_level1.png")
    print("Dungeon graph saved as dungeon_level1.png")
'''



