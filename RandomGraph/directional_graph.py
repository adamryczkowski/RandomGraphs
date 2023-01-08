from __future__ import annotations

from collections import defaultdict

import graphviz
import numpy as np
from overrides import overrides

from .dense_graph import DenseGraph
from .ifaces import IGraph


class DirectionalGraph(IGraph):
    graph: dict[int, set[int]]
    reverse_graph: dict[int, set[int]]

    @staticmethod
    def CreateFromString(s: str) -> DirectionalGraph:
        lines = s.splitlines()
        n = int(lines[0])
        m = int(lines[1])
        ans = DirectionalGraph(0)
        for i in range(m):
            i, j = map(int, lines[i + 2].split())
            ans.push_connection(i, j)
        return ans

    def __init__(self, n: int, link_density_factor: float = 0.5):
        self.graph = defaultdict(set)
        self.reverse_graph = defaultdict(set)
        self._random_directed_graph(n, link_density_factor)

    def _random_directed_graph(self, N: int, link_density_factor: float):
        if N == 0:
            return
        p = min(1., link_density_factor / 2)
        p = [p, 1 - p]
        for i in range(N):
            for j in range(N):
                if i != j and np.random.choice([True, False], p=p):
                    self.push_connection(i, j)

    @overrides
    def __len__(self):
        return len(self.graph)

    @overrides
    def children(self, i: int) -> set[int]:
        return self.graph[i]

    @overrides
    def __str__(self):
        ans = f"{len(self.graph)}\n"
        conn = [f"{i} {j}" for i in range(len(self.graph)) for j in self.graph[i]]
        ans += f"{len(conn)}\n"
        ans += "\n".join(conn)
        return ans

    def __contains__(self, i: int, j: int):
        return j in self.graph[i]

    def push_connection(self, i: int, j: int):
        self.graph[i].add(j)
        self.reverse_graph[j].add(i)

    def plot(self):
        out = graphviz.Digraph()
        for node in range(len(self)):
            out.node(str(node))
        for node in self.get_nodes():
            for child in self.children(node):
                if node in self.children(child):
                    if node < child:
                        out.edge(str(node), str(child), dir="both", arrowhead="normal", arrowtail="normal")
                else:
                    out.edge(str(node), str(child), arrowhead="normal", arrowtail="none")
        return out

    @overrides
    def get_nodes(self) -> set[int]:
        return set(self.graph.keys()).union(set(self.reverse_graph.keys()))

    def _dfs(self, i: int, visited: set = None) -> set[int]:
        if visited is None:
            visited = set()
        visited.add(i)
        for child in self.children(i):
            if child not in visited:
                self._dfs(child, visited)
        return visited

    def _dfs_reversed(self, i: int, visited: set = None) -> set[int]:
        if visited is None:
            visited = set()
        visited.add(i)
        for j in self.reverse_graph[i]:
            if j not in visited:
                self._dfs_reversed(j, visited)
        return visited

    def strongly_connected_components(self) -> DenseGraph:
        # Kosaraju's algorithm
        ans = DenseGraph()
        all_visited = set()
        for i in self.get_nodes():
            if i in all_visited:
                continue

            visited1 = set()
            self._dfs(i, visited1)

            visited2 = set()
            self._dfs_reversed(i, visited2)

            visited2.intersection_update(visited1)
            all_visited.update(visited2)

            for j in visited2:
                for k in self.graph[i]:
                    if k in visited2:
                        ans.push_connection(j, k)
                else:
                    ans.add_node(j)

        return ans

    def strongly_connected_components2(self) -> DenseGraph:
        # Kosaraju's algorithm
        ans = DenseGraph()
        all_visited = set()
        visited_stack = []

        def visit(i: int):
            if i in all_visited:
                return
            all_visited.add(i)
            for j in self.graph[i]:
                visit(j)
            visited_stack.append(i)

        for i in self.get_nodes():
            if i in all_visited:
                continue
            visit(i)

        def assign(i: int, root: int, ans: DenseGraph):
            if i in ans:
                return
            ans.push_connection(i, root)
            for j in self.reverse_graph[i]:
                assign(j, root, ans)

        for i in reversed(visited_stack):
            assign(i, i, ans)

        return ans

    @overrides
    def remove_node(self, i: int):
        for j in self.graph[i]:
            self.reverse_graph[j].remove(i)
        for j in self.reverse_graph[i]:
            self.graph[j].remove(i)
        del self.graph[i]
        del self.reverse_graph[i]

    @overrides
    def remove_connection(self, i: int, j: int):
        self.graph[i].remove(j)
        self.reverse_graph[j].remove(i)

    @overrides
    def remove_unconnected_nodes(self):
        for i in list(self.get_nodes()):
            if not self.children(i):
                self.remove_node(i)

    @overrides
    def add_node(self, i: int):
        self.graph[i] = set()
        self.reverse_graph[i] = set()