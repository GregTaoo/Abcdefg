import random

import pygame

import action
import entity
import includes
import particle
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

    def render(self, screen: pygame.Surface):
        self.blur_background(screen)
        for button in self.buttons:
            button.render(screen)

    def on_close(self):
        pass


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

    def render(self, screen: pygame.Surface):
        super().render(screen)
        pygame.draw.rect(screen, (255, 255, 255), self.input_box)
        txt_surface = includes.FONT.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))


class DeathUI(UI):

    def __init__(self):
        super().__init__('You Died')
        self.add_button(Button('你死了，点击重生', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50), (200, 50),
                               includes.FONT, (255, 255, 255), (0, 0, 0), lambda: includes.CLIENT.player_respawn()))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True


class SuccessUI(UI):

    def __init__(self, coins=0):
        super().__init__('You Won')
        self.coins = coins
        self.add_button(Button('胜利，点击继续', (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150), (200, 50),
                               includes.FONT, (255, 255, 255), (0, 0, 0), lambda: includes.CLIENT.close_ui()))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = includes.FONT.render('获得     x ' + str(self.coins), True, (255, 255, 255))
        screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(includes.COIN_IMAGE, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2 + 45,
                                          SCREEN_HEIGHT // 2 - 52))


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
        self.use_crt = False
        self.escaping_stage = 0
        self.attack_button = Button('普攻', (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 50), (100, 50),
                                    includes.FONT, (255, 255, 255), (0, 0, 0), self.round_start)
        self.add_button(self.attack_button)
        self.ultimate_button = Button('大招', (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 50), (100, 50),
                                      includes.FONT, (255, 255, 255), (0, 0, 0),
                                      lambda: self.round_start(action.Actions.ULTIMATE_RIGHT))
        self.add_button(self.ultimate_button)
        self.ultimate_button.set_active(self.player.ultimate_available())
        self.escape_button = Button('逃跑', (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 10), (100, 50),
                                    includes.FONT, (255, 255, 255), (0, 0, 0),
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
        self.use_crt = random.randint(0, 100) < self.player.crt * 100

    def render(self, screen: pygame.Surface):
        super().render(screen)
        if self.playing_action:
            target_poses, damage, text = self.action.get_current_pos()
            if self.half_round < self.round * 2:
                real_dmg = damage * self.player.atk * (2 if self.use_crt else 1)
                self.enemy.hp -= real_dmg
                if real_dmg != 0:
                    particle.add_particle(particle.DamageParticle(real_dmg, self.enemy_pos, 180, self.use_crt))
                    includes.SOUND_HIT.play()
                self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
                if target_poses is None:
                    self.player.render_at_absolute_pos(screen, self.player_pos)
                else:
                    for i in target_poses:
                        self.player.render_at_absolute_pos(screen, i)
                        if self.escaping_stage == 2 and text != '':
                            entity.render_dialog_at_absolute_pos(text, screen, (i[0] + self.player.size[0] // 2,
                                                                                i[1] - 40), includes.FONT)
            else:
                real_dmg = damage * self.enemy.atk * (2 if self.use_crt else 1)
                self.player.hp -= real_dmg
                if real_dmg != 0:
                    particle.add_particle(particle.DamageParticle(real_dmg, self.player_pos, 180, self.use_crt))
                    includes.SOUND_HIT.play()
                self.player.render_at_absolute_pos(screen, self.player_pos)
                if target_poses is None:
                    self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
                else:
                    for i in target_poses:
                        self.enemy.render_at_absolute_pos(screen, i)
        else:
            self.player.render_at_absolute_pos(screen, self.player_pos)
            self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
        txt_surface = includes.FONT.render(f"Round {self.round}", True, (0, 0, 0))
        screen.blit(txt_surface, (30, 30))
        particle.render_particles(screen, includes.MIDDLE_FONT)

    def tick(self, keys, events):
        super().tick(keys, events)
        if self.playing_action is None or (self.action is not None and self.action.is_end()):
            if self.player.hp <= 0:
                includes.SOUND_PLAYER_DEATH.play()
                includes.CLIENT.close_ui()
                includes.CLIENT.open_death_ui()
            elif self.enemy.hp <= 0:
                self.player.coins += self.enemy.coins
                includes.CLIENT.close_ui()
                includes.CLIENT.open_ui(SuccessUI(self.enemy.coins))
        if self.playing_action:
            if self.action.is_end():
                if self.half_round < self.round * 2:
                    self.action.reset()
                    self.action = action.Actions.ATTACK_LEFT
                    self.half_round += 1
                    self.use_crt = random.randint(0, 100) < self.enemy.crt * 100
                    if self.escaping_stage == 2:
                        includes.CLIENT.close_ui()
                else:
                    self.action.reset()
                    self.playing_action = False
                    self.set_buttons_active(True)
                    self.ultimate_button.set_active(self.player.ultimate_available())
                    if self.escaping_stage == 1:
                        self.escaping_stage = 2
                        self.round_start(action.Actions.ESCAPE_LEFT)
            self.action.tick()
        particle.tick_particles()
        return True

    def on_close(self):
        particle.remove_all_particles()


class TradeUI(UI):

    def __init__(self, player, npc):
        super().__init__('Trade')
        self.player = player
        self.buttons = []
        self.npc = npc
        cnt = 0
        for option in npc.trade_list:
            self.add_button(Button(option.name, (SCREEN_WIDTH // 2 - 50, 50 + cnt * 70), (100, 50),
                                   includes.FONT, (255, 255, 255), (0, 0, 0), option.on_trade))
            cnt += 1
        self.add_button(Button('离开', (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 10), (100, 50),
                               includes.FONT, (255, 255, 255), (0, 0, 0), includes.CLIENT.close_ui))

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def tick(self, keys, events):
        super().tick(keys, events)
        return True
