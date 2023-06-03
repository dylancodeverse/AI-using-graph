from collections import deque

from teasingApp.models_custom.teasingApp.Graph_AL import Graph_AL
from teasingApp.models_custom.teasingApp.Teasing import Teasing

# from Graph_AL import Graph_AL
# from Teasing import Teasing


class Graph_Teasing(Graph_AL):
    def __init__(self, taquin: Teasing, source=None) -> None:
        super().__init__(source)
        self.adjancy_list = {taquin: []}
        derivates = taquin.get_tuples_derivate()
        for derivate in derivates:
            self.adjancy_list[taquin].append(derivate)

    def __str__(self):
        result = ""
        for taquin, moves in self.adjancy_list.items():
            result += f"Teasing:\n{taquin}\n"
            for move in moves:
                result += f"Move: {move[1]} --> Teasing:\n{move[0]}\n"
            result += "\n"
        return result
    
    def solve_taquin(self, goal):
        first_key = list(self.adjancy_list.keys())[0]
        return self.shortest_path(first_key, goal)
    
    def shortest_path(self, start, goal):
        visited = set()
        queue = deque([(start, [])])
        while queue:
            current_taquin, path = queue.popleft()
            if current_taquin.matrix == goal.matrix:
                return path
            if tuple(map(tuple, current_taquin.matrix)) in visited:
                continue
            visited.add(tuple(map(tuple, current_taquin.matrix)))
            for neighbor, move in self.adjancy_list[current_taquin]:
                if neighbor not in self.adjancy_list:
                    derivates = neighbor.get_tuples_derivate()
                    self.adjancy_list[neighbor] = derivates
                queue.append((neighbor,path+[move]))
        return None

