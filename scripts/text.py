import pygame


class Text:
    def __init__(
        self, text, pos, data="", size=20, font="comicsans", color=(255, 255, 255)
    ):
        pygame.font.init()
        self.text = text
        self.pos = pos
        self.color = color

        self.font = pygame.font.SysFont(font, size)

        self.update(data)

    def update(self, data=""):
        self.str = self.text + " : " + data

    def render(self, surf):
        myTxt = self.font.render(self.str, 1, self.color)
        surf.blit(myTxt, self.pos)

        pass
