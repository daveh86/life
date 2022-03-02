#!/usr/bin/env python

import random
import time
from random import randint

import unicornhathd


print("""Unicorn HAT HD: Game Of Life

Runs Conway's Game Of Life on your Unicorn HAT, this starts
with a random spread of life, so results may vary!
""")

try:
    xrange
except NameError:
    xrange = range

unicornhathd.rotation(0)
unicornhathd.brightness(0.5)
width, height = unicornhathd.get_shape()

size = width * height


class GameOfLife:
    def __init__(self):
        self.board = [int(7 * random.getrandbits(1)) for _ in xrange(size)]
        self.start = time.time()
        self.lboard = None
        self.llboard = None
        self.color_offset = randint(0, 5)
        self.color = [
                        [[154, 154, 174], [0, 0, 255],   [0, 0, 200],   [0, 0, 160],   [0, 0, 140],   [0, 0, 90],  [0, 0, 60],  [0, 0, 0]],
                        [[154, 154, 174], [255, 255, 0], [200, 200, 0], [160, 160, 0], [140, 140, 0], [90, 90, 0], [60, 60, 0], [0, 0, 0]],
                        [[154, 154, 174], [0, 255, 0],   [0, 200, 0],   [0, 160, 0],   [0, 140, 0],   [0, 90, 0],  [0, 60, 0],  [0, 0, 0]],
                        [[154, 154, 174], [0, 255, 255], [0, 200, 200], [0, 160, 160], [0, 140, 140], [0, 90, 90], [0, 60, 60], [0, 0, 0]],
                        [[154, 154, 174], [255, 0, 255], [200, 0, 200], [160, 0, 160], [140, 0, 140], [90, 0, 90], [60, 0, 60], [0, 0, 0]],
                        [[154, 154, 174], [255, 155, 0], [200, 122, 0], [160, 101, 0], [140, 85, 0],  [90, 60, 0], [60, 30, 0], [0, 0, 0]],
                        [[154, 154, 174], [255, 0, 0],   [200, 0, 0],   [160, 0, 0],   [140, 0, 0],   [90, 0, 0],  [60, 0, 0],  [0, 0, 0]]
                     ]

    def value(self, x, y):
        index = ((x % width) * height) + (y % height)
        return self.board[index]

    def neighbors(self, x, y):
        sum = 0
        for i in xrange(3):
            for j in xrange(3):
                if i == 1 and j == 1:
                    continue
                if self.value(x + i - 1, y + j - 1) == 0:
                    sum = sum + 1
        return sum

    def next_generation(self):
        new_board = [False] * size
        for i in xrange(width):
            for j in xrange(height):
                neigh = self.neighbors(i, j)
                lvl = self.value(i, j)
                if lvl == 0:
                    if neigh < 2:
                        new_board[i * height + j] = min(7, lvl + 1)
                    elif 2 <= neigh <= 3:
                        new_board[i * height + j] = 0
                    else:
                        new_board[i * height + j] = min(7, lvl + 1)
                else:
                    if neigh == 3 or neigh == 6:
                        new_board[i * height + j] = 0
                    else:
                        new_board[i * height + j] = min(7, lvl + 1)
        self.llboard = self.lboard
        self.lboard = self.board
        self.board = new_board


    def stuck(self):
        if not self.lboard or not self.llboard:
            return False
        for i in xrange(size):
            if self.board[i] != self.lboard[i] and self.board[i] != self.llboard[i]:
                return False
        return True

    def all_dead(self):
        if time.time() - self.start > 300:
            return True
        for i in xrange(size):
            if self.board[i] != 7:
                return False
        return True

    def show_board(self):
        for i in xrange(width):
            for j in xrange(height):
                rgb = self.color[self.color_offset][self.value(i, j)]
                unicornhathd.set_pixel(i, j, rgb[0], rgb[1], rgb[2])
        unicornhathd.show()

    def star_wipe(self):
        # Fill empty
        for i in xrange(width):
            for j in xrange(height):
                unicornhathd.set_pixel(i, j, 0, 0, 0)
        # Wipe to midway
        for x in xrange(width):
            y = 0
            unicornhathd.set_pixel(x, y, 255, 255, 255)
            while x > 0:
                x = x - 1
                y = y + 1
                unicornhathd.set_pixel(x, y, 255, 255, 255)
            unicornhathd.show()
            time.sleep(0.05)
        #Wipe to rest
        for y in range(1, width):
            x = width - 1
            unicornhathd.set_pixel(x, y, 255, 255, 255)
            while y < width - 1:
                x = x - 1
                y = y + 1
                unicornhathd.set_pixel(x, y, 255, 255, 255)
            unicornhathd.show()
            time.sleep(0.05)
        # Remove final Wipe
        for x in xrange(width):
            y = 0
            unicornhathd.set_pixel(x, y, 0, 0, 0)
            while x > 0:
                x = x - 1
                y = y + 1
                unicornhathd.set_pixel(x, y, 0, 0, 0)
            unicornhathd.show()
            time.sleep(0.05)
        #Wipe to rest
        for y in range(1, width):
            x = width -1 
            unicornhathd.set_pixel(x, y, 0, 0, 0)
            while y < width - 1:
                x = x - 1
                y = y + 1
                unicornhathd.set_pixel(x, y, 0, 0, 0)
            unicornhathd.show()
            time.sleep(0.05)


life = GameOfLife()

try:
    while True:
        if not life.all_dead() and not life.stuck():
            life.next_generation()
            life.show_board()
            time.sleep(0.05)
        else:
            life.star_wipe()
            life = GameOfLife()

except KeyboardInterrupt:
    unicornhathd.off()