import pygame

import action
import client
from button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class UI:

    def __init__(self, title: str):
        self.title = title
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def tick(self, keys, events):
        for button in self.buttons:
            button.tick(events)
        return False

    @staticmethod
    # Copilot 写的
    def blur_background(screen: pygame.Surface):
        surface = pygame.Surface(screen.get_size())
        surface.blit(screen, (0, 0))
        for _ in range(5):  # Adjust the range for more/less blur
            surface = pygame.transform.smoothscale(surface, (surface.get_width() // 2, surface.get_height() // 2))
            surface = pygame.transform.smoothscale(surface, screen.get_size())
        screen.blit(surface, (0, 0))

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        self.blur_background(screen)
        for button in self.buttons:
            button.draw(screen)


class InputTextUI(UI):

    def __init__(self):
        super().__init__('Input Text')
        self.input_box = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        self.text = ''

    def tick(self, keys, events):
        super().tick(keys, events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return False
                else:
                    self.text += event.unicode
        return True

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        super().render(screen, font)
        txt_surface = font.render(self.text, True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), self.input_box)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))


class DeathUI(UI):

    def __init__(self, font: pygame.font.Font):
        super().__init__('You Died')
        self.add_button(Button('你死了，点击重生', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50), (200, 50),
                               font, (255, 255, 255), (0, 0, 0), lambda: client.CLIENT.player_respawn()))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True


class BattleUI(UI):

    def __init__(self, player, enemy):
        super().__init__('Battle')
        self.player = player
        self.enemy = enemy
        self.player_pos = (200, 200)
        self.enemy_pos = (SCREEN_WIDTH - 200, 200)
        self.round = 0
        self.half_round = 0
        self.playing_action = False
        self.action = None
        self.attack_button = Button('攻击', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50), (200, 50),
                                    client.CLIENT.font, (255, 255, 255), (0, 0, 0), self.round_start)
        self.add_button(self.attack_button)

    def round_start(self):
        self.round += 1
        self.half_round += 1
        self.attack_button.set_active(False)
        self.playing_action = True
        self.action = action.Actions.ATTACK_RIGHT

    def attack(self):
        self.enemy.hp -= 10
        if self.enemy.hp <= 0:
            client.CLIENT.entities.remove(self.enemy)
            client.CLIENT.close_ui()

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        super().render(screen, font)
        if self.playing_action:
            if self.half_round < self.round * 2:
                self.enemy.render_at_absolute_pos(screen, self.enemy_pos, font)
                print(self.action.get_current_pos())
                self.player.render_at_absolute_pos(screen, self.action.get_current_pos(), font)
            else:
                self.player.render_at_absolute_pos(screen, self.player_pos, font)
                self.enemy.render_at_absolute_pos(screen, self.action.get_current_pos(), font)
        else:
            self.player.render_at_absolute_pos(screen, self.player_pos, font)
            self.enemy.render_at_absolute_pos(screen, self.enemy_pos, font)

    def tick(self, keys, events):
        super().tick(keys, events)
        if self.playing_action:
            if self.action.is_end():
                if self.half_round < self.round * 2:
                    self.enemy.hp -= 10
                    self.action.reset()
                    self.action = action.Actions.ATTACK_LEFT
                    self.half_round += 1
                else:
                    self.player.hp -= 10
                    self.action.reset()
                    self.playing_action = False
                    self.attack_button.set_active(True)
            self.action.tick()
        if self.player.hp <= 0:
            client.CLIENT.open_death_ui()
        elif self.enemy.hp <= 0:
            client.CLIENT.close_ui()
        return True
