import networkx as nx
import matplotlib.pyplot as plt
import os
import random
import json


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def generate(self, num_nodes=5, connectedness=0.2):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(num_nodes))

        for i in range(1, num_nodes):
            self.graph.add_edge(i, random.randrange(i))

        extra_edges = int((num_nodes*(num_nodes-1)/2)*connectedness)

        possible_edges = [
            (i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)
            if not self.graph.has_edge(i, j)
        ]
        self.graph.add_edges_from(random.sample(possible_edges, min(extra_edges, len(possible_edges))))

    def save(self):
        with open("graph_data.js", "w") as file:
            nodes_data = [{"id": node, "label": str(node)} for node in self.graph.nodes()]
            edges_data = [{"from": u, "to": v} for u, v in self.graph.edges()]
            graph_data = {"nodes": nodes_data, "edges": edges_data}
            file.write("const graph = ")
            json.dump(graph_data, file, indent=4)

    def render(self):
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=16)
        plt.title("Граф")
        plt.show()

    def k_coloring(self, k):
        def can_color(node, color):
            for neighbor in self.graph.neighbors(node):
                if node_groups.get(neighbor) == color:
                    return False
            return True

        def update_history():
            steps.append(node_groups.copy())

        def step(index):
            if index == len(nodes):
                return True

            node = nodes[index]

            for color in range(1, k + 1):
                if can_color(node, color):
                    node_groups[node] = color
                    update_history()

                    if step(index + 1):
                        return True
                    else:
                        node_groups[node] = 0
                        update_history()

            return False

        node_groups = {node: 0 for node in self.graph.nodes()}
        steps = []
        nodes = list(self.graph.nodes())
        update_history()
        if step(0):
            self.save()
            with open("graph_data.js", "a") as file:
                file.write("\nconst history = ")
                json.dump(steps, file, indent=4)
            return node_groups
        else:
            return None


G = Graph()
G.generate(15, 0.2)

coloring = G.k_coloring(4)

if coloring:
    print("Успішне розфарбування:", coloring)
else:
    print(f"Неможливо розфарбувати граф.")