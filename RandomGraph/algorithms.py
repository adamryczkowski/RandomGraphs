from .directional_tagged_graph import DirectionalTaggedGraph
from .ifaces import IGraph, ProcessEdge, ProcessVertex

def make_dfs_tree(graph:IGraph, start:int, reachable_ancestor_edge_style:str="dashed")->DirectionalTaggedGraph:
    out = DirectionalTaggedGraph()

    def add_node(node: int, discovered: dict[int, int], processed: dict[int, int]) -> bool:
        out.add_node(node)
        return False

    def add_vertex(parent: int, child: int, discovered: dict[int, int], processed: dict[int, int])->bool:
        if child in discovered:
            out.push_connection(parent, child, tag="dotted")
        else:
            out.push_connection(parent, child, tag="solid")
        return False

    graph.dfs(start, process_vertex_early=add_node, process_edge=add_vertex)
    return out
