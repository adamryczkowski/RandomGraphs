# https://szkopul.edu.pl/problemset/problem/JkT6CwdepjCQnJ9c6CwxHolZ/site/?key=statement
from RandomGraph import UndirectionalGraph, find_articulation_points, make_dfs_trees
def read_data()->UndirectionalGraph:
    n, m = map(int, input().split())
    graph = UndirectionalGraph()
    for _ in range(m):
        u, v = map(int, input().split())
        graph.push_connection(u, v)
    return graph

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

def solve(graph: UndirectionalGraph):
    articulation_points = find_articulation_points(graph)


if __name__ == '__main__':
    graph = RandomGraph()
    graph.plot().view(filename="undirectional.dot", quiet_view=True, quiet=True)
    make_dfs_trees(graph).plot().view(filename="tree.dot", quiet_view=True, quiet=True)

    print(solve(graph))
