from collections import deque
from typing import Dict
from teasingApp.models_custom.teasingApp.Graph_access_file import graph_access_file

class Graph_AL:
    def __init__(self, source: str) -> None:
        if source is not None:
            all = graph_access_file.get_all_lines(source)
            self.elements = graph_access_file.get_elements(all, 0)
            self.is_weighted = graph_access_file.get_bool(all, 1)
            self.adjancy_list = graph_access_file.get_adjancy_list(all, 2, self.is_weighted)
            for indexes in self.elements:
                if indexes not in self.adjancy_list:
                    self.adjancy_list[indexes] = []

    def BFS(self, start_node, target_node):
        if self.is_weighted:
            raise ValueError("Cannot apply BFS: the graph is weighted")
        visited = set()  # Ensemble pour stocker les nœuds visités
        queue = deque([(start_node, [])])  # File pour maintenir les nœuds à visiter avec leur chemin parcouru
        while queue:
            current_node, path = queue.popleft()
            visited.add(current_node)
            if current_node == target_node:
                return path  # Retourne le chemin si le nœud cible est atteint
            neighbors = self.adjancy_list[current_node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))  # Ajoute le voisin à la file avec le chemin parcouru

        return None  # Aucun chemin trouvé


    def dijkstra(self, start: str) -> Dict[str, int]:
        distance = {node: float('inf') for node in self.adjancy_list}
        distance[start] = 0
        visited = set()
        all_paths = {node: [[], 0] for node in self.adjancy_list}  # Utiliser une liste au lieu d'un tuple
        while visited != set(self.adjancy_list):
            current_node = min(distance, key=distance.get)
            visited.add(current_node)
            for neighbor, weight in self.adjancy_list[current_node]:
                if neighbor not in visited:
                    all_paths[neighbor][0].append(current_node)
                    new_distance = distance[current_node] + int(weight)
                    if new_distance < distance.get(neighbor, float('inf')):
                        distance[neighbor] = new_distance
                        all_paths[neighbor][1] = new_distance
            del distance[current_node]
        return all_paths
    
    def get_shortest_path(self ,start:str ,end:str):
        return self.dijkstra(start)[end]
