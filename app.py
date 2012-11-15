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
        self.grow = False
        self.direction = 1
        self.tiles = {}
        self.reset()

    def reset(self):
        """
        reset snake
        """
        self.grow = False
        self.direction = 1
        self.tiles = [[18, 20, 1], [19, 20, 1], [20, 20, 1]]

    def get_pos(self):
        """
        returns the position of the head of the snake
        """
        return self.tiles[-1]

    def bite(self):
        """
        checks if you bite yourself in the tail
        """
        bite = 0
        for tile1 in self.tiles:
            for tile2 in self.tiles:
                if tile1[0] == tile2[0] and tile1[1] == tile2[1]:
                    bite = bite + 1
            if bite > 1:
                return True
            bite = 0
        return False

    def move(self):
        """
        add a new pixel to the snakes head and delete the last one
        """
        # add new tile to front
        if self.direction == 0:
            self.tiles.append([self.tiles[-1][0] - 1, self.tiles[-1][1]])
        elif self.direction == 1:
            self.tiles.append([self.tiles[-1][0] + 1, self.tiles[-1][1]])
        elif self.direction == 2:
            self.tiles.append([self.tiles[-1][0], self.tiles[-1][1] - 1])
        elif self.direction == 3:
            self.tiles.append([self.tiles[-1][0], self.tiles[-1][1] + 1])

        # check collision
        if self.tiles[-1][0] < 0 or self.tiles[-1][0] > 41:
            return False
        elif self.tiles[-1][1] < 0 or self.tiles[-1][1] > 41:
            return False
        elif self.bite():
            return False
        else:
            # delete last tile
            if not self.grow:
                self.tiles.pop(0)
            self.grow = False
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
        self.font_obj = pygame.font.Font('freesansbold.ttf', 22)

        self.color_red = pygame.Color(255, 0, 0)
        self.color_green = pygame.Color(0, 255, 0)
        self.color_blue = pygame.Color(0, 0, 255)
        self.color_black = pygame.Color(0, 0, 0)
        self.color_grey = pygame.Color(128, 128, 128)

        self.snake = Snake()
        self.highscore = '0 (None)'
        self.score = 0
        self.gameover = False
        self.apple = [randrange(41), randrange(41)]
        self.oldapple = self.apple
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
                    if self.snake.direction != 1:
                        self.snake.direction = 0
                elif event.key == K_RIGHT:
                    if self.snake.direction != 0:
                        self.snake.direction = 1
                elif event.key == K_UP:
                    if self.snake.direction != 3:
                        self.snake.direction = 2
                elif event.key == K_DOWN:
                    if self.snake.direction != 2:
                        self.snake.direction = 3
                elif event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

    def run(self):
        """
        contains the gameloop
        """
        while True:
            self.eventhandler()
            self.gameover = not self.snake.move()

            if self.snake.get_pos() == self.apple:
                self.score = self.score + 1
                self.oldapple = self.apple
                self.apple = [randrange(41), randrange(41)]

            # draw grid
            #for x in range(42):
            #    pygame.draw.line(self.surface, self.color_grey, (x * 10, 24), (x * 10, 444), 1)
            #for y in range(42):
            #    pygame.draw.line(self.surface, self.color_grey, (0, y * 10 + 24), (420, y * 10 + 24), 1)

            self.surface.fill(self.color_black)
            self.draw_apple()

            for i in range(len(self.snake.tiles)):
                # paint dot
                pygame.draw.rect(self.surface,
                                 self.color_red,
                                 (self.snake.tiles[i][0] * 10 + 2, self.snake.tiles[i][1] * 10 + 26, 6, 6))
                # paint the part that connects to the next dot
                if i > 0:
                    if self.snake.tiles[i - 1][0] < self.snake.tiles[i][0]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10, self.snake.tiles[i][1] * 10 + 26, 2, 6))
                    if self.snake.tiles[i - 1][0] > self.snake.tiles[i][0]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10 + 8, self.snake.tiles[i][1] * 10 + 26, 2, 6))
                    if self.snake.tiles[i - 1][1] < self.snake.tiles[i][1]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10 + 2, self.snake.tiles[i][1] * 10 + 24, 6, 2))
                    if self.snake.tiles[i - 1][1] > self.snake.tiles[i][1]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10 + 2, self.snake.tiles[i][1] * 10 + 32, 6, 2))
                # paint the part that connects to the previous dot
                if i < len(self.snake.tiles) - 1:
                    if self.snake.tiles[i + 1][0] < self.snake.tiles[i][0]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10, self.snake.tiles[i][1] * 10 + 26, 2, 6))
                    if self.snake.tiles[i + 1][0] > self.snake.tiles[i][0]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10 + 8, self.snake.tiles[i][1] * 10 + 26, 2, 6))
                    if self.snake.tiles[i + 1][1] < self.snake.tiles[i][1]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10 + 2, self.snake.tiles[i][1] * 10 + 24, 6, 2))
                    if self.snake.tiles[i + 1][1] > self.snake.tiles[i][1]:
                        pygame.draw.rect(self.surface,
                                     self.color_red,
                                     (self.snake.tiles[i][0] * 10 + 2, self.snake.tiles[i][1] * 10 + 32, 6, 2))
            # draw head
            pygame.draw.circle(self.surface,
                               self.color_red,
                               (self.snake.tiles[-1][0] * 10 + 5,
                                self.snake.tiles[-1][1] * 10 + 5 + 24),
                               5, 0)
            if self.oldapple in self.snake.tiles:
                pygame.draw.circle(self.surface,
                                   self.color_red,
                                   (self.oldapple[0] * 10 + 5,
                                    self.oldapple[1] * 10 + 5 + 24),
                                   5, 0)

            if self.snake.tiles[0] == self.oldapple:
                self.snake.grow = True
                self.oldapple = [50, 50]

            score_text = 'Score: ' + str(self.score) + \
                         ' - Highscore: ' + self.highscore
            msg_surface = self.font_obj.render(score_text,
                                               False,
                                               self.color_blue)
            msg_rect = msg_surface.get_rect()
            msg_rect.topleft = (5, 0)
            self.surface.blit(msg_surface, msg_rect)

            pygame.draw.line(self.surface, self.color_grey, (0, 24), (420, 24), 1)

            pygame.display.update()
            pygame.display.flip()
            self.fps_clock.tick(5 + self.score / 5)

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