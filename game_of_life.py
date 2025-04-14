import pygame
import copy


class GameOfLife:

    '''
    The grid will have 50x50 cells
    each cell will be a square of 16*16 pixels
    '''
    def __init__(self):
        self.grid = []
        self.width = 800
        self.height = 800

        self.screen = None
        self.clock = None
        self.running = False
        self.state = "setup"
    
    def make_grid(self):
        self.grid = []
        for i in range(100):
            row = []
            for j in range(100):
                row.append(0)
            self.grid.append(row)
    
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
    
    def handle_events_setup(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    i = x // 16
                    j = y // 16
                    self.grid[i][j] = 1
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is held
                    x, y = pygame.mouse.get_pos()
                    i = x // 16
                    j = y // 16
                    self.grid[i][j] = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.state = "simulation"
        return True
    
    def handle_events_simulation(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw_grid(self):
        self.screen.fill((255, 255, 255))

        for i in range(50):
            for j in range(50):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (i*16, j*16, 16, 16))

        #draw grid lines

        for i in  range(50):
            pygame.draw.line(self.screen, (0,0,255), (0, i*16), (800, i*16))
            pygame.draw.line(self.screen, (0,0,255), (i*16, 0), (i*16, 800))

        pygame.display.flip()

    def update_grid(self):
        # Apply the rules of the game of life to the grid
        # The rules are:
        # 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # 2. Any live cell with two or three live neighbours lives on to the next generation.
        # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        if self.state == "simulation":
            newGrid = copy.deepcopy(self.grid)
            for i in range(50):
                for j in range(50):
                    count = self.getNeighbourCount(i, j)
                    if self.grid[i][j] == 1:
                        if count < 2 or count > 3:
                            newGrid[i][j] = 0  # Dies
                        else:
                            newGrid[i][j] = 1  # Lives
                    else:
                        if count == 3:
                            newGrid[i][j] = 1  # Reproduces
            self.grid = newGrid


    def getNeighbourCount(self, i, j):
        adj = [[1,0], [0,1], [-1,0], [0,-1], [1,1], [-1,1], [-1,-1], [1,-1]]
        alive = 0
        for k in range(8):
            p, q  = i + adj[k][0], j + adj[k][1]

            if p <50 and p>=0 and q<50 and q>=0:
                if self.grid[p][q] == 1:
                    alive = alive+1
        return alive

    def run(self):
        self.init_pygame()
        self.make_grid()

        running = True
        while running:
            if self.state == "setup":
                running = self.handle_events_setup()
                self.update_grid()
                self.draw_grid()
                self.clock.tick(60)
            elif self.state == "simulation":
                running = self.handle_events_simulation()
                self.update_grid()
                self.draw_grid()
                self.clock.tick(10)

__all__ = ['GameOfLife']