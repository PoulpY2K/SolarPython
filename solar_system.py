#!/usr/bin/env python

import sys
import pygame
import math
from astroquery.jplhorizons import Horizons
pygame.init()

screenW, screenH = 1280, 720
screen = pygame.display.set_mode((screenW, screenH))
# pygame.draw.circle(screen,  (255, 100, 0), (100,100), 20)
# pygame.draw.aaline(screen, (255, 255, 255), (160, 100), p)
# screen.set_at((10, 10), (255,0,0))

play = True
clock = pygame.time.Clock()
mouse = None

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEMOTION:
            mouse = event.pos
        if event.type == pygame.KEYUP:
            print(event.key, event.unicode, event.scancode)
            if event.key == pygame.K_ESCAPE:
                play = False

    screen.fill((0, 0, 0))

    clock.tick(60)
    pygame.display.flip()