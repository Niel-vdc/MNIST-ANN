import pygame
from pygame import mouse
import sys
import tensorflow as tf
import numpy as np
from Button import Button;

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
FPS = 30

font = pygame.font.Font('OpenSans-Regular.ttf', 14)
model = tf.keras.models.load_model('handwritten.model')

class Cell():
    def __init__(self, x, y, cell_width, colour=(255, 255, 255)):
        self.surface = pygame.Surface([cell_width, cell_width])
        self.colour = colour
        self.surface.fill(colour)
        self.x = x
        self.y = y
        self.cell_width = cell_width
        self.drawed = False
        self.light_drawed = False

    def draw(self):
        if (not self.drawed) & (not self.light_drawed):
            self.colour = (255, 255, 255)
        if (self.light_drawed) & (not self.drawed):
            self.colour = (100, 100, 100)
        if self.drawed:
            self.colour = (10, 10, 10)
            
        screen.blit(self.surface, (self.x, self.y))
        self.surface.fill(self.colour)




class Canvas:
    def __init__(self, x, y, nx, ny, cell_width):
        self.x = x  # top left
        self.y = y  # top left
        self.nx = nx    #n of cells in x
        self.ny = ny    #n of cells in y
        self.cell_width = cell_width
        self.cells = []
        self.output = []
        self.create()
        self.predictions = []
        self.clear_button = Button(150, self.y + self.ny * self.cell_width + 50, 100, 30, (200, 200, 200), (255, 255, 255), (150, 150, 150), self.clear, font, (0, 0, 0), "Clear", 2, (100, 100, 100))


    def create(self):
        for i in range(self.nx):
            for j in range(self.ny):
                cell = Cell(self.x + i * self.cell_width, self.y + j * self.cell_width, self.cell_width)
                self.cells.append(cell)

    def draw(self):
        for cell in self.cells:
            cell.draw()


        for i, pred in enumerate(sorted(self.predictions,key=lambda x: x[1], reverse=True)):
            text = font.render(f'{pred[0]}: {round(pred[1], 2)}%', True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH/2 + 50, i * 30 + 50))

        self.clear_button.draw(screen)

    def clear(self):
        self.cells = []
        self.output = []
        self.predictions = []
        self.create()



        

    def interact(self):
        mouse_pos = mouse.get_pos()
        self.clear_button.update()

        if mouse.get_pressed()[0]:
            self.output = []
            for cell in self.cells:
                if ((cell.x - 2 * cell.cell_width <= mouse_pos[0] <= cell.x - cell.cell_width) | (cell.x + 2 * cell.cell_width <= mouse_pos[0] <= cell.x + 3 *cell.cell_width )) & ((cell.y - 2 * cell.cell_width <= mouse_pos[1] <= cell.y - cell.cell_width) | (cell.y + 2*cell.cell_width <= mouse_pos[1] <= cell.y + 3* cell.cell_width)):
                    cell.light_drawed = True

                if (cell.x - cell.cell_width <= mouse_pos[0] <= cell.x + 2* cell.cell_width) & (cell.y - cell.cell_width<= mouse_pos[1] <= cell.y + 2 * cell.cell_width):
                    cell.drawed = True
                self.output.append(255 - cell.colour[0])

            print(self.output)
                
            
            predictions = model.predict(tf.keras.utils.normalize([canvas.output]))
            
            self.predictions = []
            for i, pred in enumerate(predictions[0]):
                self.predictions.append([i, pred])





screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


canvas = Canvas(0,50, 28, 28, 10)



while True:
    clock.tick(FPS)
    screen.fill((200, 200, 200))
    canvas.draw()

    for event in pygame.event.get():
        canvas.interact()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
            
        

    pygame.display.flip()