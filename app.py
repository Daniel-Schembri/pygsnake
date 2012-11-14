#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pygsnake - A simple snake game in Python with Pygame

Created on Mon Oct 29 07:48:38 2012

@author: XenGi
"""

import sys
import pygame
from pygame.locals import *
from random import randrange
import getpass


class Snake:
    """
    The snake
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """
        reset snake
        """
        self.lastdirection = 'right'
        self.direction = 'right'
        self.tiles = [[18, 20, 0], [19, 20, 0], [20, 20, 0]]

    def move_right(self):
        """
        set direction of snake to right
        """
        if self.direction == 'left':
            return False
        else:
            self.lastdirection = self.direction
            self.direction = 'right'
            return True

    def move_left(self):
        """
        set direction of snake to right
        """
        if self.direction == 'right':
            return False
        else:
            self.lastdirection = self.direction
            self.direction = 'left'
            return True

    def move_up(self):
        """
        set direction of snake to right
        """
        if self.direction == 'down':
            return False
        else:
            self.lastdirection = self.direction
            self.direction = 'up'
            return True

    def move_down(self):
        """
        set direction of snake to right
        """
        if self.direction == 'up':
            return False
        else:
            self.lastdirection = self.direction
            self.direction = 'down'
            return True

    def move(self, apple=False):
        """
        add a new pixel to the snakes head and delete the last one
        """
        # add new tile to front
        head = self.tiles[-1]
        if head in self.tiles[:-1]:
            return False
        if self.direction == 'right':
            if self.lastdirection == 'right':
                self.tiles.append([head[0] + 1, head[1], '-'])  #rr
            if self.lastdirection == 'up':
                self.tiles.append([head[0] + 1, head[1], 'ur'])
            if self.lastdirection == 'down':
                self.tiles.append([head[0] + 1, head[1], 'dr'])
        elif self.direction == 'left':
            if self.lastdirection == 'left':
                self.tiles.append([head[0] - 1, head[1], '-'])  #ll
            if self.lastdirection == 'up':
                self.tiles.append([head[0] - 1, head[1], 'lu'])
            if self.lastdirection == 'down':
                self.tiles.append([head[0] - 1, head[1], 'ld'])
        elif self.direction == 'up':
            if self.lastdirection == 'right':
                self.tiles.append([head[0], head[1] - 1, 'ur'])
            if self.lastdirection == 'left':
                self.tiles.append([head[0], head[1] - 1, 'ul'])
            if self.lastdirection == 'up':
                self.tiles.append([head[0], head[1] - 1, '|']) #uu
        elif self.direction == 'down':
            if self.lastdirection == 'right':
                self.tiles.append([head[0], head[1] + 1, 'dr'])
            if self.lastdirection == 'left':
                self.tiles.append([head[0], head[1] + 1, 'dl'])
            if self.lastdirection == 'down':
                self.tiles.append([head[0], head[1] + 1, '|']) #dd

        # check collision
        if head[0] < 0 or head[0] > 41:
            return False
        elif head[1] < 0 or head[1] > 41:
            return False
        else:
            # delete last tile
            if not apple:
                self.tiles.pop(0)
            return True


class App:
    """
    The game
    """
    def __init__(self):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((420, 444), DOUBLEBUF)
        pygame.display.set_caption('PyGSnake')
        self.font_obj = pygame.font.Font('freesansbold.ttf', 24)

        self.color_red = pygame.Color(255, 0, 0)
        self.color_green = pygame.Color(0, 255, 0)
        self.color_blue = pygame.Color(0, 0, 255)
        self.color_black = pygame.Color(0, 0, 0)

        self.score = 0
        self.apple = [randrange(41), randrange(41)]
        self.snake = Snake()

        self.reset()

    def write_highscore(self):
        """
        write the highscore and username to the highscore file
        """
        try:
            hfile = open('highscore', 'w')
            hfile.write(str(self.score) + ' (' + getpass.getuser() + ')')
            hfile.close()
        except IOError, exc:
            print 'Can\'t write highscore to file.', exc.message

    def draw_apple(self):
        """
        draw the apple
        """
        pygame.draw.circle(self.surface,
                           self.color_green,
                           (self.apple[0] * 10 + 5,
                            self.apple[1] * 10 + 5 + 24),
                           5, 0)

    def eventhandler(self):
        """
        change the direction of the snake according to pressed keys
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.gameover = not self.snake.move_left()
                elif event.key == K_RIGHT:
                    self.gameover = not self.snake.move_right()
                elif event.key == K_UP:
                    self.gameover = not self.snake.move_up()
                elif event.key == K_DOWN:
                    self.gameover = not self.snake.move_down()
                elif event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

    def run(self):
        """
        contains the gameloop
        """
        while True:
            self.surface.fill(self.color_black)
            self.draw_apple()
            if (self.apple[0] == self.snake.tiles[-1][0] and
                self.apple[1] == self.snake.tiles[-1][1]):
                self.score = self.score + 1
                self.apple = [randrange(41), randrange(41)]
                self.gameover = not self.snake.move(apple=True)
            else:
                self.gameover = not self.snake.move()

            for tile in self.snake.tiles:
                if tile[2] == '-':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10, tile[1] * 10 + 25, 10, 8))
                if tile[2] == 'lu':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10, tile[1] * 10 + 25, 9, 8))
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 1))
                if tile[2] == 'ld':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10, tile[1] * 10 + 25, 9, 8))
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 33, 8, 1))
                if tile[2] == 'ru':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 10))
                if tile[2] == 'rd':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 10))
                if tile[2] == '|':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 10))
                if tile[2] == 'ul':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 10))
                if tile[2] == 'ur':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 10))
                if tile[2] == 'dl':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 10))
                if tile[2] == 'dr':
                    pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (tile[0] * 10 + 1, tile[1] * 10 + 24, 8, 10))

            score_text = 'Score: ' + str(self.score) + \
                         ' - Highscore: ' + self.highscore
            msg_surface = self.font_obj.render(score_text,
                                               False,
                                               self.color_blue)
            msg_rect = msg_surface.get_rect()
            msg_rect.topleft = (0, 0)
            self.surface.blit(msg_surface, msg_rect)

            pygame.display.update()
            pygame.display.flip()
            self.fps_clock.tick(10 + self.score / 5)

            self.eventhandler()

            if self.gameover:
                break

        if self.score > int(self.highscore.split()[0]):
            self.write_highscore()
        msg_surface1 = self.font_obj.render('Game Over',
                                           False,
                                           self.color_blue)
        msg_rect1 = msg_surface1.get_rect()
        msg_rect1.center = (210, 210)
        msg_surface2 = self.font_obj.render('Continue? [Y/N]',
                                           False,
                                           self.color_blue)
        msg_rect2 = msg_surface2.get_rect()
        msg_rect2.center = (210, 258)
        self.surface.blit(msg_surface1, msg_rect1)
        self.surface.blit(msg_surface2, msg_rect2)
        pygame.display.update()
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        return True
                    elif event.key == K_n:
                        return False

    def reset(self):
        """
        reset game
        """
        self.score = 0
        try:
            hfile = open('highscore', 'r')
            self.highscore = hfile.read()
            hfile.close()
        except IOError:
            self.highscore = '0 (None)'
        self.gameover = False

        self.snake.reset()
        self.apple = [randrange(41), randrange(41)]


if __name__ == '__main__':
    APP = App()
    GAMELOOP = True
    while(GAMELOOP):
        GAMELOOP = APP.run()
        APP.reset()