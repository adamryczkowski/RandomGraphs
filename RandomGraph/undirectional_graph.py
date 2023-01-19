from __future__ import annotations

import graphviz
import numpy as np
from collections import defaultdict

from .ifaces import IUndirectionalGraph, ProcessEdge, ProcessVertex, IGraph, EdgeType

from overrides import overrides


class UndirectionalGraph(IUndirectionalGraph):
    _graph: dict[int, set[int]]

    @staticmethod
    def CreateRandom(N: int, link_density_factor: float = 0.5) -> UndirectionalGraph:
        out = UndirectionalGraph()
        out._random_directed_graph(N, link_density_factor)
        return out

    @staticmethod
    def CreateFromString(s: str) -> UndirectionalGraph:
        lines = s.splitlines()
        n = int(lines[0])
        ans = UndirectionalGraph()
        for i in range(n):
            i = int(lines[i + 1])
            ans._graph[i] = set()

        m = int(lines[n + 1])
        for i in range(m):
            i, j = [int(el) for el in lines[i + n + 2].split()]
            ans.push_connection(i, j)

        return ans

    def __init__(self):
        self._graph = defaultdict(set)

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
        return len(self._graph)

    @overrides
    def __str__(self):
        nodes = [f"{i}" for i in self._graph.keys()]
        ans = f"{len(nodes)}\n"
        if len(nodes) > 0:
            ans += "\n".join(nodes)
            ans += "\n"

        conn = [f"{i} {j}" for i in self._graph.keys() for j in self._graph[i] if i < j]
        ans += f"{len(conn)}\n"
        if len(conn) > 0:
            ans += "\n".join(conn)
        return ans

    @overrides
    def dfs(self, start: int, discovered: dict[int, int] = None,
            processed: dict[int, int] = None,
            parents: dict[int, int] = None,
            process_vertex_early: ProcessVertex = None, process_edge: ProcessEdge = None,
            process_vertex_late: ProcessVertex = None) -> int:

        if discovered is None:
            discovered = {}
        if processed is None:
            processed = {}
        if parents is None:
            parents = {}

        time = 0

        def edge_classification(parent: int, child: int) -> EdgeType:
            if parents.get(child) == parent:
                return EdgeType.TREE

            if child in discovered and child not in processed:
                return EdgeType.BACK

            if child in processed and discovered[parent] < discovered[child]:
                return EdgeType.FORWARD

            if child in processed and discovered[parent] > discovered[child]:
                return EdgeType.CROSS

            raise ValueError("Unknown edge type")

        def _dfs(node: int) -> bool:
            nonlocal time, discovered, processed, parents
            time += 1
            discovered[node] = time

            if process_vertex_early:
                finish = process_vertex_early(node)

                if finish:
                    return True

            children = list(self.get_children(node))
            children.sort()

            for child in children:
                if child not in discovered:
                    parents[child] = node
                    if process_edge:
                        finish = process_edge(parent=node, child=child,
                                              edge_type=edge_classification(parent=node, child=child))
                        if finish:
                            return True
                    finish = _dfs(child)
                    if finish:
                        return True
                elif not child in processed and parents.get(node) != child:
                    if process_edge:
                        finish = process_edge(parent=node, child=child,
                                              edge_type=edge_classification(parent=node, child=child))
                        if finish:
                            return True
            if process_vertex_late:
                finish = process_vertex_late(node)
                if finish:
                    return True
            time += 1
            processed[node] = time
            return False

        _dfs(start)
        return time // 2

    @overrides
    def push_connection(self, i: int, j: int):
        self._graph[i].add(j)
        self._graph[j].add(i)

    @overrides
    def plot(self) -> graphviz.Digraph:
        out = graphviz.Digraph()
        for i in self.get_nodes():
            out.node(str(i))
        for i in self.get_nodes():
            for j in self._graph[i]:
                if i < j:
                    out.edge(str(i), str(j), arrowhead="none")
        return out

    @overrides
    def __contains__(self, i: int):
        return i in self._graph

    @overrides
    def get_children(self, i: int) -> set[int]:
        return self._graph[i]

    @overrides
    def get_nodes(self) -> set[int]:
        return set(self._graph.keys())

    @overrides
    def remove_unconnected_nodes(self):
        nodes = self.get_nodes()
        for node in nodes:
            if len(self.get_children(node)) == 0:
                self.remove_node(node)
        return self

    @overrides
    def remove_node(self, i: int):
        for j in self.get_children(i):
            self._graph[j].remove(i)
        del self._graph[i]

    @overrides
    def remove_connection(self, i: int, j: int):
        self._graph[i].remove(j)
        self._graph[j].remove(i)

    @overrides
    def __eq__(self, other: IGraph) -> bool:
        if not isinstance(other, UndirectionalGraph):
            return False
        return self._graph == other._graph

    @overrides
    def add_node(self, i: int):
        self._graph[i] = set()
