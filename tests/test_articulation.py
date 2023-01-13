from RandomGraph import make_dfs_tree, UndirectionalGraph


def RandomGraph()->UndirectionalGraph:
    out = UndirectionalGraph.CreateRandom(10, 0.5)
    return out

def test():
    graph = RandomGraph()
    d = graph.plot()
    d.view(filename="undirectional.dot", quiet_view=True, quiet=True)
    print(graph)
    tree = make_dfs_tree(graph, 0)
    d = tree.plot()
    d.view(filename="tree.dot", quiet_view=True, quiet=True)
    print(tree)


if __name__ == '__main__':
    test()
