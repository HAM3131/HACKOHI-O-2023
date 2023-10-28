from math import sqrt, floor, atan2, degrees
import plotly.graph_objects as go
import random
import copy

class NodeType():
    # Bit pairs for different types of space (flat, sloped, stairs, elevator, escalator)
    ROOM        = "room"
    STAIRS      = "stairs"
    ELEVATOR    = "elevator"
    ESCALATOR   = "escalator"
    DOOR        = "door"
    HALLWAY     = "hallway"
    EXIT        = "exit"
    OUTSIDE     = "outside"
    OTHER       = "other"

class Node:
    def __init__(self, name, data):
        self.__name = name
        self.__data = data
        self.__connections = {}

    def print(self):
        type = self.get_type()
        if (type == NodeType.ROOM):
            return f"{self.__name}"
        elif (type == NodeType.STAIRS):
            return f"the {self.__name}"
        elif (type == NodeType.ELEVATOR):
            return f"the {self.__name}"
        elif (type == NodeType.ESCALATOR):
            return f"the {self.__name}"
        elif (type == NodeType.DOOR):
            return f"the {self.__name}"
        elif (type == NodeType.HALLWAY):
            return f"the {self.__name}"
        elif (type == NodeType.EXIT):
            return f"the {self.__name}"
        elif (type == NodeType.OUTSIDE):
            return f"{self.name}"
        elif (type == NodeType.OTHER):
            return f"{self.name}"
    
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
    
    def get_type(self):
        return (self.__data.get('type', NodeType.OTHER))
    
    def get_mult(self):
        return (self.__data.get('mult', 1))


class Space:
    def __init__(self, units="feet"):
        self.__nodes = {}
        self.units = units

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

    def remove_node(self, name):
        remNode = self.get_node(name)
        connections = [x for x in remNode.get_connections().keys()]
        for connection in connections:
            self.remove_connection(name, connection)


    def add_connection(self, name1, name2):
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
            connection_data = {}
            baseDistance = self.node_distance(name1, name2, True)
            realDistance = min(self.get_node(name1).get_mult(), self.get_node(name2).get_mult()) * baseDistance
            connection_data['distance'] = realDistance
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
            self.get_node(name1).remove_connection(name2)
            self.get_node(name2).remove_connection(name1)
    
    def node_distance(self, name1, name2, disable_warning=False):
        if (not (self.__nodes[name1].connection_exists(name2) or self.__nodes[name2].connection_exists(name1)) and not disable_warning):
            print("[*] You are calculating the distance between two nodes which aren't connected")
        (x1, y1, z1) = self.__nodes[name1].get_position()
        (x2, y2, z2) = self.__nodes[name2].get_position()
        (dx, dy, dz) = (x2-x1, y2-y1, z2-z1)
        return sqrt(dx*dx + dy*dy + dz*dz)
    
    def node_y_distance(self, name1, name2, disable_warning=False):
        if (not (self.__nodes[name1].connection_exists(name2) or self.__nodes[name2].connection_exists(name1)) and not disable_warning):
            print("[*] You are calculating the distance between two nodes which aren't connected")
        (_, y1, _) = self.__nodes[name1].get_position()
        (_, y2, _) = self.__nodes[name2].get_position()
        return y2-y1
    
    def get_intermediate_direction(self, node1_name, node2_name):
        if node1_name not in self.__nodes or node2_name not in self.__nodes:
            return "Invalid node names"

        x1, y1, _ = self.__nodes[node1_name].get_position()
        x2, y2, _ = self.__nodes[node2_name].get_position()

        dx = x2 - x1
        dy = y2 - y1

        angle = (180 / 3.14159) * (atan2(dy, dx) % (2 * 3.14159))

        if 22.5 <= angle < 67.5:
            return "Northeast"
        elif 67.5 <= angle < 112.5:
            return "East"
        elif 112.5 <= angle < 157.5:
            return "Southeast"
        elif 157.5 <= angle < 202.5:
            return "South"
        elif 202.5 <= angle < 247.5:
            return "Southwest"
        elif 247.5 <= angle < 292.5:
            return "West"
        elif 292.5 <= angle < 337.5:
            return "Northwest"
        else:
            return "North"
        
    def get_clock_direction(self, node1_name, node2_name, node3_name):
        if any(name not in self.__nodes for name in [node1_name, node2_name, node3_name]):
            return "Invalid node names"

        x1, y1, _ = self.__nodes[node1_name].get_position()
        x2, y2, _ = self.__nodes[node2_name].get_position()
        x3, y3, _ = self.__nodes[node3_name].get_position()

        angle1 = degrees(atan2(y2 - y1, x2 - x1)) % 360
        angle2 = degrees(atan2(y3 - y1, x3 - x1)) % 360

        clock_angle = (angle2 - angle1 + 360) % 360
        clock_direction = round(clock_angle / 30) % 12

        if clock_direction == 0:
            return "12 o'clock"
        else:
            return f"{clock_direction} o'clock"
    
    def plot_space(self):
        # Initialize lists to store node and edge coordinates
        x_nodes, y_nodes, z_nodes = [], [], []
        x_edges, y_edges, z_edges = [], [], []

        # Populate node coordinates
        for _, node in self.__nodes.items():
            x, y, z = node.get_position()
            x_nodes.append(x)
            y_nodes.append(y)
            z_nodes.append(z)

        # Populate edge coordinates
        for _, node1 in self.__nodes.items():
            x1, y1, z1 = node1.get_position()
            for name2 in node1.get_connections():
                x2, y2, z2 = self.__nodes[name2].get_position()
                x_edges.extend([x1, x2, None])
                y_edges.extend([y1, y2, None])
                z_edges.extend([z1, z2, None])

        # Create a scatter plot for nodes with blue color
        scatter = go.Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes, mode='markers', marker=dict(size=8, color='blue'))

        # Create a line plot for edges with white color
        lines = go.Scatter3d(x=x_edges, y=y_edges, z=z_edges, mode='lines', line=dict(color='white'))

        # Create a Surface plot for the Z-plane
        plane = go.Surface(
            x=[0, 10],
            y=[0, 10],
            z=[[-0.5,-0.5],[-0.5,-0.5]],
            colorscale=[[0, 'gray'], [1, 'gray']],  # set plane color to gray
            showscale=False  # hide the color scale
        )

        # Create the 3D plot
        fig = go.Figure(data=[scatter, lines, plane])

        # Customize the layout
        fig.update_layout(
        scene=dict(
            zaxis=dict(
                showbackground=False,  # Show z-axis plane
                showticklabels=False,  # Hide tick labels
                showgrid=False,  # Hide grid lines
                zeroline=False,  # Hide zero line
                title=''
            ),
            yaxis=dict(
                showbackground=False,  # Hide y-axis plane
                showticklabels=False,  # Hide tick labels
                showgrid=False,  # Hide grid lines
                zeroline=False,  # Hide zero line
                title=''
            ),
            xaxis=dict(
                showbackground=False,  # Hide x-axis plane
                showticklabels=False,  # Hide tick labels
                showgrid=False,  # Hide grid lines
                zeroline=False,  # Hide zero line
                title=''
            ),
            bgcolor='black'  # Black background
        ),
        paper_bgcolor='black',  # Black surrounding background
        plot_bgcolor='black',  # Black grid background
        scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))  # Adjust camera
    )

        fig.show()

    def plot_space_highlight(self, highlight_nodes):
        # Initialize lists to store node and edge coordinates
        x_nodes, y_nodes, z_nodes = [], [], []
        x_edges, y_edges, z_edges = [], [], []
        x_highlight, y_highlight, z_highlight = [], [], []
        x_highlight_edges, y_highlight_edges, z_highlight_edges = [], [], []

        # Populate node coordinates
        for name, node in self.__nodes.items():
            x, y, z = node.get_position()
            if name in highlight_nodes:
                x_highlight.append(x)
                y_highlight.append(y)
                z_highlight.append(z)
            else:
                x_nodes.append(x)
                y_nodes.append(y)
                z_nodes.append(z)

        # Populate edge coordinates
        for name1, node1 in self.__nodes.items():
            x1, y1, z1 = node1.get_position()
            for name2 in node1.get_connections():
                x2, y2, z2 = self.__nodes[name2].get_position()
                if name1 in highlight_nodes and name2 in highlight_nodes:
                    x_highlight_edges.extend([x1, x2, None])
                    y_highlight_edges.extend([y1, y2, None])
                    z_highlight_edges.extend([z1, z2, None])
                else:
                    x_edges.extend([x1, x2, None])
                    y_edges.extend([y1, y2, None])
                    z_edges.extend([z1, z2, None])

        # Create a scatter plot for nodes with blue color
        scatter = go.Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes, mode='markers', marker=dict(size=8, color='blue'))

        # Create a scatter plot for highlighted nodes with red color
        scatter_highlight = go.Scatter3d(x=x_highlight, y=y_highlight, z=z_highlight, mode='markers', marker=dict(size=8, color='red'))

        # Create a line plot for edges with white color
        lines = go.Scatter3d(x=x_edges, y=y_edges, z=z_edges, mode='lines', line=dict(color='white'))

        # Create a line plot for highlighted edges with yellow color
        lines_highlight = go.Scatter3d(x=x_highlight_edges, y=y_highlight_edges, z=z_highlight_edges, mode='lines', line=dict(color='yellow'))

        # Create the 3D plot
        fig = go.Figure(data=[scatter, lines, scatter_highlight, lines_highlight])

        # Customize the layout
        fig.update_layout(
            scene=dict(
                zaxis=dict(
                    showbackground=False,
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    title=''
                ),
                yaxis=dict(
                    showbackground=False,
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    title=''
                ),
                xaxis=dict(
                    showbackground=False,
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    title=''
                ),
                bgcolor='black'
            ),
            paper_bgcolor='black',
            plot_bgcolor='black',
            scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        )

        fig.show()

def path_to_string(space, path):
    route = ""
    for i, name in enumerate(path):
        node = space.get_node(name)
        node_type = node.get_type()
        if (i == 0):
            direction = space.get_intermediate_direction(name, path[1])
            route += f"First, face {direction} towards {space.get_node(path[1]).print()}.\n"
        if (i == len(path)-1):
            route += "You have arrived at your destination!"

        if (node_type == NodeType.ROOM):
            route += f"Enter {node.print()} and find {space.get_node(path[i+1]).print()}.\n"
            route += f"\tIt should be {space.node_distance(path[i-1], path[i+1])} {space.units} to your {space.get_clock_direction(path[i-1], path[i+1])}"
        elif (node_type == NodeType.STAIRS):
            if (space.get_node(path[i-1]).get_type != NodeType.STAIRS):
                flights = 0
                direction = "up" if (space.node_y_distance(name, path[i+1]) > 0) else "down"
                next_node = space.get_node(path[i+1+flights])
                while (next_node.get_type() == NodeType.STAIRS):
                    flights += 1
                    next_node = path[i+1+flights]
                if flights > 0:
                    route += f"Head {direction} {flights} flights of stairs to {next_node.print()}"
                else: 
                    route += f"Go to the "

def blacklistedSpaceCopy(mainSpace, blacklist):
    newSpace = copy.deepcopy(mainSpace)
    nodeList = newSpace.get_nodes()
    removeList = []
    for nodeName, node in nodeList.items():
        if node.get_type() in blacklist:
            removeList.append(nodeName)
    for remNode in removeList:
        newSpace.remove_node(remNode)
    print(newSpace.get_nodes().keys())
    return newSpace