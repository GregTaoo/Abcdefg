import pygame

import action
import client
import entity
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
            button.render(screen)


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
        pygame.draw.rect(screen, (255, 255, 255), self.input_box)
        txt_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))


class DeathUI(UI):

    def __init__(self, font: pygame.font.Font):
        super().__init__('You Died')
        self.add_button(Button('你死了，点击重生', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50), (200, 50),
                               font, (255, 255, 255), (0, 0, 0), lambda: client.CLIENT.player_respawn()))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True


class SuccessUI(UI):

    def __init__(self, font: pygame.font.Font):
        super().__init__('You Won')
        self.add_button(Button('胜利，点击继续', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50), (200, 50),
                               font, (255, 255, 255), (0, 0, 0), lambda: client.CLIENT.close_ui()))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True


class BattleUI(UI):

    def __init__(self, player, enemy):
        super().__init__('Battle')
        for i in action.get_all_actions():
            i.reset()
        self.player = player
        self.enemy = enemy
        self.player_pos = (150, 200)
        self.enemy_pos = (SCREEN_WIDTH - 200, 200)
        self.round = 0
        self.half_round = 0
        self.playing_action = False
        self.action = None
        self.escaping_stage = 0
        self.attack_button = Button('普攻', (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 50), (100, 50),
                                    client.CLIENT.font, (255, 255, 255), (0, 0, 0), self.round_start)
        self.add_button(self.attack_button)
        self.ultimate_button = Button('大招', (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 50), (100, 50),
                                      client.CLIENT.font, (255, 255, 255), (0, 0, 0),
                                      lambda: self.round_start(action.Actions.ULTIMATE_RIGHT))
        self.add_button(self.ultimate_button)
        self.ultimate_button.set_active(self.player.ultimate_available())
        self.escape_button = Button('逃跑', (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 10), (100, 50),
                                    client.CLIENT.font, (255, 255, 255), (0, 0, 0),
                                    self.on_click_escape_button)
        self.add_button(self.escape_button)

    def on_click_escape_button(self):
        self.escaping_stage = 1
        self.round_start(action.Actions.EMPTY)

    def set_buttons_active(self, active):
        for button in self.buttons:
            button.set_active(active)

    def round_start(self, use_action=action.Actions.ATTACK_RIGHT):
        self.round += 1
        self.half_round += 1
        self.set_buttons_active(False)
        self.playing_action = True
        self.action = use_action
        if use_action == action.Actions.ATTACK_RIGHT:
            self.player.update_energy()
        elif use_action == action.Actions.ULTIMATE_RIGHT:
            self.player.reset_energy()

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        super().render(screen, font)
        if self.playing_action:
            target_poses, damage, text = self.action.get_current_pos()
            if self.half_round < self.round * 2:
                self.enemy.hp -= damage * self.player.atk
                self.enemy.render_at_absolute_pos(screen, self.enemy_pos, font)
                if target_poses is None:
                    self.player.render_at_absolute_pos(screen, self.player_pos, font)
                else:
                    for i in target_poses:
                        self.player.render_at_absolute_pos(screen, i, font)
                        if self.escaping_stage == 2 and text != '':
                            entity.render_dialog_at_absolute_pos(text, screen, (i[0] + self.player.size[0] // 2,
                                                                                i[1] - 40), font)
            else:
                self.player.hp -= damage * self.enemy.atk
                self.player.render_at_absolute_pos(screen, self.player_pos, font)
                if target_poses is None:
                    self.enemy.render_at_absolute_pos(screen, self.enemy_pos, font)
                else:
                    for i in target_poses:
                        self.enemy.render_at_absolute_pos(screen, i, font)
        else:
            self.player.render_at_absolute_pos(screen, self.player_pos, font)
            self.enemy.render_at_absolute_pos(screen, self.enemy_pos, font)
        txt_surface = font.render(f"Round {self.round}", True, (0, 0, 0))
        screen.blit(txt_surface, (30, 30))

    def tick(self, keys, events):
        super().tick(keys, events)
        if self.playing_action:
            if self.action.is_end():
                if self.half_round < self.round * 2:
                    self.action.reset()
                    self.action = action.Actions.ATTACK_LEFT
                    self.half_round += 1
                    if self.escaping_stage == 2:
                        client.CLIENT.close_ui()
                else:
                    self.action.reset()
                    self.playing_action = False
                    self.set_buttons_active(True)
                    self.ultimate_button.set_active(self.player.ultimate_available())
                    if self.escaping_stage == 1:
                        self.escaping_stage = 2
                        self.round_start(action.Actions.ESCAPE_LEFT)
            self.action.tick()
        if self.player.hp <= 0:
            client.CLIENT.open_death_ui()
        elif self.enemy.hp <= 0:
            client.CLIENT.open_ui(SuccessUI(client.CLIENT.font))
        return True
