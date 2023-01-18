from __future__ import annotations

import graphviz
from overrides import overrides

from .ifaces import IGraph, ProcessVertex, ProcessEdge


class DenseGraph(IGraph):
    """Graph where we assume every node is connected to every other node in a group of n nodes.
    """

    _groups: list[set[int]]
    _group_id: dict[int, int]  # maps node to group id

    def __init__(self):
        self._groups = []
        self._group_id = {}

    @overrides
    def dfs(self, start: int, discovered: dict[int, int] = None, processed: dict[int, int] = None,
            parents: dict[int, int] = None, process_vertex_early: ProcessVertex = None,
            process_edge: ProcessEdge = None, process_vertex_late: ProcessVertex = None) -> None:
        raise NotImplementedError()

    @overrides
    def __len__(self):
        return len(self._group_id)

    @overrides
    def __str__(self) -> str:
        ans = f"{len(self)}\n"
        for group in self._groups:
            ans += f"{len(group)} {' '.join(str(group))}"
        return ans

    @overrides
    def __repr__(self):
        return str(self)

    @overrides
    def push_connection(self, i: int, j: int):
        if i in self._group_id:
            group_id1 = self._group_id[i]
            group1 = self._groups[group_id1]

            if j in self._group_id:
                group_id2 = self._group_id[j]
                group2 = self._groups[group_id2]
                if group_id1 != group_id2:
                    group1.update(group2)
                    for node in group2:
                        self._group_id[node] = group_id1
                    del self._groups[group_id2]
            else:
                group1.add(j)
                self._group_id[j] = group_id1
        else:
            if j in self._group_id:
                group_id2 = self._group_id[j]
                group2 = self._groups[group_id2]
                group2.add(i)
                self._group_id[i] = group_id2
            else:
                group_id = len(self._groups)
                self._groups.append({i, j})
                self._group_id[i] = group_id
                self._group_id[j] = group_id

    @overrides
    def add_node(self, i: int):
        if i not in self._group_id:
            self._groups.append({i})
            self._group_id[i] = len(self._groups) - 1

    @overrides
    def remove_node(self, i: int):
        group_id = self._group_id[i]
        group = self._groups[group_id]
        group.remove(i)
        del self._group_id[i]
        if len(group) == 0:
            del self._groups[group_id]

    @overrides
    def remove_connection(self, i: int, j: int):
        raise NotImplementedError

    @overrides
    def remove_unconnected_nodes(self):
        for group_id, group in enumerate(self._groups):
            if len(group) == 0:
                del self._groups[group_id]

    @overrides
    def plot(self) -> graphviz.Digraph:
        out = graphviz.Digraph()
        for i in self.get_nodes():
            out.node(str(i))
        for group_id in set(self._group_id.values()):
            items = list(self._groups[group_id])
            items.sort()
            if len(items) == 0:
                continue
            anchor = items[0]
            for i in range(1, len(items)):
                element = items[i]
                if element != anchor:
                    out.edge(str(anchor), str(element), arrowhead="none")
        return out

    @overrides
    def __contains__(self, i: int):
        return i in self._group_id

    @overrides
    def children(self, i: int) -> set[int]:
        group_id = self._group_id[i]
        group = self._groups[group_id]
        return group - {i}

    @overrides
    def get_nodes(self) -> set[int]:
        return set(self._group_id.keys())

    @overrides
    def __eq__(self, other: IGraph):
        if not isinstance(other, DenseGraph):
            return False
        for item in self.get_nodes():
            if self.children(item) != other.children(item):
                return False
        return True
