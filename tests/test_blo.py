# https://szkopul.edu.pl/problemset/problem/JkT6CwdepjCQnJ9c6CwxHolZ/site/?key=statement
from RandomGraph import UndirectionalGraph, find_articulation_points, make_dfs_trees


def read_data() -> UndirectionalGraph:
    n, m = map(int, input().split())
    graph = UndirectionalGraph()
    for _ in range(m):
        u, v = map(int, input().split())
        graph.push_connection(u, v)
    return graph

def GetExample(s:str) -> UndirectionalGraph:
    lines = s.splitlines()
    n, m = [int(el) for el in lines[0].split()]

    ans = UndirectionalGraph()
    print(ans)
    for i in range(n):
        ans.add_node(i+1)
        print(ans)

    for i in range(m):
        i, j = [int(el) for el in lines[i + 1].split()]
        ans.push_connection(i, j)

    return ans



def RandomGraph() -> UndirectionalGraph:
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
21
0 2
1 9
2 0
2 1
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

    connection_counts = {}

    all_meetings = len(graph) * (len(graph) - 1)

    for node in graph.get_nodes():
    # for node in articulation_points:
        if node in articulation_points:
            discovered = {node: 1}
            connection_count = 0

            for child in graph.get_children(node):
                if child not in discovered:
                    count = graph.dfs(child, discovered=discovered)
                    connection_count += (count * (count - 1))

            connection_counts[node] = all_meetings - connection_count
        else:
            connection_counts[node] = (len(graph) - 1) * 2

    return connection_counts


if __name__ == '__main__':
    s = """5 5
1 2
2 3
1 3
3 4
4 5"""
    graph = GetExample(s)
    graph.plot().view(filename="undirectional.dot", quiet_view=True, quiet=True)
    make_dfs_trees(graph).plot().view(filename="tree.dot", quiet_view=True, quiet=True)

    connection_counts = solve(graph)

    conn = [f"{connection_counts[key]}" for key in graph.get_nodes()]
    print("\n".join(conn))
