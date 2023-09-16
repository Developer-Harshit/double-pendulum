import math
import pygame
from random import random, randint
from scripts.text import Text
from scripts.const import RED, WHITE, BLUE, GREEN, WIDTH, HEIGHT, RENDER_SCALE


g = 2
SCALE = 2


class Control_Pendulum:
    def __init__(self, pen, size=20):
        self.pen = pen
        self.blob = 1

        self.blob_text = Text(
            "Active Blob", (0, HEIGHT / RENDER_SCALE - size * 2), str(self.blob), size
        )

        self.m1_txt = Text("Mass 1", (0, 5), (str(round((self.pen.m1), 3))), size)
        self.m2_txt = Text(
            "Mass 2", (0, size + 10), (str(round((self.pen.m2), 3))), size
        )
        self.r1_txt = Text(
            "Length 1", (0, size * 2 + 15), (str(round((self.pen.r1), 3))), size
        )
        self.r2_txt = Text(
            "Length 2", (0, size * 3 + 20), (str(round((self.pen.r2), 3))), size
        )

        self.a1_txt = Text(
            "Angle 1",
            (0, size * 4 + 25),
            (str(round(math.degrees(self.pen.a1), 3))),
            size,
        )
        self.a2_txt = Text(
            "Angle 2",
            (0, size * 5 + 30),
            (str(round(math.degrees(self.pen.a2), 3))),
            size,
        )

    def update_text(self):
        self.m1_txt.update((str(round((self.pen.m1), 3))))
        self.m2_txt.update((str(round((self.pen.m2), 3))))

        self.a1_txt.update(str(round(math.degrees(self.pen.a1), 3)))
        self.a2_txt.update(str(round(math.degrees(self.pen.a2), 3)))

        self.r1_txt.update((str(round((self.pen.r1), 3))))
        self.r2_txt.update((str(round((self.pen.r2), 3))))

        self.blob_text.update(str(self.blob))

    def render_text(self, surf):
        self.m1_txt.render(surf)
        self.m2_txt.render(surf)

        self.a1_txt.render(surf)
        self.a2_txt.render(surf)

        self.r1_txt.render(surf)
        self.r2_txt.render(surf)

        self.blob_text.render(surf)

        pass

    def update_mass(self, amount=0.1):
        if self.blob == 1:
            self.pen.m1 += amount
        else:
            self.pen.m2 += amount

    def update_angle(self, amount=0.1):
        if self.blob == 1:
            self.pen.a1 += amount
        else:
            self.pen.a2 += amount

    def update_length(self, amount=0.1):
        if self.blob == 1:
            self.pen.r1 += amount
        else:
            self.pen.r2 += amount


class Pendulum:
    def __init__(self, pos):
        self.hook = pos
        self.m1, self.m2 = 15, 20
        self.radius = self.m2 / SCALE / 2
        self.r1, self.r2 = 150, 150

        self.a1, self.a2 = 0, 0  # math.pi / randint(1, 10), math.pi / randint(1, 10)

        self.a1_v, self.a2_v = 0, 0
        self.a1_a, self.a2_a = 0, 0
        self.update_pos()

    def render(self, surf):
        self.update_pos()

        pos1 = (self.x1 - self.m1 / 2, self.y1 + self.m1 / 2)
        pos2 = (self.x2 - self.m2 / 2, self.y2 + self.m2 / 2)
        hook_pos = (self.hook[0] - 2.5, self.hook[1] + 2.5)

        pygame.draw.aaline(surf, WHITE, hook_pos, pos1)
        pygame.draw.aaline(surf, WHITE, pos1, pos2)

        pygame.draw.circle(surf, GREEN, hook_pos, 5)
        pygame.draw.circle(surf, RED, pos1, self.m1 / SCALE)
        pygame.draw.circle(surf, BLUE, pos2, self.m2 / SCALE)

        pass

    def update_acc1(self):
        exp1 = -g * (2 * self.m1 + self.m2) * math.sin(self.a1)
        exp2 = self.m2 * g * math.sin(self.a1 - 2 * self.a2)
        exp3 = (
            2
            * math.sin(self.a1 - self.a2)
            * self.m2
            * (
                (self.a2_v * self.a2_v) * self.r2
                + (self.a1_v * self.a1_v) * self.r1 * math.cos(self.a1 - self.a2)
            )
        )
        exp4 = self.r1 * (
            2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.a1 - 2 * self.a2)
        )

        self.a1_a = (exp1 - exp2 - exp3) / (exp4)

    def update_acc2(self):
        exp1 = 2 * math.sin(self.a1 - self.a2)
        exp2 = (self.a1_v * self.a1_v) * self.r1 * (self.m1 + self.m2)
        exp3 = g * (self.m1 + self.m2) * math.cos(self.a1)
        exp4 = (self.a2_v * self.a2_v) * self.r2 * self.m2 * math.cos(self.a1 - self.a2)
        exp5 = self.r2 * (
            2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.a1 - 2 * self.a2)
        )

        self.a2_a = (exp1 * (exp2 + exp3 + exp4)) / (exp5)

    def update(self):
        self.update_acc1()

        self.update_acc2()

        self.update_angular()

        pass

    def update_pos(self):
        # print(self.a1, self.a2)
        self.x1 = self.r1 * math.sin(self.a1) + self.hook[0]
        self.y1 = self.r1 * math.cos(self.a1) + self.hook[1]
        self.x2 = self.x1 + self.r2 * math.sin(self.a2)
        self.y2 = self.y1 + self.r2 * math.cos(self.a2)
        self.pos = (self.x2 - self.m2 / 2, self.y2 + self.m2 / 2)

    def update_angular(self):
        self.a1_v += self.a1_a
        self.a2_v += self.a2_a

        self.a1 += self.a1_v
        self.a2 += self.a2_v

        pass
