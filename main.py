# Double Pendulum

import pygame
import sys
from random import random, randint, choice
from scripts.trail import draw_circle, Trail
from scripts.pendulum import Pendulum, Control_Pendulum
from scripts.text import Text
from scripts.const import RENDER_SCALE, WIDTH, HEIGHT, WHITE, BLUE, RED, BG_COLOR


# from scripts.recorder import pygame_screen_recorder as Recorder

print("Starting Game")

# right click - second blot
# left click -- first blob
# angle mass length
#   a    w     d


class Mouse:
    def __init__(self, radius=5, color=WHITE):
        self.radius = radius
        self.pos = self.get_pos()
        self.prev_pos = self.pos
        self.circle = draw_circle(radius, color)

    def update(self):
        self.prev_pos = self.pos
        self.pos = self.get_pos()

    def render(self, surf):
        surf.blit(self.circle, self.pos)

    def get_pos(self):
        mouse_pos = pygame.mouse.get_pos()

        return (
            mouse_pos[0] / RENDER_SCALE - self.radius,
            mouse_pos[1] / RENDER_SCALE - self.radius,
        )


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Double Pendulum")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # display is half of screen size
        self.display = pygame.Surface((WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE))
        self.clock = pygame.time.Clock()

        self.particles = []
        self.circles = []
        for i in range(100):
            self.circles.append(draw_circle(random() * 0.5 + 0.3, (255, 255, 255)))
        self.cursor = Mouse(5)
        self.trail = Trail(self.cursor, 3)

        self.pendulum = Pendulum((WIDTH / RENDER_SCALE / 2, 100))
        self.pen_trial = Trail(self.pendulum, 0.2, True)
        self.pen_control = Control_Pendulum(self.pendulum)

        self.show_history = False

        self.show_info = True

        self.a_pressed = False
        self.w_pressed = False
        self.d_pressed = False

        # self.recorder = Recorder("test.gif")

        # self.is_recording = False

    def run(self):
        running = True
        while running:
            # For Background ------------------------------------------------------|
            self.display.fill(BG_COLOR)

            # For Trail -----------------------------------------------------------|
            self.pen_trial.update()
            self.pen_trial.render(self.display)

            self.trail.update()
            self.trail.render(self.display)

            # For Pendulum --------------------------------------------------------|
            if not (self.a_pressed):
                self.pendulum.update()
            self.pendulum.render(self.display)

            # For Cursor ----------------------------------------------------------|
            self.cursor.update()
            self.cursor.render(self.display)

            # For Text  -----------------------------------------------------------|
            if self.show_info:
                self.pen_control.update_text()
                self.pen_control.render_text(self.display)

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                # Quit Event ------------------------------------------------------|
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                    exit()

                # KeyDown Event ---------------------------------------------------|
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        sys.exit()
                        exit()
                    # if event.key == pygame.K_r:
                    #     self.is_recording = not self.is_recording
                    # if event.key == pygame.K_s:
                    #     self.recorder.save()
                    #     self.is_recording = False
                    if event.key == pygame.K_z:
                        self.pendulum = Pendulum((WIDTH / RENDER_SCALE / 2, 100))
                        self.pen_trial = Trail(self.pendulum, 0.2, True)
                        self.pen_control = Control_Pendulum(self.pendulum)
                    if event.key == pygame.K_c:
                        self.pen_trial.clear_history()

                    if event.key == pygame.K_x:
                        self.pen_trial.history = not self.pen_trial.history

                    if event.key == pygame.K_t:
                        self.show_info = not self.show_info

                    if event.key == pygame.K_a:
                        self.a_pressed = True
                    if event.key == pygame.K_w:
                        self.w_pressed = True
                    if event.key == pygame.K_d:
                        self.d_pressed = True

                # MouseDown Event -------------------------------------------------|
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left Click
                        self.pen_control.blob = 1

                    if event.button == 3:  # Right Click
                        self.pen_control.blob = 2

                    if event.button == 4:  # Up Mouse Scroll
                        if self.a_pressed:
                            self.pen_control.update_angle(0.1)
                        if self.w_pressed:
                            self.pen_control.update_mass(1)

                        if self.d_pressed:
                            self.pen_control.update_length(1)

                    if event.button == 5:  # Dwon Mouse Scroll
                        if self.a_pressed:
                            self.pen_control.update_angle(-0.1)
                        if self.w_pressed:
                            self.pen_control.update_mass(-1)

                        if self.d_pressed:
                            self.pen_control.update_length(-1)
                        pass
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.a_pressed = False
                    if event.key == pygame.K_w:
                        self.w_pressed = False
                    if event.key == pygame.K_d:
                        self.d_pressed = False
            # Recorder ------------------------------------------------------------|
            # if self.is_recording:
            #     self.recorder.click(self.screen)
            #     self.display.blit(self.cursor.circle, (WIDTH - 5, HEIGHT - 5))
            # Rendering Screen ----------------------------------------------------|
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)

        # Quit --------------------------------------------------------------------|
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
sys.exit()
exit()
pygame.quit()
print("Game Over")
