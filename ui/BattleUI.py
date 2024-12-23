import random

import pygame

import Config
from entity import Entity
from render import Particle, Action
import I18n
from ui.UI import UI
from ui.BattleSuccessUI import BattleSuccessUI
from ui.widget.ClassicButton import ClassicButton


class BattleUI(UI):

    def __init__(self, player, enemy):
        super().__init__()
        for i in Action.ACTIONS:
            i.reset()
        self.player = player
        self.enemy = enemy
        self.player_pos = (150, 200)
        self.enemy_pos = (Config.SCREEN_WIDTH - 200, 200)
        self.round = 0
        self.half_round = 0
        self.playing_action = False
        self.action = None
        self.use_crt = False
        self.escaping_stage = 0
        self.attack_button = ClassicButton(I18n.text('common_attack'),
                                           (Config.SCREEN_WIDTH // 2 - 150, Config.SCREEN_HEIGHT // 2 + 50),
                                           (95, 50), (255, 255, 255), (0, 0, 0), self.round_start)
        self.add_button(self.attack_button)
        self.ultimate_button = ClassicButton(I18n.text('ultimate_attack'),
                                             (Config.SCREEN_WIDTH // 2 - 50, Config.SCREEN_HEIGHT // 2 + 50),
                                             (95, 50), (255, 255, 255), (0, 0, 0),
                                             lambda: self.round_start(Action.ULTIMATE_RIGHT))
        self.add_button(self.ultimate_button)
        self.ultimate_button.set_active(self.player.ultimate_available())
        self.escape_button = ClassicButton(I18n.text('escape'),
                                           (Config.SCREEN_WIDTH // 2 + 50, Config.SCREEN_HEIGHT // 2 + 50),
                                           (95, 50), (255, 255, 255), (0, 0, 0),
                                           self.on_click_escape_button)
        self.add_button(self.escape_button)

    def on_click_escape_button(self):
        self.escaping_stage = 1
        self.round_start(Action.EMPTY)

    def set_buttons_active(self, active):
        for button in self.buttons:
            button.set_active(active)

    def round_start(self, use_action=Action.ATTACK_RIGHT):
        self.round += 1
        self.half_round += 1
        self.set_buttons_active(False)
        self.playing_action = True
        self.action = use_action
        if use_action == Action.ATTACK_RIGHT:
            self.player.update_energy()
        elif use_action == Action.ULTIMATE_RIGHT:
            self.player.reset_energy()
        self.use_crt = random.randint(0, 100) < self.player.crt * 100

    def render(self, screen: pygame.Surface):
        super().render(screen)
        if self.playing_action:
            target_poses, damage, text, sounds = self.action.get_current_pos()
            for sound in sounds:
                Config.SOUNDS[sound].play()
            if self.half_round < self.round * 2:
                real_dmg = damage * self.player.atk * (self.player.crt_damage if self.use_crt else 1)
                self.enemy.damage(real_dmg)
                if real_dmg != 0:
                    Particle.add_particle(Particle.DamageParticle(real_dmg, self.enemy_pos, 180, self.use_crt))
                self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
                if target_poses is None:
                    self.player.render_at_absolute_pos(screen, self.player_pos)
                else:
                    if text != '':
                        text = I18n.text(text).get() or ''
                    for i in target_poses:
                        self.player.render_at_absolute_pos(screen, i)
                        if text != '':
                            Entity.render_dialog_at_absolute_pos(text, screen, (i[0] + self.player.size[0] // 2,
                                                                                i[1] - 40), Config.FONT)
            else:
                real_dmg = damage * self.enemy.atk * (self.enemy.crt_damage if self.use_crt else 1)
                self.player.damage(real_dmg)
                if real_dmg != 0:
                    Particle.add_particle(Particle.DamageParticle(real_dmg, self.player_pos, 180, self.use_crt))
                    if self.player.hp <= 0:
                        Config.SOUNDS['player_death'].play()
                self.player.render_at_absolute_pos(screen, self.player_pos)
                if target_poses is None:
                    self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
                else:
                    for i in target_poses:
                        self.enemy.render_at_absolute_pos(screen, i)
        else:
            self.player.render_at_absolute_pos(screen, self.player_pos)
            self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
        txt_surface = Config.FONT.render(I18n.text('rounds').format(self.round), True, (255, 255, 255))
        screen.blit(txt_surface, (30, 30))
        Particle.render_particles(screen, Config.MIDDLE_FONT)

    def tick(self, keys, events):
        super().tick(keys, events)
        if self.playing_action is None or (self.action is not None and self.action.is_end()):
            if self.player.hp <= 0:
                Config.CLIENT.close_ui()
                Config.CLIENT.open_death_ui()
            elif self.enemy.hp <= 0:
                self.player.coins += self.enemy.coins
                Config.CLIENT.close_ui()
                Config.CLIENT.open_ui(BattleSuccessUI(self.enemy.name, self.enemy.coins))
                Config.SOUNDS['victory'].play()
        if self.playing_action:
            if self.action.is_end():
                if self.half_round < self.round * 2:
                    self.action.reset()
                    self.action = Action.ATTACK_LEFT
                    self.half_round += 1
                    self.use_crt = random.randint(0, 100) < self.enemy.crt * 100
                    if self.escaping_stage == 2:
                        Config.CLIENT.close_ui()
                else:
                    self.action.reset()
                    self.playing_action = False
                    self.set_buttons_active(True)
                    self.ultimate_button.set_active(self.player.ultimate_available())
                    if self.escaping_stage == 1:
                        self.escaping_stage = 2
                        self.round_start(Action.ESCAPE_LEFT)
            self.action.tick()
        Particle.tick_particles()
        return True

    def on_close(self):
        Particle.remove_all_particles()

