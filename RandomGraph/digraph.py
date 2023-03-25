from typing import Optional

import graphviz
from overrides import overrides

from . import IGraph, ProcessVertex, ProcessEdge
from .ifaces import IDirectionalGraph

from .directional_graph import DirectionalGraph


class DiGraph(IDirectionalGraph):
    _edges: dict[tuple[int, int], int]  # Connection -> its cost
    _left_edges: dict[int, set[int]]  # What are the edges that start from the left edge key?
    _right_edges: dict[int, set[int]]  # What are the edges that start from the right edge key?

    def __init__(self):
        self._edges = {}
        self._left_edges = {}
        self._right_edges = {}

    def vertex_side(self, i: int) -> int:
        """
        Returns the side of vertex i.
        :param i: vertex id
        :return: side of the vertex; 0 - left side, 1 - right side
        """
        if i in self._left_edges:
            return 0
        elif i in self._right_edges:
            return 1
        else:
            raise ValueError(f"Vertex {i} does not exist")

    @overrides
    def push_connection(self, i: int, j: int, tag: Optional[str] = None, cost: int = 1):
        """
        :return Pushes a connection between from vertex i to j.
        """
        assert tag is None

        if i in self._left_edges:
            right_set = self._left_edges[i]
        else:
            right_set = set()
            self._left_edges[i] = right_set

        if j in self._right_edges:
            left_set = self._right_edges[j]
        else:
            left_set = set()
            self._right_edges[j] = left_set

        right_set.add(j)
        left_set.add(i)

        self._edges[(i, j)] = cost

    @overrides
    def get_connection_weight(self, i: int, j: int) -> int:
        return self._edges[(i, j)]

    @overrides
    def remove_node(self, i: int):
        """
        Removes a node from the graph, along all the connections to and from it.
        :param i:
        :return:
        """
        side = self.vertex_side(i)

        if side == 0:
            edge_set = self._left_edges[i]
        else:
            edge_set = self._right_edges[i]

        for j in edge_set:
            if (i, j) in self._edges:
                self.remove_connection(i, j)
            if (j, i) in self._edges:
                self.remove_connection(j, i)

    @overrides
    def remove_connection(self, i: int, j: int):
        """
        :return: Removes connection from i to j. "i" does not need to be on left side of the graph.
        """
        del self._edges[(i, j)]

        if j in self._left_edges and i in self._right_edges:
            i, j = j, i
        # from now on, i is on the left, and j is on the right

        self._left_edges[i].remove(j)
        self._right_edges[j].remove(i)

    @overrides
    def remove_unconnected_nodes(self):
        items_to_delete = set()
        for key, items in self._left_edges.items():
            if len(items) == 0:
                items_to_delete.add(key)

        for key, items in self._right_edges.items():
            if len(items) > 0 and key in items_to_delete:
                items_to_delete.remove(key)

        for key in items_to_delete:
            del self._right_edges[key]
            del self._left_edges[key]

    @overrides
    def get_children(self, i: int) -> set[int]:
        """
        :return: Returns all the children of vertex i.
        """
        if i in self._left_edges:
            return self._left_edges[i]
        else:
            return set()

    @overrides
    def __len__(self):
        return len(self._left_edges) + len(self._right_edges)

    @overrides
    def __contains__(self, i: int, j: int):
        return (i, j) in self._edges

    @overrides
    def __str__(self):
        ans = [f"{i} {j} {k}" for (i, j), k in self._edges.items()]
        return "\n".join(ans)

    @overrides
    def get_nodes(self) -> set[int]:
        ans = {i for i in self._left_edges.keys()}
        ans.update({i for i in self._right_edges.keys()})
        return ans

    @overrides(check_signature=False)
    def add_node(self, i: int, side: int):
        assert side in (0, 1)
        assert i not in self._left_edges and i not in self._right_edges

        if side == 0:
            self._left_edges[i] = set()
        else:
            self._right_edges[i] = set()

    def make_directional_graph(self)-> DirectionalGraph:
        """
        :return: Returns a directional graph and discards all the weights.
        """
        ans = DirectionalGraph()
        for (i, j) in self._edges.keys():
            ans.push_connection(i, j)
        return ans
    @overrides
    def dfs(self, start: int, discovered: dict[int, int] = None, processed: dict[int, int] = None,
            parents: dict[int, int] = None, process_vertex_early: ProcessVertex = None,
            process_edge: ProcessEdge = None, process_vertex_late: ProcessVertex = None) -> int:
        raise NotImplementedError

    @overrides
    def __eq__(self, other: IGraph):
        raise NotImplementedError

    @overrides
    def plot(self) -> graphviz.Digraph:
        raise NotImplementedError
