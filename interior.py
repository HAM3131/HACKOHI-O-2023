from enum import IntEnum
from math import sqrt

class SpaceMode(IntEnum):
    # Bit pairs for different types of space (flat, sloped, stairs, elevator, escalator)
    FLAT       = 0b0001
    SLOPED     = 0b0010
    STAIRS     = 0b0100
    ELEVATOR   = 0b1000

class Node:
    def __init__(self, name, data):
        self.__name = name
        self.__data = data
        self.__connections = {}
    
    def add_connection(self, name, data):
        if (name in self.__connections):
            print(f'[X] Connection from node {self.__name} to node {name} already exists!')
        else:
            self.__connections[name] = data

    def remove_connection(self, name):
        if (name in self.__connections):
            del self.__connections[name]
        else:
            print(f'[X] Tried to remove non-existent connection from node {self.__name} to node {name}!')

    def get_connections(self):
        return self.__connections
    
    def connection_exists(self, name):
        return name in self.__connections

    def get_conn(self, name):
        if (self.connection_exists(name)):
            return self.__connections[name]
        else:
            print(f'[X] There is no connection between the node {self.__name} to {name}')
    
    def get_position(self):
        return (self.__data['x'], self.__data['y'], self.__data['z'])


class Space:
    def __init__(self):
        self.__nodes = {}

    def get_nodes(self):
        return self.__nodes
    
    def get_node(self, name):
        if (not name in self.__nodes):
            print(f'[X] Tried to get nonexistent node {name} from Space')
        else:
            return self.__nodes[name]

    def add_node(self, name, data):
        if (name in self.__nodes):
            print("[X] There is already a node by that name")
        else: 
            self.__nodes[name] = Node(name, data)

    def add_connection(self, name1, name2, connection_data):
        valid_request = True
        if (not name1 in self.__nodes):
            valid_request = False
            print(f"[X] Tried to create connection with nonexistent node {name1}")
        if (not name2 in self.__nodes):
            valid_request = False
            print(f"[X] Tried to create connection with nonexistent node {name2}")
        if (valid_request):
            # We might need to change the data passed if a variable in it is representing direction.
            # For example, we might calculate distance between the nodes and put that in the connection_data
            # before adding the connection, or if one of the two says that the connection is "going up", then
            # that will need to be changed to "going down" for the other node
            self.__nodes[name1].add_connection(name2, connection_data)
            self.__nodes[name2].add_connection(name1, connection_data)

    def remove_connection(self, name1, name2):
        valid_request = True
        if (not name1 in self.__nodes):
            valid_request = False
            print(f"[X] Tried to remove connection with nonexistent node {name1}")
        if (not name2 in self.__nodes):
            valid_request = False
            print(f"[X] Tried to remove connection with nonexistent node {name2}")
        if (valid_request):
            name1.remove_connection(name2)
            name2.remove_connection(name1)
    
    def node_distance(self, name1, name2):
        if (not (self.__nodes[name1].connection_exists(name2) or self.__nodes[name2].connection_exists(name1))):
            print("[*] You are calculating the distance between two nodes which aren't connected")
        (x1, y1, z1) = self.__nodes[name1].get_position()
        (x2, y2, z2) = self.__nodes[name2].get_position()
        (dx, dy, dz) = (x2-x1, y2-y1, z2-z1)
        return sqrt(dx*dx + dy*dy + dz*dz)