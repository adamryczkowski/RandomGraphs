import graphviz
from .directional_graph import DirectionalGraph
from typing import Any, Optional


class DirectionalTaggedGraph(DirectionalGraph):
    tags: dict[tuple[int, int], str]

    def __init__(self):
        super().__init__()
        self.tags = {}

    # noinspection PyMethodOverriding
    def push_connection(self, i: int, j: int, tag: str):
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
        for node in range(len(self)):
            out.node(str(node))
        for node in self.get_nodes():
            for child in self.children(node):
                if node in self.children(child):
                    if node < child:
                        out.edge(str(node), str(child), dir="both", arrowhead="normal", arrowtail="normal",
                                 style=self.get_tag(node, child))
                else:
                    out.edge(str(node), str(child), arrowhead="normal", arrowtail="none",
                             style=self.get_tag(node, child))
        return out
