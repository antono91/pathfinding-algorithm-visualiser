import pygame
from queue import PriorityQueue
from node import Node

class PathfindingVisualizer:
    ROWS = COLS = 50
    LIGHT_GRAY = (140, 140, 140)
    WHITE = (255, 255, 255)

    def __init__(self, width=800):
        pygame.init()
        self.width = width
        self.grid = self.create_grid()

        self.win = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption("Pathfinding Algorithm Visualizer")
        self.running = True

        self.start = None
        self.end = None

    def create_grid(self):
        grid = []
        node_width = self.width // self.ROWS
        for row in range(self.ROWS):
            grid.append([])
            for col in range(self.COLS):
                grid[row].append(Node(row, col, node_width))
                if row in (0, self.ROWS-1) or col in (0, self.COLS-1):
                    grid[row][col].set_wall()
        return grid

    def draw_grid(self):
        space = self.width // self.ROWS
        for row in range(self.ROWS):
            pygame.draw.line(self.win, self.LIGHT_GRAY,
                             (0, space * row), (self.width, space * row))
        for col in range(self.COLS):
            pygame.draw.line(self.win, self.LIGHT_GRAY,
                             (space * col, 0), (space * col, self.width))

    def draw(self):
        self.win.fill(self.WHITE)
        for row in self.grid:
            for node in row:
                node.draw(self.win)
        self.draw_grid()
        pygame.display.update()

# ----------------------- Algorithm Functions -----------------------

    def __h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current):
        while current in came_from:
            current = came_from[current]
            current.set_path()
            self.draw()


    def run_algorithm(self):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))
        came_from = {}
        g_score = {node: float("inf") for row in self.grid for node in row}
        g_score[self.start] = 0
        f_score = {node: float("inf") for row in self.grid for node in row}
        f_score[self.start] = self.__h(self.start.get_pos(), self.end.get_pos())

        open_set_hash = {self.start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end:
                self.reconstruct_path(came_from, current)
                return True
            
            for neighbor in current.get_neighbors(self.grid):
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.__h(neighbor.get_pos(), self.end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.set_open()
            self.draw()

            if current != self.start:
                current.set_closed()
        return False   
        



# ----------------------------------------------------------------

    def hande_mouse_inputs(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons:
            x, y = pygame.mouse.get_pos()
            row, col = y // (self.width //
                             self.ROWS), x // (self.width // self.COLS)
            node = self.grid[row][col]
            if mouse_buttons[0]:
                if not self.start and node != self.end:
                    self.start = node
                    node.set_start()
                elif not self.end and node != self.start:
                    self.end = node
                    node.set_end()
                elif node != self.start and node != self.end:
                    node.set_wall()
            elif mouse_buttons[2]:
                node.reset()
                if node == self.start:
                    self.start = None
                elif node == self.end:
                    self.end = None

    def loop(self):
        while self.running:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        self.run_algorithm()
                    
                    if event.key == pygame.K_c:
                        self.start = None
                        self.end = None
                        self.grid = self.create_grid()

                self.hande_mouse_inputs()

        pygame.quit()