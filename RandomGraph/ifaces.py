from abc import abstractmethod


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