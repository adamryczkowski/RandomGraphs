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

def my_agenci3()->AgenciGraph:
    graph = AgenciGraph.CreateFromString("""12
10
1 10
6 100
5 5
4 35
8 65
12 10
9 15
2 15
10 0
3 35
15
1 5
2 6
3 5
4 10
5 1
7 5
7 14
8 1
8 11
11 3
11 12
11 5
12 1
12 7
12 8""")
    return graph

def my_agenci4()->AgenciGraph:
    graph = AgenciGraph.CreateFromString("""13
10
1 0
2 0
11 35
9 15
10 25
7 30
12 45
14 10
15 20
13 25
24
1 12
1 7
2 14
2 7
4 10
4 7
5 1
5 6
6 2
6 5
6 8
7 3
7 11
8 1
9 7
10 12
10 15
11 2
11 8
12 15
14 6
15 11
15 12
15 6""")
    return graph


if __name__ == '__main__':
    # graph = DirectionalGraph(8)
    graph = my_agenci4()
    # graph = AgenciGraph(15, link_density_factor=0.2)
    print(graph)
    d = graph.plot()
    d.view(filename="graph.dot", quiet_view=True, quiet=True)

    ugraph = graph.plot(False)
    ugraph.view(filename="ugraph.dot", quiet_view=True, quiet=True)
