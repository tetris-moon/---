import pygame
GRAY = (169,169,169)

class UserScreen:
    def __init__(self, screenx, screeny, width=100, height=200):
        self.screenx = screenx
        self.screeny = screeny
        self.width = width
        self.height = height

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, (self.screenx, self.screeny, self.width, self.height))

class Interface:
    def __init__(self):
        self.screens = [
            UserScreen(500, 10),
            UserScreen(735, 10),
            UserScreen(965, 10),
            UserScreen(500, 310),
            UserScreen(735, 310),
            UserScreen(965, 310)
        ]

    def draw(self, surface):
        for s in self.screens:
            s.draw(surface)