import time

import pygame

import Config
import I18n
from UI.Hud import Hud
from UI.SelectLanguageUI import SelectLanguageUI
from UI.widget.ImageButton import ImageButton


class MainHud(Hud):

    def __init__(self, player):
        super().__init__()
        self.player = player
        Config.COIN_IMAGE = pygame.transform.scale(pygame.image.load('./assets/coin.png'), (20, 20))
        Config.LANGUAGE_IMAGE = pygame.transform.scale(pygame.image.load('./assets/language.png'), (20, 20))
        self.add_button(ImageButton(Config.LANGUAGE_IMAGE, (10, Config.SCREEN_HEIGHT - 30),
                                    lambda: Config.CLIENT.open_ui(SelectLanguageUI())))
        self.messages = []

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.FONT.render(I18n.text('player_pos').format(
            I18n.text(Config.CLIENT.dimension.name), self.player.x, self.player.y), True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
        txt_surface = Config.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(Config.COIN_IMAGE, (Config.SCREEN_WIDTH - 10 - txt_surface.get_width() - 25, 8))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH - 10 - txt_surface.get_width(), 10))
        txt_surface = Config.FONT.render(I18n.text('player_values').format(
            self.player.atk, self.player.crt * 100, (self.player.crt_damage - 1) * 100), True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH - 10 - txt_surface.get_width(), Config.SCREEN_HEIGHT - 30))

        current_time = time.time()
        y_offset = Config.SCREEN_HEIGHT - 50
        max_height = 300
        max_width = Config.SCREEN_WIDTH // 2
        messages_to_render = [(msg, ts) for msg, ts in self.messages if current_time - ts <= 20]

        for message, timestamp in messages_to_render:
            lines = []
            while message:
                for i in range(len(message)):
                    if Config.FONT.size(message[:i])[0] > max_width:
                        break
                else:
                    i = len(message)
                lines.append(message[:i])
                message = message[i:]
            for line in lines:  # Render each line from bottom to top
                txt_surface = Config.FONT.render(line, True, (255, 255, 255))
                y_offset -= txt_surface.get_height() + 5
                if y_offset < Config.SCREEN_HEIGHT - max_height:
                    return
                screen.blit(txt_surface, (10, y_offset))
