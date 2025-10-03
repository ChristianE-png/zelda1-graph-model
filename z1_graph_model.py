#Christian Ellington
#J00735086
#z1_graph_model.py


import networkx as nx



print("Hello, Hyrule.")

#Create an empty graph of hyrule's requirements/connections
z1g = nx.Graph() #For undirected graph
#z1g = nx.DiGraph() #For a directed graph

#Ruleset
    #Nodes are all dungeon rooms + the overworld
    #Edges are dungeon rooms/overworld areas that connect to one another
    #Nodes contain item and key attributes. Items consist of key items or keys that are picked up throughout the game.
    #Edges contain required and keyNeeded attributes. 
        #required items are key items the player must have to enter the room.
        #keyNeeded implies that the player must use a key to enter the room.
    #My current concern is with the player not picking up the sword.
        #Use bombs/other items to get by these req's, but how do you know you can get them in the first place?
        #Makes rooms with required fights (boss and combat rooms) a bit harder to navigate

#Overworld Node (Connected to all dungeon entrances + Overworld Requirements)
z1g.add_node("Overworld") 

#Level 1 Nodes
z1g.add_node("L1_R1", items = [], keys = 1)
z1g.add_node("L1_R2", items = [], keys = 1)
z1g.add_node("L1_R3", items = [], keys = 0)
z1g.add_node("L1_R4", items = [], keys = 0)
z1g.add_node("L1_R5", items = [], keys = 1)
z1g.add_node("L1_R6", items = [], keys = 0)
z1g.add_node("L1_R7", items = [], keys = 0)
z1g.add_node("L1_R8", items = [], keys = 0)
z1g.add_node("L1_R9", items = [], keys = 0)
z1g.add_node("L1_R10", items = ["Wooden_Boomerang"], keys = 0)
z1g.add_node("L1_R11", items = [], keys = 1)
z1g.add_node("L1_R12", items = [], keys = 1)
z1g.add_node("L1_R13", items = [], keys = 0)
z1g.add_node("L1_R14", items = ["Triforce_Piece"], keys = 0)
z1g.add_node("L1_R15", items = [], keys = 0)
z1g.add_node("L1_R16", items = [], keys = 1)
z1g.add_node("L1_B1", items = ["Bow"], keys = 0) #This is the basement/staircase room
#Probably won't end up needing these, they can just be absorbed into L1_R15 since it houses the room

z1g.add_edge("Overworld", "L1_Ent", required = [], keyNeeded = False)

z1g.add_edge("L1_Ent", "L1_R1", required = [], keyNeeded = False)
z1g.add_edge("L1_Ent", "L1_R2", required = [], keyNeeded = False)
z1g.add_edge("L1_Ent", "L1_R3", required = [], keyNeeded = True)

z1g.add_edge("L1_R3", "L1_R5", required = [], keyNeeded = False)

z1g.add_edge("L1_R4", "L1_R5", required = [], keyNeeded = False)
z1g.add_edge("L1_R4", "L1_R8", required = [], keyNeeded = True)
z1g.add_edge("L1_R5", "L1_R6", required = [], keyNeeded = False)
z1g.add_edge("L1_R5", "L1_R9", required = [], keyNeeded = False)
z1g.add_edge("L1_R6", "L1_R10", required = [], keyNeeded = False)

z1g.add_edge("L1_R7", "L1_R8", required = [], keyNeeded = False)
z1g.add_edge("L1_R8", "L1_R9", required = [], keyNeeded = False)
z1g.add_edge("L1_R9", "L1_R10", required = [], keyNeeded = True)
z1g.add_edge("L1_R9", "L1_R12", required = [], keyNeeded = False)
z1g.add_edge("L1_R10", "L1_R11", required = [], keyNeeded = False)
z1g.add_edge("L1_R11", "L1_R13", required = [], keyNeeded = True)

z1g.add_edge("L1_R12", "L1_R16", required = [], keyNeeded = True)
z1g.add_edge("L1_13", "L1_R14", required = [], keyNeeded = False)

z1g.add_edge("L1_R15", "L1_R16", required = [], keyNeeded = True)
z1g.add_edge("L1_R15", "L1_B1", required = [], keyNeeded = False) #Same deal as above


#Overworld Requirements(nodes and edges) (these will be reorganized later)
z1g.add_node("L4_Ent", items = [], keys = 0)
z1g.add_node("L7_Ent", items = [], keys = 0) #these are temp

z1g.add_edge("Overworld", "L4_Ent", required = ["Raft"], keyNeeded = False)
z1g.add_edge("Overworld", "L7_Ent", required = ["Whistle"], keyNeeded = False)










print("Nodes:", z1g.nodes())
print("Edges:", z1g.edges())