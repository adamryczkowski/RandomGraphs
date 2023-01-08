from __future__ import annotations

import graphviz
import numpy as np
from collections import defaultdict

from .ifaces import IGraph

from overrides import overrides


class UndirectionalGraph(IGraph):
    graph: dict[int, set[int]]

    def __init__(self, n: int, link_density_factor: float = 0.5):
        self.graph = defaultdict(set)
        self._random_directed_graph(n, link_density_factor)

    def _random_directed_graph(self, N: int, link_density_factor: float):
        if N == 0:
            return
        p = min(1., link_density_factor / 2)
        p = [p, 1 - p]
        for i in range(N):
            for j in range(i, N):
                if i != j and np.random.choice([True, False], p=p):
                    self.push_connection(i, j)

    @overrides
    def __len__(self):
        return len(self.graph)

    @overrides
    def __str__(self):
        ans = f"{len(self.graph)}\n"
        conn = [f"{i} {j}" for i in range(len(self.graph)) for j in self.graph[i]]
        ans += f"{len(conn)}\n"
        ans += "\n".join(conn)
        return ans

    @overrides
    def push_connection(self, i: int, j: int):
        self.graph[i].add(j)
        self.graph[j].add(i)

    @overrides
    def plot(self):
        out = graphviz.Digraph()
        for i in range(len(self)):
            out.node(str(i))
        for i in range(len(self.graph)):
            for j in self.graph[i]:
                if i < j:
                    out.edge(str(i), str(j), arrowhead="none")
        return out

    @overrides
    def __contains__(self, i: int):
        return i in self.graph

    @overrides
    def children(self, i: int) -> set[int]:
        return self.graph[i]

    @overrides
    def get_nodes(self) -> set[int]:
        return set(self.graph.keys())

    @overrides
    def remove_unconnected_nodes(self):
        nodes = self.get_nodes()
        for node in nodes:
            if len(self.children(node)) == 0:
                self.remove_node(node)
        return self

    @overrides
    def remove_node(self, i: int):
        for j in self.children(i):
            self.graph[j].remove(i)
        del self.graph[i]

    @overrides
    def remove_connection(self, i: int, j: int):
        self.graph[i].remove(j)
        self.graph[j].remove(i)

    @overrides
    def __eq__(self, other: UndirectionalGraph) -> bool:
        return self.graph == other.graph

    @overrides
    def add_node(self, i: int):
        self.graph[i] = set()