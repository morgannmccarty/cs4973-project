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
    def generate_adj_matrix(self, distance: int) -> np.array:
        """ Generated a localized adjacency matrix for up to a distance of "distance" nodes away from self.
        """
        return None
    
    @abc.abstractmethod
    def to_represented_str(self) -> str:
        """ Create a representation string that is easy converted back to a node.
        """
        return ""

class Graph(abc.ABC):

    @abc.abstractmethod
    def optimal_path(self) -> typing.List[TNode]:
        return None

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
        if self.initialized:
            return
        else:
            x, y = 0, 0
            if self.left == None:
                if self.right == None:
                    if self.up == None:
                        if self.down == None:
                            return
                        else:
                            x, y = self.down.get_identifier()
                            y += 1
                    else:
                        x, y = self.up.get_identifier()
                        y -= 1
                else:
                    x, y = self.right.get_identifier()
                    x -= 1
            else:
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

    def __eq__(self, other):
        return isinstance(other, MazeNode) and self.pos == other.pos

    def __hash__(self) -> int:
        return hash(self.pos)

    def __repr__(self):
#         try:
#             return f"""\
# left: {str(self.left.get_identifier())}, up: {str(self.up.get_identifier())}
# self: {str(self.get_identifier())}
# down: {str(self.down.get_identifier())}, right: {str(self.right.get_identifier())}"""
#         except:
#             return str(self.get_identifier())
        return self.to_represented_str()

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
        self.shortest_path = None

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

    def optimal_path(self, *args):
        if len(self.members) <= 2:
            return self.members
        if self.shortest_path != None:
            return self.shortest_path
        node_s = random.choice(self.members)
        node_t = random.choice(self.members)
        while node_t == node_s:
            node_t = random.choice(self.members)
        if len(args) != 0:
            node_s = self.members[args[0]]
            node_t = self.members[args[1]]
        unvisited = set(self.members)
        distances = []
        for i in range(len(self.members)):
            if self.members[i] == node_s:
                distances.append(0)
            else:
                distances.append(float("inf"))
        
        path_not_found = True

        while path_not_found:
            uni_dis = sorted(list(distances))
            cn_index = -1
            min_num = 0
            while cn_index == -1:
                min_dis = uni_dis[min_num]
                mindices = [num for num, x in enumerate(distances) if x == min_dis]
                for mindex in mindices:
                    if self.members[mindex] in unvisited:
                        cn_index = mindex
                        break
                min_num += 1
            current_node = self.members[cn_index]

            if current_node == node_t:
                path_not_found = False
                break
            children = [current_node.left, current_node.right, current_node.up, current_node.down]
            for child in children:
                if child == None:
                    continue
                if child in unvisited:
                    child_index = self.members.index(child)
                    distances[child_index] = min(distances[child_index], distances[cn_index] + 1)
            unvisited.remove(current_node)
        
        path = [node_t]
        for _ in range(distances[self.members.index(node_t)]):
            current_node = path[0]
            children_nodes = [current_node.left, current_node.right, current_node.up, current_node.down]
            child_distance = [distances[self.members.index(x)] if x != None else float("inf") for x in children_nodes]
            next_node = children_nodes[np.argmin(child_distance)]
            path = [next_node] + path

        self.shortest_path = path
        return path

    @staticmethod
    def from_represented_str(str):
        def str_to_tuple(str):
            str = str.strip("()")
            try:
                return tuple(map(int, str.split(", ")))
            except:
                return (None, None)

        snodes = str.split("\n")
        snodes.pop()
        nodes = []
        taken_pos = set()

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
            if c_pos == (0, 0) and c_pos not in taken_pos:
                new_node = MazeNode(c_pos)
                nodes.append(new_node)
                taken_pos.add(c_pos)
                center_node = new_node
            else:
                center_node = [n for n in nodes if n.get_identifier() == c_pos][0]

            for i in range(len(out_poses)):
                if out_poses[i] != (None, None) and out_poses[i] not in taken_pos:
                    new_node = MazeNode()
                    dirs[i](center_node, new_node)
                    new_node.initialize()
                    nodes.append(new_node)
                    taken_pos.add(out_poses[i])
                    
        return Maze(nodes)   

    @staticmethod
    def generate_example(num_nodes):
        surrounded_nodes = set()
        nodes = []
        coords = []

        nodes.append(MazeNode((0, 0)))
        coords.append((0, 0))

        nn = 1
        while nn < num_nodes:
            node = nodes[nn - 1]
            while node in surrounded_nodes:
                node = random.choice(nodes)

            
            possible_adds = [MazeNode.add_left, MazeNode.add_right, MazeNode.add_up, MazeNode.add_down]
            existing_nodes = [node.left, node.right, node.up, node.down]
            exact_adds = [MazeNode(node.get_identifier() + (-1, 0)), MazeNode(node.get_identifier() + (1, 0)), MazeNode(node.get_identifier() + (0, 1)), MazeNode(node.get_identifier() + (0, -1))]

            for n in nodes:
                for i in range(len(possible_adds)):
                    if exact_adds[i] == n:
                        possible_adds[i](node, n)

            good_adds = [possible_adds[i] for i in range(len(possible_adds)) if existing_nodes[i] == None]


            if good_adds == []:
                surrounded_nodes.add(node)
            else:
                node_add = random.choice(good_adds)
                new_node = MazeNode()
                node_add(node, new_node)
                new_node.initialize()
                nodes.append(new_node)
                nn += 1
        
        return Maze(nodes)

    def path_description(self):
        self.opt_path = self.optimal_path()
        path_description_simple = []
        for step in self.opt_path:
            children = [step.left, step.right, step.up, step.down]
            dirs = ["left", "right", "up", "down"]
            path_description_simple += [dirs[children.index(step)]]
        print(path_description_simple)
        short = np.random.normal(loc=4, scale=1, size=(3, 100))
        short = [[round(x) for x in out] for out in short]
        print(short)

Node.register(MazeNode)
Graph.register(Maze)
            
if __name__ == "__main__":
    print("Running data_structure tests...")

    # Test 1: Make sure Graph is an abstraction of Maze
    try:
        assert isinstance(Maze([]), Graph)
    except:
        print("Maze is not a child of Graph.")
    # Test 2: Make sure Node is an abstraction of MazeNode
    try:
        assert isinstance(MazeNode([]), Node)
    except:
        print("MazeNode is not a child of Node.")
    nodes = [MazeNode((0, 0)), MazeNode()]
    # Test 3: Node initialization test from given pos
    try:
        assert nodes[0].initialized
    except:
        print("Node did not initialize from given position.")
    # Test 4: Node not initially initialized test
    try:
        assert not nodes[1].initialized
    except:
        print("Node initialized with being initialized")
    #Test 5: Node argument count test
    try:
        node_3 = MazeNode((0, 0), nodes[1])
    except:
        pass
    else:
        print("MazeNode initialized with too many arguments")
    
    nodes = nodes + [MazeNode(), MazeNode(), MazeNode()]
    nodes[0].add_left(nodes[1])
    nodes[0].add_right(nodes[2])
    nodes[0].add_up(nodes[3])
    nodes[0].add_down(nodes[4])

    for node in nodes:
        node.initialize()

    try:
        assert str(nodes[0]) == "S(0, 0)|L(-1, 0)|R(1, 0)|U(0, 1)|D(0, -1)"
        #OLD: "left: (-1, 0), up: (0, 1)\nself: (0, 0)\ndown: (0, -1), right: (1, 0)"
    except:
        print("Node string did not convert properly")

    repr_str = Maze.generate_example(20).to_represented_str()
    

    try:
        repr_str == (Maze.from_represented_str(repr_str)).to_represented_str()
    except:
        print("Outputted represented string did not match original represented string.")
    
    gen_maze = Maze.generate_example(10)

    repr_str_op = "S(0, 0)|L_|R_|U(0, 1)|D_\nS(0, 1)|L_|R(1, 1)|U_|D(0, 0)\nS(1, 1)|L(0, 1)|R_|U(1, 2)|D_\nS(1, 2)|L(0, 2)|R_|U_|D(1, 1)\nS(0, 2)|L(-1, 2)|R(1, 2)|U_|D_\nS(-1, 2)|L_|R(0, 2)|U_|D(-1, 1)\nS(-1, 1)|L(-2, 1)|R_|U(-1, 2)|D_\nS(-2, 1)|L(-3, 1)|R(-1, 1)|U_|D_\nS(-3, 1)|L(-4, 1)|R(-2, 1)|U_|D_\nS(-4, 1)|L_|R(-3, 1)|U_|D_"
    opt_path = "[S(0, 2)|L(-1, 2)|R(1, 2)|U_|D_, S(-1, 2)|L_|R(0, 2)|U_|D(-1, 1), S(-1, 1)|L(-2, 1)|R_|U(-1, 2)|D_, S(-2, 1)|L(-3, 1)|R(-1, 1)|U_|D_]"
    
    gen_maze.path_description()

    try:
        gen_maze = Maze.from_represented_str(repr_str_op)
        assert opt_path == str(gen_maze.optimal_path(4, 7))
    except:
        print("Optimal path determined not optimal path.")

    print("Finished data_structure tests.")