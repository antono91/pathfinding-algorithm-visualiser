import pygame


class Node:
    LIGHT_GREEN = (144, 238, 144)
    RED = (255, 0, 0)
    DARK_GRAY = (192, 192, 192)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 69, 0)
    AQUA = (0, 255, 255)

    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.x = col * width
        self.y = row * width
        self.color = self.WHITE

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == self.DARK_GRAY

    def is_open(self):
        return self.color == self.LIGHT_GREEN

    def is_wall(self):
        return self.color == self.BLACK

    def is_path(self):
        return self.color == self.PURPLE

    def is_start(self):
        return self.color == self.ORANGE

    def is_end(self):
        return self.color == self.AQUA

    def reset(self):
        self.color = self.WHITE

    def set_closed(self):
        self.color = self.DARK_GRAY

    def set_open(self):
        self.color = self.YELLOW

    def set_wall(self):
        self.color = self.BLACK

    def set_path(self):
        self.color = self.PURPLE

    def set_start(self):
        self.color = self.ORANGE

    def set_end(self):
        self.color = self.AQUA

    def reset(self):
        self.color = self.WHITE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def get_neighbors(self, grid):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for dir in directions:
            new_row, new_col = self.row + dir[0], self.col + dir[1]
            if 0 < new_row < len(grid) and 0 < new_col < len(grid) and not grid[new_row][new_col].is_wall():
                neighbors.append(grid[new_row][new_col])
        return neighbors
