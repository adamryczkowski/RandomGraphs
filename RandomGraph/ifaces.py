from abc import abstractmethod
from typing import Optional, Callable, Protocol


class ProcessVertex(Protocol):
    def __call__(self, node: int, discovered: dict[int, int], processed: dict[int, int]) -> bool:
        """
        :param node: Visited node as int
        :param discovered: dictionary of all already discovered nodes, with value being the timestamp of the discovery
        :param processed: dictionary of all preocessed nodes, with value being the timestamp of the processing
        :return: true if process should be terminated, false otherwise.
        """


class ProcessEdge(Protocol):
    def __call__(self, parent: int, child: int, discovered: dict[int, int], processed: dict[int, int]) -> bool:
        """
        :param parent: ID of the parent node
        :param child: ID of the child node
        :param discovered: dictionary of all already discovered nodes, with value being the timestamp of the discovery
        :param processed: dictionary of all preocessed nodes, with value being the timestamp of the processing
        :return: true if process should be terminated, false otherwise.
        """


class IGraph:

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
    def plot(self):
        pass

    @abstractmethod
    def __contains__(self, i: int, j: int):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def children(self, i: int) -> set[int]:
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
            process_vertex_early: ProcessVertex = None,
            process_edge: ProcessEdge = None,
            process_vertex_late: ProcessVertex = None) -> None:
        pass
