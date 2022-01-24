from abc import ABC, abstractmethod
from typing import Union


class AlgorithmBase(ABC):

    def __init__(self, matrix):
        self.matrix = matrix

    # Use this function for all algorithms
    def find_path(self, start_point: tuple, end_point: tuple) -> Union[list, None]:
        pass

class DFS(AlgorithmBase):

    def __init__(self, matrix: list):
        super().__init__(matrix)

    def find_neighbours(self, node: tuple) -> list:
        x, y = node
        neighbours = list(filter(lambda x: 0 <= x[0] < len(self.matrix) and
                                 0 <= x[1] < len(self.matrix) and self.matrix[x[1]][x[0]] != 0,
                                 [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]))
        return neighbours  
    
    def find_path(self, start_point: tuple, end_point: tuple) -> list:
        visited = []
        stack = [start_point]
        path_map = {}

        while stack:
            for neighbour in self.find_neighbours(stack[0]):
                if not neighbour in visited:
                    stack.append(neighbour)

                    path_map.update(
                        {
                            neighbour: stack[0]
                        }
                    )

                    if neighbour == end_point:
                        curr = end_point
                        path = []
                        while curr != start_point:
                            path.append(curr)
                            curr = path_map[curr]
                        return path[1:]

            visited.append(stack.pop(0))
        return []
                            

        
