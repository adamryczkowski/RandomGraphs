from RandomGraph import DirectionalGraph



def test1():
    graph = DirectionalGraph(15, link_density_factor=0.4)
#     graph = DirectionalGraph.CreateFromString("""7
# 7
# 0 3
# 1 3
# 1 4
# 2 1
# 3 6
# 4 3
# 5 4""")
#     print(graph)

    sgraph1 = graph.strongly_connected_components()
    sgraph2 = graph.strongly_connected_components2()

    g = graph.plot()
    g.view(filename="sg", quiet_view=True, quiet=True)

    g1 = sgraph1.plot()
    g1.view(filename="sg1", quiet_view=True, quiet=True)

    g2 = sgraph2.plot()
    g2.view(filename="sg2", quiet_view=True, quiet=True)

    assert sgraph1 == sgraph2

if __name__ == '__main__':
    test1()
    print('OK')