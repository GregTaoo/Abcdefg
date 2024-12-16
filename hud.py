import pygame

import client
import includes
from config import SCREEN_WIDTH


class Hud:

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        pass


class MainHud(Hud):

    def __init__(self, player):
        self.player = player
        includes.COIN_IMAGE = pygame.transform.scale(pygame.image.load('assets/coin.png'), (20, 20))

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        txt_surface = font.render(f"World: {client.CLIENT.dimension.name}; Pos: {self.player.x},{self.player.y}",
                                  True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
        txt_surface = font.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(includes.COIN_IMAGE, (SCREEN_WIDTH - 10 - txt_surface.get_width() - 25, 8))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), 10))
