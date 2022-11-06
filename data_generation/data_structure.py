from abc import ABC
import abc
from typing import Self


class Graph(ABC):

    @abc.AbstractMethod
    def add_left(self, left: Self) -> None:
        pass

    @abc.AbstractMethod    
    def add_right(self, left: Self) -> None:
        pass

    @abc.AbstractMethod
    def add_up(self, left: Self) -> None:
        pass

    @abc.AbstractMethod
    def add_down(self, left: Self) -> None:
        pass

class MazeNode(Graph):
    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
    



if __name__ == "__main__":
    pass