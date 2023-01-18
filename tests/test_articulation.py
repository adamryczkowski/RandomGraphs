from RandomGraph import make_dfs_trees, UndirectionalGraph, find_articulation_points

from plotly import graph_objects as go


def RandomGraph()->UndirectionalGraph:
    # out = UndirectionalGraph.CreateRandom(10, 0.5)
    out = UndirectionalGraph.CreateFromString("""10
0
2
1
9
3
4
5
6
7
8
20
0 2
1 9
2 0
2 3
3 2
4 9
4 5
5 9
5 4
5 6
5 7
6 5
6 7
7 5
7 6
8 9
9 8
9 1
9 4
9 5""")
    return out

def test():
    graph = RandomGraph()
    d = graph.plot()
    d.view(filename="undirectional.dot", quiet_view=True, quiet=True)
    print(graph)
    tree = make_dfs_trees(graph)
    d = tree.plot()
    d.view(filename="tree.dot", quiet_view=True, quiet=True)
    print(tree)

    sets = find_articulation_points(graph)
    print(sets)


if __name__ == '__main__':
    test()
