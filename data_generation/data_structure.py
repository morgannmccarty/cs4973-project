import abc
import typing
import numpy as np

TNode = typing.TypeVar("TNode", bound = "Node")

class Node(abc.ABC):
    """ Abstract Node class in which to create methods that will be implemented in subclasses.
    """

    @abc.abstractmethod
    def add_left(self, left: TNode) -> None:
        """ Update the node to store a value for the Node to the left.
        """
        pass

    @abc.abstractmethod   
    def add_right(self, left: TNode) -> None:
        """ Update the node to store a value for the Node to the right.
        """
        pass

    @abc.abstractmethod
    def add_up(self, left: TNode) -> None:
        """ Update the node to store a value for the Node above.
        """
        pass

    @abc.abstractmethod
    def add_down(self, left: TNode) -> None:
        """ Update the node to store a value for the Node to the below.
        """
        pass

    @abc.abstractmethod
    def get_identifier(self) -> typing.Any:
        """ Get and return unique identifier for the graph node.
        """
        pass

    @abc.abstractmethod
    def generate_adj_matrix(self) -> np.array:
        pass

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
                        x, y = self.down.get_identifier()
                        y += 1
                        self.pos = (x, y)
                else:
                    x, y = self.up.get_identifier()
                    y -= 1
                    self.pos = (x, y)
            else:
                x, y = self.right.get_identifier()
                x -= 1
                self.pos = (x, y)
        else:
            x, y = self.left.get_identifier()
            x += 1
            self.pos = (x, y)
        self.initialized = True
    
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

if __name__ == "__main__":
    print("Running data_structure tests...")
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
    print("Finished data_structure tests.")