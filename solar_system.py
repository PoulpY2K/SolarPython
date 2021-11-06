#!/usr/bin/env python

import json
import sys
import pygame
import math
import itertools
pygame.init()

screenW, screenH = 1680, 900


class SolarSystemObject:
    min_display_size = 8
    display_log_base = 1.2

    def __init__(
        self,
        solar_system,
        name,
        mass,
        color,
        position=(0, 0),
        velocity=(0, 0),
    ):
        self.solar_system = solar_system
        self.screen = self.solar_system.screen
        self.name = name
        self.mass = mass
        self.color = color
        self.position = position
        self.velocity = velocity
        self.display_size = self.calculate_display_size()

        solar_system.add_object(self)

    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           self.position, self.display_size)

    def move(self):
        if not isinstance(self, Sun):
            self.position = (
                self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def calculate_display_size(self):
        return max(math.log(self.mass, self.display_log_base), self.min_display_size,)

    def distance(self, object):
        return math.hypot(self.position[0] - object.position[0], self.position[1] - object.position[1])

    def angle(self, object):
        dx, dy = (self.position[0] - object.position[0],
                  self.position[1] - object.position[1])
        return math.atan2(dy, dx)


class Sun(SolarSystemObject):
    def __init__(
            self,
            solar_system,
            mass,
            name = "Soleil",
            position=(screenW/2, screenH/2),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, name, mass, (255, 255, 0), position, velocity)


class Planet(SolarSystemObject):
    colours = itertools.cycle([(255, 0, 0), (0, 255, 0), (0, 0, 255)])

    def __init__(
            self,
            solar_system,
            name,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, name, mass, next(Planet.colours),
                         (screenW/2 + position[0], screenH/2 + position[1]), velocity)


class Mouse():
    def __init__(
            self,
            mass,
            position=(0, 0),
    ):
        self.mass = mass
        self.position = position


class SolarSystem:
    def __init__(self, width, height, bgColor=(0, 0, 0)):
        self.screen = pygame.display.set_mode((width, height))
        self.bgColor = bgColor
        self.clock = pygame.time.Clock()
        self.objects = []

    def add_object(self, object):
        if(object not in self.objects):
            self.objects.append(object)

    def remove_object(self, object):
        if(object in self.objects):
            self.objects.remove(object)

    def update(self):
        for object in self.objects:
            if isinstance(object, SolarSystemObject):
                object.move()
                object.draw()
        pygame.display.flip()
        self.clock.tick_busy_loop(60)

    @staticmethod
    def gravity_acceleration(
            first: SolarSystemObject,
            second: SolarSystemObject,
    ):
        force = (first.mass * second.mass) / first.distance(second) ** 2
        angle = first.angle(second)
        reverse = -1
        for object in first, second:
            if isinstance(object, SolarSystemObject):
                a = force / object.mass
                ax = a * math.cos(angle)
                ay = a * math.sin(angle)
                object.velocity = (
                    object.velocity[0] + (reverse * ax),
                    object.velocity[1] + (reverse * ay),
                )
                reverse = 1

    def check_collision(self, first, second):
        # if isinstance(first, Planet) and isinstance(second, Planet): #------------Permet d'empêcher la suppression en cas de rencontre de planète
        #     return
        if first.distance(second) < first.display_size + second.display_size:
            for object in first, second:
                if isinstance(object, Planet):
                    self.remove_object(object)
                elif isinstance(object, Sun):
                    object.mass += (first.mass if isinstance(first,
                                    Planet) else second.mass)
                    object.display_size = object.calculate_display_size()

    def calculate_all_object_interactions(self):
        objects_copy = self.objects.copy()
        for idx, first in enumerate(objects_copy):
            for second in objects_copy[idx + 1:]:
                self.gravity_acceleration(first, second)
                if not isinstance(first, Mouse) and not isinstance(second, Mouse):
                    self.check_collision(first, second)

    def run(self):

        global planetsFromJSON
        planets = []

        with open("planets.json", 'r') as f:
            planetsFromJSON = json.load(f)

        sun = Sun(self, mass=30)
        
        for name in planetsFromJSON:
            value = planetsFromJSON[name]
            planets.append(Planet(self, value["name"], value["mass"], (value["pos"][0] + sun.display_size, value["pos"][1] + sun.display_size), value["v"]))
            print(planets[-1].position)

        mouse_object = Mouse(60)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEMOTION:
                    mouse_object.position = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.add_object(mouse_object)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and mouse_object in self.objects:
                        self.remove_object(mouse_object)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            self.screen.fill(self.bgColor)

            self.calculate_all_object_interactions()
            self.update()


solar_system = SolarSystem(width=screenW, height=screenH)
solar_system.run()
