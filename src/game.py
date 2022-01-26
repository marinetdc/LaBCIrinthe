import pygame
import os
import numpy as np
import time
from math import sqrt
import random
import mazeGeneration
from serialData import readSerialData, readLine
from serial import *

terrain_dict = {'WALL': 0, 'ROAD': 1, 'GOAL': 2, 'START': 3}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

firstiteration = True # helps the palette swap
#port = 'COM5'  # specify port used to read analog data (EDA/ECG)
#s = Serial(port)
#device = readLine(s)  # might be a costly solution


class Game:
    def __init__(self, grid_width, grid_height, block_size, fps, mode = 'generation'):
        """
        define width and height in cells
        generation mode automatically generates levels / test mode loads handmade levels
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.block_size = block_size
        self.width = block_size * grid_width
        self.height = block_size * grid_height
        self.fps = fps
        self.mode = mode

        pygame.display.set_caption('A-Mazing game')
        pygame.font.init()
        self.window = pygame.display.set_mode((self.width, self.height))

        # Flags
        self.arrived = False
        self.ended = False
        self.running = True
        self.end_drawn = False
        self.odd = False

        self.level = 1
        self.errors = 0
        self.start = 0
        self.terrain = None
        self.agent = None
        self.visibility = 4

        # events
        self.level_ended = pygame.USEREVENT + 1

        # Levels
        if mode == 'generation':

            level1 = mazeGeneration.Maze('level1', width = self.grid_width, height = self.grid_height)
            level2 = mazeGeneration.Maze('level2', width = self.grid_width, height = self.grid_height)
            level3 = mazeGeneration.Maze('level3', width = self.grid_width, height = self.grid_height)
            level1 = np.loadtxt(os.path.join('../assets/levels', 'level1.csv'), delimiter=',')
            level2 = np.loadtxt(os.path.join('../assets/levels', 'level2.csv'), delimiter=',')
            level3 = np.loadtxt(os.path.join('../assets/levels', 'level3.csv'), delimiter=',')
        if mode == 'test':
            level1 = np.loadtxt(os.path.join('../assets', 'level1.csv'), delimiter=',')
            level2 = np.loadtxt(os.path.join('../assets', 'level2.csv'), delimiter=',')
            level3 = np.loadtxt(os.path.join('../assets', 'level3.csv'), delimiter=',')
            
        self.current_level = level1
        self.levels = [level1, level2, level3]
        self.load_level(level1)

        # Images
        agent_img0 = pygame.image.load(os.path.join('../assets', 'agent-0.png'))
        self.agent_img0 = pygame.transform.scale(agent_img0, (self.block_size, self.block_size))
        agent_img1 = pygame.image.load(os.path.join('../assets', 'agent-1.png'))
        self.agent_img1 = pygame.transform.scale(agent_img1, (self.block_size, self.block_size))
        grass = pygame.image.load(os.path.join('../assets', 'grass.png'))
        self.grass = pygame.transform.scale(grass, (self.block_size, self.block_size))
        road = pygame.image.load(os.path.join('../assets', 'road.png'))
        self.road = pygame.transform.scale(road, (self.block_size, self.block_size))
        
        goal0 = pygame.image.load(os.path.join('../assets', 'goal-0.png'))
        self.goal0 = pygame.transform.scale(goal0, (self.block_size, self.block_size))
        goal1 = pygame.image.load(os.path.join('../assets', 'goal-1.png'))
        self.goal1 = pygame.transform.scale(goal1, (self.block_size, self.block_size))

    def palette_swap(self, surf, old_color, new_color):
        #select a color to be replaced
        img_copy = pygame.Surface(surf.get_size())
        img_copy.fill(new_color)
        surf.set_colorkey(old_color)
        img_copy.blit(surf, (0, 0))
        return img_copy
    
    def run(self):
        clock = pygame.time.Clock()
        self.start = time.time()

        counter = 0
        while self.running:
            clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == self.level_ended:
                    self.ended = True
                if event.type == pygame.QUIT:
                    self.running = False

            # Check flags
            if not self.ended:
                self.handle_decision()
            if self.arrived:
                self.ended = True
                self.arrived = False

            '''
            PALETTE SWAP TEST
            '''
            global firstiteration
            # road
            
            if firstiteration == True:
                channel_1 = 255
                channel_2 = 179
                channel_3 = 0
                global port
            self.original_c = ((channel_1%256), channel_2%256, channel_3%256)
            self.road = self.palette_swap(self.road, self.original_c, ((channel_1 + 1)%256, 179, 0))
            self.road.set_colorkey((0, 0, 0))
            
            # grass
            '''
            if firstiteration == True:
                channel_1_grass = 139
                channel_2_grass = 195
                channel_3_grass = 74
                firstiteration = False
            self.original_c_grass = ((channel_1_grass%256), channel_2_grass%256, channel_3_grass%256)
            self.grass = self.palette_swap(self.grass, self.original_c_grass, ((channel_1_grass + 1)%256, 195, 74))
            self.grass.set_colorkey((0, 0, 0))
            channel_1_grass -= 1
            '''

            self.draw()

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE] and not self.end_drawn and self.ended:
                self.level += 1
                self.load_level(self.levels[self.level - 1])
                self.ended = False

            if counter % 5 == 0:
                self.odd = not self.odd
            counter += 1
            
    def draw(self):
        if not self.ended:
            self.window.fill(BLACK)
            self.draw_terrain()
            self.print_status()
            if self.odd:
                self.window.blit(self.agent_img0, (self.agent.x, self.agent.y))
            else:
                self.window.blit(self.agent_img1, (self.agent.x, self.agent.y))
        elif self.level <= 2:
            self.draw_end_level()
        else:
            self.draw_game_end()
        pygame.display.update()

    def draw_terrain(self):
        if self.level != 3:
            for i in range(self.grid_height):
                for j in range(self.grid_width):
                    x = self.to_coord(j)
                    y = self.to_coord(i)
                    if self.current_level[i, j] == 0:
                        self.window.blit(self.grass, (x, y))
                    elif self.current_level[i, j] == 1:
                        self.window.blit(self.road, (x, y))
                    elif self.current_level[i, j] == 2:
                        self.window.blit(self.road, (x, y))
                        if self.odd:
                            self.window.blit(self.goal0, (x, y))
                        else:
                            self.window.blit(self.goal1, (x, y))
                    else:
                        self.window.blit(self.road, (x, y))
        else:
            self.draw_level3()

    def draw_level3(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                x = self.to_coord(j)
                y = self.to_coord(i)
                dist = sqrt((self.to_grid(self.agent.x - x))**2 + (self.to_grid(self.agent.y - y))**2)
                if dist < self.visibility:
                    if self.current_level[i, j] == 0:
                        self.window.blit(self.grass, (x, y))
                    elif self.current_level[i, j] == 1:
                        self.window.blit(self.road, (x, y))
                    elif self.current_level[i, j] == 2:
                        self.window.blit(self.road, (x, y))
                        if self.odd:
                            self.window.blit(self.goal0, (x, y))
                        else:
                            self.window.blit(self.goal0, (x, y))
                    else:
                        self.window.blit(self.road, (x, y))

    def print_status(self):
        # Set font
        font_size = 20
        font = pygame.font.Font('freesansbold.ttf', font_size)

        text = font.render('Lv. {}'.format(self.level), True, RED)
        text_rect = text.get_rect()
        text_rect.center = (int(self.width / 4) - 50, text_rect.height)
        self.window.blit(text, text_rect)

        text = font.render('TIME: {:.0f}'.format(time.time() - self.start), True, RED)
        text_rect = text.get_rect()
        text_rect.center = (int(self.width / 4 + 50), text_rect.height)
        self.window.blit(text, text_rect)

        text = font.render('ERRORS: {}'.format(self.errors), True, RED)
        text_rect = text.get_rect()
        text_rect.center = (int(self.width / 4 * 3), text_rect.height)
        self.window.blit(text, text_rect)

    def handle_decision(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT] and self.move_possible('LEFT'):
            self.agent.x -= self.block_size
        if keys_pressed[pygame.K_RIGHT] and self.move_possible('RIGHT'):
            self.agent.x += self.block_size
        if keys_pressed[pygame.K_UP] and self.move_possible('UP'):
            self.agent.y -= self.block_size
        if keys_pressed[pygame.K_DOWN] and self.move_possible('DOWN'):
            self.agent.y += self.block_size

        if self.current_level[self.to_grid(self.agent.y), self.to_grid(self.agent.x)] == 2:
            self.arrived = True

    def move_possible(self, direction):
        if not self.in_window(direction):
            self.errors += 1
            return False
        grid_x = self.to_grid(self.agent.x)
        grid_y = self.to_grid(self.agent.y)

        if direction == 'LEFT':
            grid_x -= 1
        if direction == 'RIGHT':
            grid_x += 1
        if direction == 'UP':
            grid_y -= 1
        if direction == 'DOWN':
            grid_y += 1

        if self.current_level[grid_y, grid_x] == 0:
            self.errors += 1
            return False
        else:
            return True

    def in_window(self, direction):
        if direction == 'LEFT':
            return 0 < self.to_grid(self.agent.x)
        if direction == 'RIGHT':
            return self.to_grid(self.agent.x) < self.grid_width - 1
        if direction == 'UP':
            return 0 < self.to_grid(self.agent.y)
        if direction == 'DOWN':
            return self.to_grid(self.agent.y) < self.grid_height - 1

    def load_level(self, level):
        self.current_level = level
        start = np.argwhere(self.current_level == terrain_dict['START'])
        self.agent = pygame.Rect(self.to_coord(start[0, 1]),
                                 self.to_coord(start[0, 0]),
                                 self.block_size, self.block_size)


    def to_grid(self, val):
        return int(val // self.block_size)

    def to_coord(self, val):
        return val * self.block_size

    def draw_end_level(self):

        self.window.fill(WHITE)

        # Set font
        font_size = 30
        font = pygame.font.Font('freesansbold.ttf', font_size)

        text = font.render('End of the level {}'.format(self.level), True, RED)
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2, self.height // 2)
        self.window.blit(text, text_rect)

        text = font.render('Press [SPACE] to continue', True, RED)
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2, self.height // 2 + 40)

        self.window.blit(text, text_rect)

    def draw_game_end(self):
        if not self.end_drawn:
            self.window.fill(WHITE)

            # Set font
            font_size = 30
            font = pygame.font.Font('freesansbold.ttf', font_size)

            text = font.render('End of the game!!', True, RED)
            text_rect = text.get_rect()
            text_rect.center = (self.width // 2, self.height // 2)
            self.window.blit(text, text_rect)

            text = font.render('Time to complete: {:.0f} seconds'.format(time.time() - self.start), True, RED)
            text_rect = text.get_rect()
            text_rect.center = (self.width // 2, self.height // 2 + 40)
            self.window.blit(text, text_rect)

            text = font.render('Number of errors: {}'.format(self.errors), True, RED)
            text_rect = text.get_rect()
            text_rect.center = (self.width // 2, self.height // 2 + 80)
            self.window.blit(text, text_rect)
            self.end_drawn = True


if __name__ == '__main__':
    game = Game(20, 20, 20, 10, mode='generation')
    game.run()
