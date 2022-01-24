import pygame as pg
from grid import Grid
from typing import Union
import threading
from algrorithms import DFS
import sys


# Constants for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# TO DO
# Make perfomance improvements
# Separate Render and Logic
# Check threading and multiprocessing
# Choose what is better


class Sandbox:
    def __init__(self, width: int=500, height: int=500, scale: int=20):
        pg.init()

        self.grid = Grid(scale, width, height)

        self.width = width
        self.height = height
        self.scale = scale

        self.size = (self.width, self.height)
        self.screen = pg.display.set_mode(self.size)

        self.walls = []
        self.targets = []

        self.path = []

    def main(self):
        while True:
            action = self.handle_input()

            self.screen.fill(BLACK)

            if action:
                self.activate_block(action)
            
            if self.walls or self.targets:
                self.draw_active_blocks()

            self.draw_board()

            pg.display.flip()

    def draw_board(self) -> None:
        

        # Draw grid layout
        for x in range(0, self.width, self.width // self.scale):
            for y in range(0, self.height, self.height // self.scale):
                # Draw columns
                pg.draw.line(self.screen, WHITE, (x, 0), (x, self.height))
                # Draw rows
                pg.draw.line(self.screen, WHITE, (0, y), (self.width, y))

    def activate_block(self, mouse_action) -> None:
        x, y = list(mouse_action.values())[0]

        x_grid, y_grid = self.grid.translate_screen_position(x, y)
        if mouse_action.get('wall'):
            if (x_grid, y_grid) in self.targets:
                self.targets.remove((x_grid, y_grid))

            if self.grid.matrix[y_grid][x_grid]:
                self.grid.matrix[y_grid][x_grid] = 0
                self.walls.append((x_grid, y_grid))

            else:
                self.grid.matrix[y_grid][x_grid] = 1
                self.walls.remove((x_grid, y_grid))

        elif mouse_action.get('target'):
            if (x_grid, y_grid) in self.walls:
                self.walls.remove((x_grid, y_grid))
            if (x_grid, y_grid) in self.targets:
                self.targets.remove((x_grid, y_grid))
            elif len(self.targets) != 2:
                self.targets.append((x_grid, y_grid))

        
    def draw_active_blocks(self):
        for wall in self.walls:
            x, y = wall
            rect_cords = self.grid.rectangle_cords(x, y, self.width, self.height)
            pg.draw.rect(self.screen, WHITE, rect_cords)

        for target in self.targets:
            x, y = target
            rect_cords = self.grid.rectangle_cords(x, y, self.width, self.height)
            pg.draw.rect(self.screen, RED, rect_cords)

        for path in self.path:
            x, y = path
            rect_cords = self.grid.rectangle_cords(x, y, self.width, self.height)
            pg.draw.rect(self.screen, GREEN, rect_cords)

    def handle_input(self) -> Union[dict, None]:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return {'wall': pg.mouse.get_pos()}
                if event.button == 3:
                    return {'target': pg.mouse.get_pos()}

            if event.type == pg.KEYDOWN and len(self.targets) == 2:
                if event.key == pg.K_SPACE:
                    if not self.path:
                        algorithm = DFS(self.grid.matrix)
                        start_point, end_point = self.targets
                        thread = threading.Thread(
                            target=algorithm.find_path,
                            args=(start_point, end_point, self.path),
                            daemon=True
                        )
                        thread.start()
                    else:
                        self.path = []
                    
sandbox = Sandbox()
sandbox.main()
