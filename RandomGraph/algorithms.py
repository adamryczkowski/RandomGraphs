from .directional_graph import DirectionalGraph
from .undirectional_graph import UndirectionalGraph
from .directional_tagged_graph import DirectionalTaggedGraph
from .ifaces import IGraph

def make_dfs_tree(graph:IGraph, start:int, reachable_ancestor_edge_style:str="dashed")->DirectionalTaggedGraph:
    graph.d