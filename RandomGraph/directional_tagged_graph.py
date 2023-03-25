from typing import Optional

import graphviz

from .directional_graph import DirectionalGraph
from .ifaces import IGraph


class DirectionalTaggedGraph(DirectionalGraph):
    tags: dict[tuple[int, int], str]

    def __init__(self):
        super().__init__()
        self.tags = {}

    # noinspection PyMethodOverriding
    def push_connection(self, i: int, j: int, tag: Optional[str] = None, cost: int = 1):
        assert cost == 1
        super().push_connection(i, j)
        if i < j:
            self.tags[(i, j)] = tag
        else:
            self.tags[(j, i)] = tag

    def get_tag(self, i: int, j: int) -> Optional[str]:
        if i < j:
            return self.tags.get((i, j), None)
        else:
            return self.tags.get((j, i), None)

    def plot(self, **kwargs):
        out = graphviz.Digraph()
        for node in self.get_nodes():
            out.node(str(node))
        for node in self.get_nodes():
            for child in self.get_children(node):
                if node in self.get_children(child):
                    if node < child:
                        out.edge(str(node), str(child), dir="both", arrowhead="normal", arrowtail="normal",
                                 style=self.get_tag(node, child))
                else:
                    out.edge(str(node), str(child), arrowhead="normal", arrowtail="none",
                             style=self.get_tag(node, child))
        return out

    def __eq__(self, other: IGraph):
        if not isinstance(other, DirectionalTaggedGraph):
            return False
        if self._graph != other._graph:
            return False
        if self.tags != other.tags:
            return False
