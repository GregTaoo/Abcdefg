import pygame

import includes
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Hud:

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface):
        pass


class MainHud(Hud):

    def __init__(self, player):
        self.player = player
        includes.COIN_IMAGE = pygame.transform.scale(pygame.image.load('assets/coin.png'), (20, 20))

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface):
        txt_surface = includes.FONT.render(
            f"World: {includes.CLIENT.dimension.name}; Pos: {self.player.x},{self.player.y}",
            True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
        txt_surface = includes.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(includes.COIN_IMAGE, (SCREEN_WIDTH - 10 - txt_surface.get_width() - 25, 8))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), 10))
        txt_surface = includes.FONT.render(f"ATK: {self.player.atk:.1f}, CRT: {self.player.crt * 100:.1f}%,"
                                           f" CRT DMG: {(self.player.crt_damage - 1) * 100:.1f}%", True, (255, 255, 255))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), SCREEN_HEIGHT - 30))
