import time

import pygame

import Config
import I18n
from ui.Hud import Hud
from ui.SelectLanguageUI import SelectLanguageUI
from ui.widget.ImageButton import ImageButton


class MainHud(Hud):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.add_button(ImageButton(Config.LANGUAGE_IMAGE, (10, Config.SCREEN_HEIGHT - 30),
                                    lambda: Config.CLIENT.open_ui(SelectLanguageUI())))
        self.messages = []
        self.display_hint = False
        self.hint = ''
        self.target_entity = None

    def add_message(self, message, color):
        self.messages.insert(0, (message, color, time.time()))

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.FONT.render(I18n.text('player_pos').format(
            I18n.text(Config.CLIENT.dimension.name), self.player.x, self.player.y), True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
        txt_surface = Config.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(Config.COIN_IMAGE, (Config.SCREEN_WIDTH - 10 - txt_surface.get_width() - 25, 8))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH - 10 - txt_surface.get_width(), 10))
        txt_surface = Config.FONT.render(I18n.text('player_values').format(
            self.player.atk, self.player.crt * 100, (self.player.crt_damage - 1) * 100, self.player.max_hp), True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH - 10 - txt_surface.get_width(), Config.SCREEN_HEIGHT - 30))

        if self.display_hint:
            y = Config.SCREEN_HEIGHT // 2 - 8 if self.target_entity.can_interact() ^ self.target_entity.can_battle()\
                else Config.SCREEN_HEIGHT // 2 - 25
            if self.target_entity.can_interact():
                txt_surface = Config.FONT.render(I18n.text('hint_interact').format(self.target_entity.name),
                                                 True, (150, 255, 150))
                screen.blit(txt_surface,
                            (Config.SCREEN_WIDTH - txt_surface.get_width(), y))
                y += 25
            if self.target_entity.can_battle():
                txt_surface = Config.FONT.render(I18n.text('hint_battle').format(self.target_entity.name),
                                                 True, (150, 255, 150))
                screen.blit(txt_surface,
                            (Config.SCREEN_WIDTH - txt_surface.get_width(), y))

        if len(self.hint) > 0:
            txt_surface = Config.FONT.render(self.hint, True, (255, 0, 0))
            screen.blit(txt_surface, ((Config.SCREEN_WIDTH - txt_surface.get_width()) // 2, Config.SCREEN_HEIGHT - 150))
            self.hint = ''

        current_time = time.time()
        y_offset = Config.SCREEN_HEIGHT - 50
        lines_cnt = 0
        for message, color, timestamp in self.messages:
            if timestamp > current_time - 20:
                if len(message.get().strip()) > 0:
                    txt_surface = Config.FONT.render(message.get().strip(), True, color)
                    screen.blit(txt_surface, (10, y_offset))
                    y_offset -= 20
                    lines_cnt += 1
            if lines_cnt > 10:
                break

