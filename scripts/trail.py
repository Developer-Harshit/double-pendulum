import pygame
import math
from random import random, choice, randint
from scripts.const import (
    BG_COLOR,
    GREEN,
    CYAN,
    BLUE,
    VIOLET,
    PINK,
    RED,
    ORANGE,
    WHITE,
    WIDTH,
    HEIGHT,
    RENDER_SCALE,
)

COLOR_SET = choice([[BLUE, VIOLET, PINK], [RED, ORANGE, PINK], [GREEN, BLUE, CYAN]])


def draw_circle(radius, color=WHITE):
    surf = pygame.Surface((radius * 2, radius * 2))

    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


class Particle:
    def __init__(self, pos, circle, dec=1):
        self.pos = list(pos)
        self.circle = circle
        self.alpha = 200
        self.dec = dec

        pass

    def update(self):  # pos, circle):
        self.alpha = max(self.alpha - self.dec, 0)

    def render(self, surf):
        self.circle.set_alpha(self.alpha)
        surf.blit(
            self.circle,
            self.pos,
        )


class Trail:
    def __init__(self, host, dec=5, history=False):
        self.host = host
        self.circles = []

        self.aoff = 1
        self.history = history
        self.display = pygame.Surface((WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE))
        self.display.set_colorkey((0, 0, 0))

        for i in range(150):
            self.circles.append(
                draw_circle(
                    int(self.host.radius * random() * 0.25 + 0.4),
                    choice(COLOR_SET),
                )
            )
        self.particles = []
        self.dec = dec

    def clear_history(self):
        self.display = pygame.Surface((WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE))
        self.display.set_colorkey((0, 0, 0))
        self.particles = []

    def add_particle(self):
        self.particles.append(
            Particle(self.get_pos(self.host.pos), choice(self.circles), self.dec)
        )

    def get_pos(self, anchor):
        self.aoff += 1
        return (
            anchor[0],
            anchor[1] + math.sin(self.aoff) * 1.2,
        )

    def update(self):
        self.add_particle()

        for par in self.particles:
            par.update()  # self.get_pos(self.host.pos), choice(self.circles))
            if par.alpha <= 0:
                self.particles.remove(par)

    def render(self, surf):
        if self.history:
            for par in self.particles:
                par.render(self.display)
                # par.render(surf)

            surf.blit(self.display, (0, 0))

        else:
            for par in self.particles:
                par.render(surf)
