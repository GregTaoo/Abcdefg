import pygame


class Hud:

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        pass


class MainHud(Hud):

    def __init__(self, player):
        self.player = player

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        txt_surface = font.render(f"Pos: {self.player.x},{self.player.y}", True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
