from RandomGraph import UndirectionalGraph
from RandomGraph import DirectionalGraph
from RandomGraph import AgenciGraph

def my_graph()->DirectionalGraph:
    graph = DirectionalGraph.CreateFromString("""8
    13
    0 2
    0 5
    0 6
    0 7
    1 2
    2 7
    3 2
    3 6
    4 3
    4 7
    6 3
    6 5
    7 1""")
    return graph


def my_agenci()->AgenciGraph:
    graph = AgenciGraph.CreateFromString("""20
14
19 10
1 10
10 0
16 45
7 75
18 5
11 45
4 85
8 0
2 90
17 35
12 40
3 10
6 10
39
0 12
0 14
1 3
1 12
2 6
3 5
3 16
4 0
4 1
4 8
5 6
5 8
6 9
6 15
6 18
7 9
7 15
8 18
9 1
9 4
10 5
12 7
13 1
13 3
13 18
14 5
15 10
16 4
16 7
16 8
16 10
17 0
17 3
18 0
18 1
18 14
18 19
19 3
19 8""", shift_by_one=False)
    return graph

def my_agenci2()->AgenciGraph:
    graph = AgenciGraph.CreateFromString("""5
7
9 70
2 40
1 70
6 0
4 65
8 10
7 115
4
1 10
2 1
4 3
4 6""")
    return graph

if __name__ == '__main__':
    # graph = DirectionalGraph(8)
    # graph = my_agenci2()
    graph = AgenciGraph(10, link_density_factor=0.3)
    print(graph)
    d = graph.plot()
    d.view(filename="graph", quiet_view=True, quiet=True)

    ugraph = graph.plot(False)
    ugraph.view(filename="ugraph", quiet_view=True, quiet=True)
