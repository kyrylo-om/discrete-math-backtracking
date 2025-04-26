import networkx as nx
import matplotlib.pyplot as plt
import os
import random
import json


class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        self.steps = 0

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
    
    def render(self, color_map):
        os.makedirs("steps", exist_ok=True)

        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(self.graph, seed=42)

        colors = []
        for node in self.graph.nodes():
            c = color_map.get(node, 0)
            if c == 0:
                colors.append("lightgray")
            else:
                cmap = plt.cm.get_cmap('tab10')
                colors.append(cmap(c % 10))

        nx.draw(self.graph, pos, with_labels=True, node_color=colors, node_size=500, font_weight='bold')
        plt.savefig(f"steps/step_{self.steps:03d}.png")
        plt.close()

    def color(self, k):
        def is_safe(node, color):
            for neighbor in self.graph.neighbors(node):
                if color_map.get(neighbor) == color:
                    return False
            return True
        
        def backtrack(index):
            if index == len(nodes):
                self.steps += 1
                self.render(color_map)
                return True

            node = nodes[index]
            for color in range(1, k + 1):
                if is_safe(node, color):
                    color_map[node] = color
                    self.steps += 1
                    self.render(color_map)
                    #steps.append(color_map.copy())

                    if backtrack(index + 1):
                        return True

                    color_map[node] = 0  # backtrack
                    self.steps += 1
                    self.render(color_map)
                    #steps.append(color_map.copy())

            return False

        color_map = {node: 0 for node in self.graph.nodes()}
        nodes = list(self.graph.nodes())
        if backtrack(0):
            return color_map
        else:
            return None


G = Graph()
G.generate(10, 0.3)

coloring = G.color(4)

if coloring:
    print("Успішне розфарбування:", coloring)
else:
    print(f"Неможливо розфарбувати граф.")
print("Кроки:", G.steps)