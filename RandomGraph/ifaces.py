from __future__ import annotations

from abc import abstractmethod, ABC
from enum import Enum
from typing import Callable, Protocol

import graphviz


class EdgeType(Enum):
    TREE = 0
    BACK = 1
    FORWARD = 2
    CROSS = 3


def fun(int, str) -> int:
    pass


f: Callable[[int, str], int] = fun


class ProcessVertex(Protocol):
    def __call__(self, node: int) -> bool:
        """
        :param node: Visited node as int

        User is advised to use discovered, processed and parents dictionaries passed to the dfs algorithm.
        :return: true if process should be terminated, false otherwise.
        """
        pass


class ProcessEdge(Protocol):
    def __call__(self, parent: int, child: int, edge_type: EdgeType) -> bool:
        """
        :param parent: ID of the parent node
        :param child: ID of the child node
        User is advised to use discovered, processed and parents dictionaries passed to the dfs algorithm.
        :return: true if process should be terminated, false otherwise.
        """


class IGraph(ABC):

    @abstractmethod
    def push_connection(self, i: int, j: int):
        pass

    @abstractmethod
    def remove_node(self, i: int):
        pass

    @abstractmethod
    def remove_connection(self, i: int, j: int):
        pass

    @abstractmethod
    def remove_unconnected_nodes(self):
        pass

    @abstractmethod
    def plot(self) -> graphviz.Digraph:
        pass

    @abstractmethod
    def __contains__(self, i: int, j: int):
        pass

    @abstractmethod
    def __len__(self):
        pass

    # @abstractmethod
    # def bfs(self, start: int, process_vertex: ProcessVertex, process_edge: Optional[ProcessEdge] = None):
    #     pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_children(self, i: int) -> set[int]:
        pass

    @abstractmethod
    def get_nodes(self) -> set[int]:
        pass

    @abstractmethod
    def add_node(self, i: int):
        pass

    @abstractmethod
    def dfs(self, start: int,
            discovered: dict[int, int] = None,
            processed: dict[int, int] = None,
            parents: dict[int, int] = None,
            process_vertex_early: ProcessVertex = None,
            process_edge: ProcessEdge = None,
            process_vertex_late: ProcessVertex = None) -> int:
        pass

    @abstractmethod
    def __eq__(self, other: IGraph):
        pass


class IUndirectionalGraph(IGraph):
    pass


class IDirectionalGraph(IGraph):
    pass
