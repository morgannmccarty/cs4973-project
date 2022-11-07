import abc
import typing
import numpy as np
import random

TNode = typing.TypeVar("TNode", bound = "Node")
TGraph = typing.TypeVar("TGraph", bound = "Graph")

class Node(abc.ABC):
    """ Abstract Node class in which to create methods that will be implemented in subclasses.
    """

    @abc.abstractmethod
    def add_left(self, left: TNode) -> None:
        """ Update the node to store a value for the Node to the left.
        """
        return

    @abc.abstractmethod   
    def add_right(self, left: TNode) -> None:
        """ Update the node to store a value for the Node to the right.
        """
        return

    @abc.abstractmethod
    def add_up(self, left: TNode) -> None:
        """ Update the node to store a value for the Node above.
        """
        return

    @abc.abstractmethod
    def add_down(self, left: TNode) -> None:
        """ Update the node to store a value for the Node to the below.
        """
        return

    @abc.abstractmethod
    def get_identifier(self) -> typing.Any:
        """ Get and return unique identifier for the graph node.
        """
        return None

    @abc.abstractmethod
    def generate_adj_matrix(self) -> np.array:
        return None
    
    @abc.abstractmethod
    def to_represented_str(self) -> str:
        return ""

class Graph(abc.ABC):
    @abc.abstractmethod
    def get_members(self) -> typing.List[TNode]:
        return None
    
    @abc.abstractmethod
    def add_member(self, member: TNode) -> None:
        return None

    @abc.abstractmethod
    def to_represented_str(self) -> str:
        return ""
    
    @abc.abstractstaticmethod
    def generate_example(num_nodes: int) -> TGraph:
        return None

    @abc.abstractstaticmethod
    def from_represented_str(str) -> TGraph:
        return None

@Node.register
class MazeNode():
    """ A node within the maze.

        Essentially a storage of connected nodes.
    """
    def __init__(self, *args):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.pos = (None, None)
        self.initialized = False
        if len(args) == 1:
            self.pos = args[0]
            self.initialized = True
        if len(args) > 1:
            raise Exception("Too many arguments passed to constructor.")
    
    def initialize(self):
        """ Initialize pos based on connected nodes.
        """
        try:
             assert self.left != None
        except:
            try: 
                assert self.right != None
            except:
                try:
                    assert self.up != None
                except:
                    try:
                        assert self.down != None
                    except:
                        return
                    else:
                        # if not self.down.initialized:
                        #     self.down.initialize()
                        x, y = self.down.get_identifier()
                        y += 1
                        self.pos = (x, y)
                else:
                    # if not self.up.initialized:
                    #     self.up.initialize()
                    x, y = self.up.get_identifier()
                    y -= 1
                    self.pos = (x, y)
            else:
                # if not self.right.initialized:
                #     self.right.initialize()
                x, y = self.right.get_identifier()
                x -= 1
                self.pos = (x, y)
        else:
            # if not self.left.initialized:
            #     self.left.initialize()
            x, y = self.left.get_identifier()
            x += 1
            self.pos = (x, y)
        self.initialized = True
    
    def to_represented_str(self):
        return f"""S{self.get_identifier()}\
|L{"_" if self.left == None else self.left.get_identifier()}\
|R{"_" if self.right == None else self.right.get_identifier()}\
|U{"_" if self.up == None else self.up.get_identifier()}\
|D{"_" if self.down == None else self.down.get_identifier()}"""

    def __repr__(self):
        try:
            return f"""\
left: {str(self.left.get_identifier())}, up: {str(self.up.get_identifier())}
self: {str(self.get_identifier())}
down: {str(self.down.get_identifier())}, right: {str(self.right.get_identifier())}"""
        except:
            return str(self.get_identifier())

    def add_left(self, left):
        self.left = left
        if left.right != self:
            left.add_right(self)

    def add_right(self, right):
        self.right = right
        if right.left != self:
            right.add_left(self)
       
    def add_up(self, up):
        self.up = up
        if up.down != self:
            up.add_down(self)
        
    def add_down(self, down):
        self.down = down
        if down.up != self:
            down.add_up(self)
        
    def get_identifier(self):
        return self.pos

    def generate_adj_mat(self):
        return np.zeroes(15)

@Graph.register
class Maze():
    def __init__(self, members):
        self.members = members

    def get_members(self):
        return self.members
    
    def add_member(self, member):
        self.members.append(member)

    def to_represented_str(self):
        repr = ""
        for node in self.members:
            repr = "".join([repr, node.to_represented_str(), "\n"])
        return repr
    
    def __repr__(self):
        return self.to_represented_str()

    @staticmethod
    def from_represented_str(str):
        def str_to_tuple(str):
            str = str.strip("()")
            try:
                return tuple(map(int, str.split(", ")))
            except:
                return (None, None)

        snodes = str.split("\n")
        nodes = []

        for snode in snodes:
            snode_components = snode.split("|")
            center = snode_components[0]
            left = snode_components[1]
            right = snode_components[2]
            up = snode_components[3]
            down = snode_components[4]

            c_pos = str_to_tuple(center[1:])
            out_poses = [str_to_tuple(left[1:]), str_to_tuple(right[1:]), str_to_tuple(up[1:]), str_to_tuple(down[1:])]
            dirs = [MazeNode.add_left, MazeNode.add_right, MazeNode.add_up, MazeNode.add_down]
            center_node = None
            if c_pos == (0, 0):
                new_node = MazeNode(c_pos)
                nodes.append(new_node)
                center_node = new_node
            else:
                center_node = [n for n in nodes if n.get_identifier() == c_pos][0]

            for i in range(len(out_poses)):
                if out_poses[i] != (None, None):
                    new_node = MazeNode()
                    dirs[i](center_node, new_node)
                    new_node.initialize()
                    nodes.append(new_node)
                    
        return Maze(nodes)

    @staticmethod
    def generate_example(num_nodes):
        surrounded_nodes = set()
        nodes = []

        nodes.append(MazeNode((0, 0)))

        nn = 1
        while nn < num_nodes:
            node = nodes[nn - 1]
            while node.get_identifier in surrounded_nodes:
                node = random.choice(nodes)
            x, y = node.get_identifier()
            possible_nodes = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if all(n in surrounded_nodes for n in possible_nodes):
                surrounded_nodes.add(node.get_identifier())
            else:
                dirs = ["left", "right", "up", "down"]
                good_nodes = [dirs[possible_nodes.index(n)] for n in possible_nodes if n not in surrounded_nodes]
                dir = random.choice(good_nodes)
                new_node = MazeNode()
                if dir == "left":
                    node.add_left(new_node)
                if dir == "right":
                    node.add_right(new_node)
                if dir == "up":
                    node.add_up(new_node)
                if dir == "down":
                    node.add_down(new_node)
                new_node.initialize()
                nodes.append(new_node)
                nn += 1
        
        return Maze(nodes)

Node.register(MazeNode)
Graph.register(Maze)
            
if __name__ == "__main__":
    print("Running data_structure tests...")
    try:
        assert isinstance(Maze([]), Graph)
    except:
        print("Maze is not a child of Graph.")
    try:
        assert isinstance(MazeNode([]), Node)
    except:
        print("MazeNode is not a child of Node.")

    node_1 = MazeNode((0, 0))
    try:
        assert node_1.initialized
    except:
        print("Node did not initialize from given position.")
    node_2 = MazeNode()
    node_2.add_left(node_1)
    try:
        node_3 = MazeNode((0, 0), node_1)
    except:
        pass
    else:
        print("MazeNode initialized with too many arguments")
    
    node_3 = MazeNode()
    node_4 = MazeNode()
    node_5 = MazeNode()

    node_1.add_left(node_2)
    node_1.add_right(node_3)
    node_1.add_up(node_4)
    node_1.add_down(node_5)
    node_2.initialize()
    node_3.initialize()
    node_4.initialize()
    node_5.initialize()

    try:
        assert str(node_1) == "left: (1, 0), up: (0, 1)\nself: (0, 0)\ndown: (0, -1), right: (1, 0)"
    except:
        print("Node string did not convert properly")

    repr_str = "S(0, 0)|L(-1, 0)|R_|U_|D_\nS(-1, 0)|L_|R(0, 0)|U_|D(-1, -1)\nS(-1, -1)|L_|R_|U(-1, 0)|D(-1, -2)\nS(-1, -2)|L_|R(0, -2)|U(-1, -1)|D_\nS(0, -2)|L(-1, -2)|R_|U_|D(0, -3)\nS(0, -3)|L(-1, -3)|R_|U(0, -2)|D_\nS(-1, -3)|L_|R(0, -3)|U_|D_\nS(0, -3)|L(-1, -3)|R(1, -3)|U_|D_\nS(1, -3)|L(0, -3)|R_|U(1, -2)|D_\nS(1, -2)|L_|R_|U_|D(1, -3)"

    maze = Maze.from_represented_str(repr_str)

    try:
        repr_str == (Maze.from_represented_str(repr_str)).to_represented_str()
    except:
        print("Outputted represented string did not match original represented string.")

    print("Finished data_structure tests.")