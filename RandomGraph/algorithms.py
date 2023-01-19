from .directional_tagged_graph import DirectionalTaggedGraph
from .ifaces import IGraph, ProcessEdge, ProcessVertex, IUndirectionalGraph, EdgeType
from collections import defaultdict


def make_dfs_tree(graph: IGraph, start: int, reachable_ancestor_edge_style: str = "dotted") -> DirectionalTaggedGraph:
    out = DirectionalTaggedGraph()
    discovered: dict[int, int] = {}

    def add_node(node: int) -> bool:
        out.add_node(node)
        return False

    def add_vertex(parent: int, child: int, edge_type: EdgeType) -> bool:
        nonlocal discovered
        if child in discovered:
            out.push_connection(parent, child, tag=reachable_ancestor_edge_style)
        else:
            out.push_connection(parent, child, tag="solid")
        return False

    graph.dfs(start, discovered=discovered, process_vertex_early=add_node, process_edge=add_vertex)
    return out


def make_dfs_trees(graph: IGraph, reachable_ancestor_edge_style: str = "dotted") -> DirectionalTaggedGraph:
    out = DirectionalTaggedGraph()
    discovered: dict[int, int] = {}

    def add_node(node: int) -> bool:
        out.add_node(node)
        return False

    def add_vertex(parent: int, child: int, edge_type: EdgeType) -> bool:
        nonlocal discovered
        if child in discovered:
            out.push_connection(parent, child, tag=reachable_ancestor_edge_style)
        else:
            out.push_connection(parent, child, tag="solid")
        return False

    for node in graph.get_nodes():
        if node not in discovered:
            graph.dfs(node, discovered=discovered, process_vertex_early=add_node, process_edge=add_vertex)

    return out


def find_articulation_points(graph: IUndirectionalGraph) -> set[int]:
    """Given an undirectional graph returns a set of articulation points, i.e. nodes that if removed would split the graph into two or more components.
    Implemented using Tarjan's algorithm, from Stefen Skiena, The Algorithm Design Manual, 2nd edition
    """
    reachable_ancestor = {}
    tree_out_degree: dict[int, int] = defaultdict(int)
    out = set()
    parents: dict[int, int] = {}
    discovered: dict[int, int] = {}

    def process_vertex_early(node: int) -> bool:
        reachable_ancestor[node] = node
        return False

    def process_edge(parent: int, child: int, edge_type: EdgeType) -> bool:
        if edge_type == EdgeType.TREE:
            tree_out_degree[parent] = tree_out_degree.get(parent, 0) + 1

        if edge_type == EdgeType.BACK and parents[parent] != child:
            # edge_type == EdgeType.BACK means that the child was already discovered, so it is actually a grand-grand-grand-...-parent, not a child
            # parents[parent] != child is to prevent handling multiple edges between the same two nodes
            if discovered[child] < discovered[reachable_ancestor[parent]]:
                # If the grand-grand-...-parent was visited earlier than the current reachable ancestor of the parent, then we must update the reachable ancestor,
                # so it points to the oldest node that can be reached from the parent
                reachable_ancestor[parent] = child

        return False

    def process_vertex_late(node: int) -> bool:
        if node not in parents: # test if node is root
            if tree_out_degree[node] > 1:
                out.add(node) # Root is an articulation point if it has more than one child
            return False

        is_parent_root = parents[node] not in parents # Test if node's parent is root

        if not is_parent_root:
            if reachable_ancestor[node] == parents[node]: # Does the node have another (necessarily direct) connection to the parent?
                out.add(parents[node]) # node's parent is an articulation point if reachable ancestor of node is node's parent
                # (if it was something different, then it could only be a back edge, and node's parent would be reachable from that node)
                return False

            if reachable_ancestor[node] == node: # Is node a bridge (i.e. no back edges to any of its ancestors)?
                out.add(parents[node]) # node's parent is an articulation point if reachable ancestor of node is node itself

                if tree_out_degree[node] > 0: # Is node a leaf?
                    out.add(node) # node is an articulation point if it is not a leaf and has no back edges
                    return False

        if discovered[reachable_ancestor[node]] < discovered[reachable_ancestor[parents[node]]]:
            # Under the normal dfs traversal discovered[reachable_ancestor[node]] > discovered[reachable_ancestor[parents[node]]].
            # However, the reachable ancestor of the parent is older than the reachable ancestor of the node (because of the back edge),
            # so we must update the reachable ancestor of the parent.
            # This way we propagate the oldest reachable ancestor all the way up the tree.
            reachable_ancestor[parents[node]] = reachable_ancestor[node]
        return False

    for node in graph.get_nodes():
        if node not in discovered:
            graph.dfs(node, parents=parents, discovered=discovered, process_vertex_early=process_vertex_early,
                      process_edge=process_edge,
                      process_vertex_late=process_vertex_late)
    return out
