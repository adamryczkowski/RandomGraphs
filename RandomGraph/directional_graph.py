from __future__ import annotations

from collections import defaultdict

import graphviz
import numpy as np
from overrides import overrides

from .dense_graph import DenseGraph
from .ifaces import IDirectionalGraph, ProcessVertex, IGraph, ProcessEdge


class DirectionalGraph(IDirectionalGraph):
    _graph: dict[int, set[int]]  # for each node contains a list of children
    _reverse_graph: dict[int, set[int]]  # for each node contains a list of parents
    _node_weights: dict[int, int]  # weight for each node
    _edge_weights: dict[tuple[int, int], int]
    _edge_weights_are_symmetrical: bool

    @staticmethod
    def CreateFromString(s: str,
                         no_edge_weights: bool = True, no_node_weights: bool = True,
                         edge_weights_are_symmetrical: bool = True) -> DirectionalGraph:
        """ Ignores the weights """
        assert no_edge_weights
        assert no_node_weights
        assert edge_weights_are_symmetrical
        lines = s.splitlines()
        ans = DirectionalGraph()
        n = int(lines[0])
        for i in range(n):
            ans._graph[i] = set()
            ans._reverse_graph[i] = set()

        m = int(lines[n + 1])
        for i in range(m):
            i, j = [int(el) for el in lines[i + n + 2].split()]
            ans.push_connection(i, j)
        return ans

    @overrides
    def __eq__(self, other: IGraph):
        if not isinstance(other, DirectionalGraph):
            return False
        ans1 = self._graph == other._graph
        ans2 = self._node_weights == other._node_weights
        ans3 = self._edge_weights == other._edge_weights
        return ans1 and ans2 and ans3

    @staticmethod
    def CreateRandom(N: int, link_density_factor: float = 0.5) -> DirectionalGraph:

        ans = DirectionalGraph()

        if N == 0:
            return ans
        p = min(1., link_density_factor / 2)
        p = [p, 1 - p]
        for i in range(N):
            for j in range(N):
                if i != j and np.random.choice([True, False], p=p):
                    ans.push_connection(i, j)

        return ans

    def __init__(self, all_node_weights_equal_one: bool = True,
                 all_edge_weights_equal_one: bool = True, edge_weights_are_symmetrical: bool = True):
        self._graph = defaultdict(set)
        self._reverse_graph = defaultdict(set)
        if all_node_weights_equal_one:
            self._node_weights = defaultdict(lambda: 1)
        else:
            self._node_weights = {}

        if all_edge_weights_equal_one:
            self._edge_weights = defaultdict(lambda: 1)
        else:
            self._edge_weights = {}

        self._edge_weights_are_symmetrical = edge_weights_are_symmetrical

    @overrides
    def __len__(self):
        return len(self._node_weights)
        # return len(set(self._graph.keys()).union(self._reverse_graph.keys()))

    @property
    @overrides
    def all_node_weights_must_be_one(self) -> bool:
        if isinstance(self._node_weights, defaultdict):
            return True
        ans = all(weight == 1 for weight in self._node_weights.values())
        if ans:
            self._node_weights = defaultdict(lambda: 1)
        return ans

    @property
    @overrides
    def all_edge_weights_must_be_one(self) -> bool:
        if isinstance(self._edge_weights, defaultdict):
            return True
        ans = all(weight == 1 for weight in self._edge_weights.values())
        if ans:
            self._edge_weights = defaultdict(lambda: 1)
        return ans

    @property
    def reversed_graph(self) -> DirectionalGraph:
        ans = DirectionalGraph(all_node_weights_equal_one=True,
                               all_edge_weights_equal_one=True,
                               edge_weights_are_symmetrical=self._edge_weights_are_symmetrical)
        ans._graph = self._reverse_graph
        ans._reverse_graph = self._graph
        ans._node_weights = self._node_weights
        if self.all_node_weights_must_be_one:
            ans._edge_weights = defaultdict(lambda: 1)
        else:
            if self.all_edge_weights_must_be_one:
                ans._edge_weights = defaultdict(lambda: 1)
            else:
                ans._edge_weights = {(edge2, edge1) for (edge1, edge2), weight in self._node_weights.items()}
        return ans

    @overrides
    def get_children(self, i: int) -> set[int]:
        return self._graph[i]

    def parents(self, i: int) -> set[int]:
        return self._reverse_graph[i]

    @overrides
    def __str__(self):
        nodes = [f"{i}" for i in self._graph.keys()]
        assert self.all_node_weights_must_be_one
        if self.all_edge_weights_must_be_one:
            ans = f"{len(nodes)}\n"
            ans += "\n".join(nodes)

            conn = [f"{i} {j}" for i in range(len(self._graph)) for j in self._graph[i]]
            ans += f"\n{len(conn)}\n"
            ans += "\n".join(conn)
        else:
            ans = f"{len(nodes)}\n"
            ans += "\n".join(nodes)

            conn = [f"{i} {j} {self.get_connection_weight[(i, j)]}" for i in range(len(self._graph)) for j in self._graph[i]]
            ans += f"\n{len(conn)}\n"
            ans += "\n".join(conn)
        return ans

    def __contains__(self, i: int, j: int):
        return j in self._graph[i]

    def push_connection(self, i: int, j: int, tag: str = None, cost: int = 1):
        if self.all_node_weights_must_be_one:
            assert cost == 1
        assert tag is None
        self._graph[i].add(j)
        if j not in self._graph:
            self._graph[j] = set()

        self._reverse_graph[j].add(i)
        if i not in self._reverse_graph:
            self._reverse_graph[j] = set()

        if not self.all_edge_weights_must_be_one:
            if self._edge_weights_are_symmetrical:
                if i < j:
                    self._edge_weights[(i, j)] = cost
                else:
                    self._edge_weights[(j, i)] = cost
            else:
                self._edge_weights[(i, j)] = cost

    @overrides
    def get_connection_weight(self, i: int, j: int) -> int:
        assert i in self
        if self.all_edge_weights_must_be_one:
            return 1
        if self._edge_weights_are_symmetrical:
            if i < j:
                return self._edge_weights[(i, j)]
            else:
                return self._edge_weights[(j, i)]
        else:
            return self._edge_weights[(i, j)]

    @overrides
    def plot(self, show_stronly_connected: bool = True) -> graphviz.Digraph:
        out = graphviz.Digraph()

        if show_stronly_connected:
            cg = self.strongly_connected_components2()
        else:
            cg = None
        flag_cg = False

        for node in range(len(self)):
            flag_cg = False
            if show_stronly_connected:
                if node in cg.get_nodes():
                    if len(cg.get_children(node)) > 1:
                        flag_cg = True
            node_label = f"{node}" if self.all_node_weights_must_be_one else f"{node} ({self.get_node_weight(node)})"
            if flag_cg:
                out.node(str(node), label=node_label, style="filled", color="gray")
            else:
                out.node(str(node), label=node_label)

        for node in self.get_nodes():
            for child in self.get_children(node):
                if self.all_edge_weights_must_be_one:
                    edge_label = None
                else:
                    edge_label = f"{self.get_connection_weight(node, child)}"
                if show_stronly_connected and child in cg.get_children(node):
                    if node in self.get_children(child):
                        if node < child:
                            continue
                    out.edge(str(node), str(child), dir="both", arrowhead="none", arrowtail="none", label=edge_label)
                elif node in self.get_children(child):
                    if node < child:
                        out.edge(str(node), str(child), dir="both", arrowhead="normal", arrowtail="normal",
                                 label=edge_label)
                else:
                    out.edge(str(node), str(child), arrowhead="normal", arrowtail="none", label=edge_label)
        return out

    @overrides
    def get_nodes(self) -> set[int]:
        return set(self._graph.keys()).union(set(self._reverse_graph.keys()))

    def _dfs(self, i: int, visited: set = None) -> set[int]:
        if visited is None:
            visited = set()
        visited.add(i)
        for child in self.get_children(i):
            if child not in visited:
                self._dfs(child, visited)
        return visited

    def _dfs2(self, i: int) -> dict[int, int]:
        visited = {}
        self.dfs(start=i, discovered=visited)
        return visited

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

        parents = {}

        time = 0

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
                        finish = process_edge(parent=node, child=child)
                        if finish:
                            return True
                    finish = _dfs(child)
                    if finish:
                        return True
                else:
                    if process_edge:
                        finish = process_edge(parent=node, child=child)
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

    def _dfs_reversed(self, i: int, visited: set = None) -> set[int]:
        if visited is None:
            visited = set()
        visited.add(i)
        for j in self._reverse_graph[i]:
            if j not in visited:
                self._dfs_reversed(j, visited)
        return visited

    def _dfs_reversed2(self, i: int) -> dict[int, int]:
        visited = {}
        reversed = self.reversed_graph
        reversed.dfs(start=i, discovered=visited)
        return visited

    def strongly_connected_components(self) -> DenseGraph:
        # Kosaraju's algorithm
        ans = DenseGraph()
        all_visited = set()
        for i in self.get_nodes():
            if i in all_visited:
                continue

            visited1 = set(self._dfs2(i).keys())

            visited2 = set(self._dfs_reversed2(i).keys())

            visited2.intersection_update(visited1)
            all_visited.update(visited2)

            for j in visited2:
                for k in self._graph[i]:
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
            for j in self._graph[i]:
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
            for j in self._reverse_graph[i]:
                assign(j, root, ans)

        for i in reversed(visited_stack):
            assign(i, i, ans)

        return ans

    @overrides
    def remove_node(self, i: int):
        for j in self._graph[i]:
            if (i, j) in self._edge_weights:
                del self._edge_weights[(i, j)]
            if (j, i) in self._edge_weights:
                del self._edge_weights[(j, i)]
            self._reverse_graph[j].remove(i)
        for j in self._reverse_graph[i]:
            self._graph[j].remove(i)
        del self._graph[i]
        del self._reverse_graph[i]
        del self._node_weights[i]


    @overrides
    def get_node_weight(self, i: int) -> int:
        return self._node_weights[i]

    @overrides
    def remove_connection(self, i: int, j: int):
        if (i, j) in self._edge_weights:
            del self._edge_weights[(i, j)]
        if (j, i) in self._edge_weights:
            del self._edge_weights[(j, i)]
        self._graph[i].remove(j)
        self._reverse_graph[j].remove(i)

    @overrides
    def remove_unconnected_nodes(self):
        for i in list(self.get_nodes()):
            if not self.get_children(i):
                self.remove_node(i)

    @overrides
    def add_node(self, i: int, weight: int = 1):
        self._graph[i] = set()
        self._reverse_graph[i] = set()
        if self.all_node_weights_must_be_one:
            assert weight == 1
        else:
            self._node_weights[i] = weight

    def find_cut_nodes(self) -> set[int]:
        ans = set()
        for i in self.get_nodes():
            if len(self.get_children(i)) > 1:
                continue
            if len(self._reverse_graph[i]) > 1:
                continue
            ans.add(i)
        return ans
