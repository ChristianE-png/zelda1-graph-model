from data_extractor import DataExtractor
import networkx as nx
import matplotlib.pyplot as plt

rom = open("zelda.nes", "rb")

de = DataExtractor(rom = rom)
de.Parse()

for i in range(1,10):
    g = nx.Graph()
    edge_colors = [] #for assigning a color to each edge (which must be done in the order of each edge's creation)
    node_colors = []

    for room in de.data[i]: #Add each room to a node. Rooms with keys are yellow, otherwise lightblue
        g.add_node((de.data[i][room]["col"], de.data[i][room]["row"]))
        print(de.data[i][room]["item_info"] )
        if de.data[i][room]["item_info"] in ["Key", "D Key"]:
            node_colors.append('yellow')
        elif de.data[i][room]["room_type"] in ["T Room"]: 
            node_colors.append('red')
        else:
            node_colors.append('lightblue')

    for room in de.data[i]: #Add all verticle edges for rooms that are connected
        print(de.data[i][room]["north.wall_type"] )
        if de.data[i][room]["north.wall_type"] in ["Shutter Door", "Door", "Bomb Hole", "Locked Door"]:
            g.add_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"], de.data[i][room]["row"]+1))

            if de.data[i][room]["north.wall_type"] in ["Shutter Door"]: #Color each edge based on connection type
                edge_colors.append('purple')
            elif de.data[i][room]["north.wall_type"] in ["Locked Door"]:
                edge_colors.append('red')
            elif de.data[i][room]["north.wall_type"] in ["Bomb Hole"]:
                edge_colors.append('yellow')
            else:
                edge_colors.append('green')
        
        print(de.data[i][room]["west.wall_type"]) #Add all horizontal edges for rooms that are connected
        if de.data[i][room]["west.wall_type"] in ["Shutter Door", "Door", "Bomb Hole", "Locked Door"]:
            g.add_edge((de.data[i][room]["col"], de.data[i][room]["row"]), (de.data[i][room]["col"]-1, de.data[i][room]["row"]))

            if de.data[i][room]["west.wall_type"] in ["Shutter Door"]: #Color each edge based on connection type
                edge_colors.append('purple')
            elif de.data[i][room]["west.wall_type"] in ["Locked Door"]:
                edge_colors.append('red')
            elif de.data[i][room]["west.wall_type"] in ["Bomb Hole"]:
                edge_colors.append('yellow')
            else:
                edge_colors.append('green')

    nx.draw(g, pos={n: n for n in g.nodes()}, with_labels=True, node_color=node_colors, node_size=800, edge_color = edge_colors)
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



