# Standard Library
import random

# Third Party Library
import numpy as np


class Edge:
    def __init__(self, from_node, to_node, cost):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost


class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.nodes = set()
        self.adjacency_list = {}
        for edge in edges:
            self.nodes.update([edge.from_node, edge.to_node])
            if edge.from_node not in self.adjacency_list:
                self.adjacency_list[edge.from_node] = []
            self.adjacency_list[edge.from_node].append(edge)


class Ant:
    def __init__(self, graph, alpha, beta):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.path = []
        self.path_cost = 0.0

    def find_path(self, start_node, pheromones):
        current_node = start_node
        visited = set([current_node])
        self.path = [current_node]
        self.path_cost = 0.0

        while len(visited) < len(self.graph.nodes):
            next_node = self.choose_next_node(
                current_node, pheromones, visited
            )
            if next_node is None:
                break
            edge = next(
                edge
                for edge in self.graph.adjacency_list[current_node]
                if edge.to_node == next_node
            )
            self.path_cost += edge.cost
            self.path.append(next_node)
            visited.add(next_node)
            current_node = next_node

        # Return to start node
        return_edge = next(
            edge
            for edge in self.graph.adjacency_list[current_node]
            if edge.to_node == start_node
        )
        self.path_cost += return_edge.cost
        self.path.append(start_node)

    def choose_next_node(self, current_node, pheromones, visited):
        edges = [
            edge
            for edge in self.graph.adjacency_list.get(current_node, [])
            if edge.to_node not in visited
        ]

        if not edges:
            return None

        probabilities = []
        for edge in edges:
            pheromone = pheromones[(edge.from_node, edge.to_node)]
            heuristic = 1.0 / edge.cost
            probabilities.append(
                (pheromone**self.alpha) * (heuristic**self.beta)
            )

        sum_probabilities = sum(probabilities)
        probabilities = [prob / sum_probabilities for prob in probabilities]
        cumulative_probabilities = np.cumsum(probabilities)

        random_value = random.random()

        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if random_value <= cumulative_probability:
                return edges[i].to_node

        return edges[-1].to_node  # Fallback in case of rounding errors


def update_pheromones(pheromones, ants, evaporation_rate, Q):
    # Apply evaporation
    for key in pheromones:
        pheromones[key] *= 1 - evaporation_rate

    # Update pheromones based on ants' paths
    for ant in ants:
        for i in range(len(ant.path) - 1):
            from_node = ant.path[i]
            to_node = ant.path[i + 1]
            pheromones[(from_node, to_node)] += Q / ant.path_cost

    return pheromones


def main():
    edges = [
        Edge(0, 1, 2.0),
        Edge(0, 2, 2.0),
        Edge(1, 2, 1.0),
        Edge(1, 3, 1.0),
        Edge(2, 3, 2.0),
        Edge(3, 0, 1.0),
    ]
    graph = Graph(edges)
    alpha = 1.0
    beta = 2.0
    evaporation_rate = 0.5
    Q = 100.0
    num_ants = 10
    num_iterations = 100

    pheromones = {(edge.from_node, edge.to_node): 1.0 for edge in edges}

    best_ant = None

    for _ in range(num_iterations):
        ants = [Ant(graph, alpha, beta) for _ in range(num_ants)]
        for ant in ants:
            ant.find_path(0, pheromones)
        pheromones = update_pheromones(pheromones, ants, evaporation_rate, Q)

        current_best_ant = min(ants, key=lambda ant: ant.path_cost)
        if best_ant is None or current_best_ant.path_cost < best_ant.path_cost:
            best_ant = current_best_ant

    if best_ant:
        print(
            f"Best path: {' -> '.join(map(str, best_ant.path))} with cost: {best_ant.path_cost}"
        )
    else:
        print("No valid path found")


if __name__ == "__main__":
    main()
