import time

import pygame

import UI
import config
import i18n
from button import ImageButton
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Hud:

    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def tick(self, keys, events):
        for button in self.buttons:
            button.tick(events)

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            button.render(screen)


class MainHud(Hud):

    def __init__(self, player):
        super().__init__()
        self.player = player
        config.COIN_IMAGE = pygame.transform.scale(pygame.image.load('assets/coin.png'), (20, 20))
        config.LANGUAGE_IMAGE = pygame.transform.scale(pygame.image.load('assets/language.png'), (20, 20))
        self.add_button(ImageButton(config.LANGUAGE_IMAGE, (10, SCREEN_HEIGHT - 30),
                                    lambda: config.CLIENT.open_ui(UI.SelectLanguageUI())))
        self.messages = []

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = config.FONT.render(i18n.text('player_pos').format(
            i18n.text(config.CLIENT.dimension.name), self.player.x, self.player.y), True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
        txt_surface = config.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(config.COIN_IMAGE, (SCREEN_WIDTH - 10 - txt_surface.get_width() - 25, 8))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), 10))
        txt_surface = config.FONT.render(i18n.text('player_values').format(
            self.player.atk, self.player.crt * 100, (self.player.crt_damage - 1) * 100), True, (255, 255, 255))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), SCREEN_HEIGHT - 30))

        current_time = time.time()
        y_offset = SCREEN_HEIGHT - 50  # Start from the bottom
        max_height = 300  # Maximum height to render messages
        max_width = SCREEN_WIDTH // 2  # Maximum width for messages
        messages_to_render = [(msg, ts) for msg, ts in self.messages if current_time - ts <= 20]

        for message, timestamp in messages_to_render:
            lines = []
            while message:
                for i in range(len(message)):
                    if config.FONT.size(message[:i])[0] > max_width:
                        break
                else:
                    i = len(message)
                lines.append(message[:i])
                message = message[i:]
            for line in lines:  # Render each line from bottom to top
                txt_surface = config.FONT.render(line, True, (255, 255, 255))
                y_offset -= txt_surface.get_height() + 5
                if y_offset < SCREEN_HEIGHT - max_height:
                    return
                screen.blit(txt_surface, (10, y_offset))
