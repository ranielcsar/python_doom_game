from collections import deque
from typing import Dict, Tuple
from game_types import GameType

TupleType = Tuple[int, int]
DictTupleType = Dict[TupleType, TupleType]


class PathFinding:
    def __init__(self, game: GameType):
        self.game = game
        self.map = game.map.mini_map
        self.ways = (
            [-1, 0],
            [0, -1],
            [1, 0],
            [0, 1],
            [-1, -1],
            [1, -1],
            [1, 1],
            [-1, 1],
        )
        self.graph: DictTupleType = {}
        self.get_graph()
        self.visited: DictTupleType = {}

    def get_path(self, start: TupleType, goal: TupleType) -> TupleType:
        self.visited = self.breadth_first_search(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]

        return path[-1]

    def breadth_first_search(
        self,
        start: TupleType,
        goal: TupleType,
        graph: DictTupleType,
    ):
        queue = deque([start])
        visited = {start: None}

        while queue:
            current_node = queue.popleft()

            if current_node == goal:
                break
            next_nodes = graph[current_node]

            for next_node in next_nodes:
                if (
                    next_node not in visited
                    and next_node not in self.game.object_handler.npc_positions
                ):
                    queue.append(next_node)
                    visited[next_node] = current_node
        return visited

    def get_next_nodes(self, x, y):
        return [
            (x + delta_x, y + delta_y)
            for delta_x, delta_y in self.ways
            if (x + delta_x, y + delta_y) not in self.game.map.world_map
        ]

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get(
                        (x, y), []
                    ) + self.get_next_nodes(x, y)
