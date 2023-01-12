from __future__ import annotations
import numpy as np
import graphviz
from .directional_graph import DirectionalGraph


class AgenciGraph(DirectionalGraph):
    agents: dict[int, int]

    @staticmethod
    def CreateFromString(s: str, shift_by_one:bool = True) -> AgenciGraph:
        lines = s.splitlines()
        n_nodes = int(lines[0])
        n_agents = int(lines[1])

        agents = {}

        for i in range(n_agents):
            agent, cost = map(int, lines[i + 2].split())
            agents[agent] = cost

        ans = AgenciGraph(0)

        n_connections = int(lines[n_agents + 2])
        for i in range(n_connections):
            i, j = map(int, lines[i + n_agents + 3].split())
            if shift_by_one:
                i -= 1
                j -= 1
            ans.push_connection(i, j)

        for i, cost in agents.items():
            if shift_by_one:
                ans.add_agent(i - 1, cost)
            else:
                ans.add_agent(i, cost)

        return ans

    def __init__(self, N: int, link_density_factor: float = 0.5, agent_ratio: float = 0.7,
                 agent_dist_param: float = 10):
        super().__init__(N, link_density_factor)
        self.agents = {i: 5 * int(np.random.exponential(agent_dist_param)) for i in
                       np.random.choice(N, size=int(N * agent_ratio), replace=False)}

    def add_agent(self, node: int, cost: int):
        self.agents[node] = cost
        if node not in self.get_nodes:
            self.add_node(node)

    def __str__(self):
        ans = f"{len(self.graph)}\n" \
              f"{len(self.agents)}\n"
        for agent, cost in self.agents.items():
            ans += f"{agent + 1} {cost}\n"

        conn = []
        for parent, children in self.graph.items():
            for child in children:
                conn.append(f"{parent + 1} {child + 1}")

        ans += f"{len(conn)}\n"
        ans += "\n".join(conn)
        return ans

    def plot(self, show_stronly_connected: bool = True):
        out = graphviz.Digraph()

        if show_stronly_connected:
            cg = self.strongly_connected_components()
        else:
            cg = None

        flag_cg = False
        for node in self.get_nodes():
            flag_cg = False
            if show_stronly_connected:
                if node in cg.get_nodes():
                    if len(cg.children(node)) > 1:
                        flag_cg = True

            if node in self.agents:
                if flag_cg:
                    out.node(str(node), label=f"{node + 1} ({self.agents[node]})", style="filled", color="gray")
                else:
                    out.node(str(node), label=f"{node + 1} ({self.agents[node]})")
            else:
                if flag_cg:
                    out.node(str(node), label=f"{node + 1}", style="filled", color="gray")
                else:
                    out.node(str(node), label=f"{node + 1}")

        for node in self.get_nodes():
            for child in self.children(node):
                if show_stronly_connected and child in cg.children(node):
                    if node in self.children(child):
                        if node < child:
                            continue
                    out.edge(str(node), str(child), dir="both", arrowhead="none", arrowtail="none")
                elif node in self.children(child):
                    if node < child:
                        out.edge(str(node), str(child), dir="both", arrowhead="normal", arrowtail="normal")
                else:
                    out.edge(str(node), str(child), arrowhead="normal", arrowtail="none")
        return out
