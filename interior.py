from enum import IntEnum

class SpaceMode(IntEnum):
    # Bit pairs for different types of space (flat, sloped, stairs, elevator, escalator)
    FLAT       = 0b0001
    SLOPED     = 0b0010
    STAIRS     = 0b0100
    ELEVATOR   = 0b1000

class Node:
    def __init__(self, x, y, z, name):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.connections = {}
    
    def add_connection(self, name, data):
        if (name in self.connections):
            print(f'Connection from node {self.name} to node {name} already exists!')
        else:
            self.connections[name] = data

    def remove_connection(self, name):
        if (name in self.connections):
            del self.connections[name]
        else:
            print(f'Tried to remove non-existent connection from node {self.name} to node {name}!')

    def get_conn(self, name):
        return self.connections[name]


class Space:
    def __init__(self):
        self.__nodes = []
        
    # Getter methods for private variables
    def get_height(self):
        return self.__height
    
    def get_width(self):
        return self.__width
    
    def get_length(self):
        return self.__length
    
    def get_space_array(self):
        return self.__space_array
    
    # Setter methods for updating the space array
    def set_point(self, x, y, z, point_tuple):
        if 0 <= x < self.__height and 0 <= y < self.__width and 0 <= z < self.__length:
            self.__space_array[x][y][z] = point_tuple
        else:
            print("Invalid coordinates.")
