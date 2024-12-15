import pygame

import UI
import animation
from entity import Entity
from hud import MainHud

CLIENT = None


class Client:

    def __init__(self, screen, clock, font, player, dimension, camera):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.player = player
        self.dimension = dimension
        self.camera = camera
        self.current_ui = None
        self.current_hud = MainHud(player)
        self.entities = []

    def spawn_entity(self, entity):
        self.entities.append(entity)

    def open_ui(self, ui):
        self.current_ui = ui

    def close_ui(self):
        self.current_ui = None

    def open_death_ui(self):
        self.current_ui = UI.DeathUI(self.font)

    def player_respawn(self):
        self.player.respawn()
        self.close_ui()

    def tick(self, events):
        # 务必先渲染背景
        self.screen.fill((50, 50, 50))
        self.dimension.render(self.screen, self.camera)
        for i in self.entities:
            i.render(self.screen, self.camera, self.font)
        self.player.render(self.screen, self.camera, self.font)

        if self.current_ui is None:
            # 玩家移动
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:  # 向上移动
                self.player.move(4, self.dimension)
            if keys[pygame.K_s]:  # 向下移动
                self.player.move(3, self.dimension)
            if keys[pygame.K_a]:  # 向左移动
                self.player.move(2, self.dimension)
            if keys[pygame.K_d]:  # 向右移动
                self.player.move(1, self.dimension)
            if keys[pygame.K_f]:
                for i in self.entities:
                    if i.is_nearby(self.player):
                        self.current_ui = UI.InputTextUI()
            if keys[pygame.K_b]:
                for i in self.entities:
                    if i.is_nearby(self.player):
                        if i.name == '刁民':
                            iron_golem = Entity('Iron Golem', i.get_right_bottom_pos(),
                                                pygame.transform.scale(pygame.image.load("assets/iron_golem.png"),
                                                                       (50, 50)), atk=8)
                            self.spawn_entity(iron_golem)
                            self.current_ui = UI.BattleUI(self.player, iron_golem)
                        else:
                            self.current_ui = UI.BattleUI(self.player, i)

            # 踩岩浆扣血
            # for k in range(50):
            #     if (dimension.get_block_from_pos((player.x + k, player.y + k)) == Blocks.LAVA or
            #             dimension.get_block_from_pos((player.x + 50 - k, player.y + k)) == Blocks.LAVA):
            #         player.hp -= 1 / 90
            # player.hp = max(0, player.hp)
            self.player.tick(self.dimension)
            for i in animation.get_all_animations():
                i.tick()
            for i in self.entities:
                i.tick(self.dimension, self.player)

            # 更新摄像机位置
            self.camera = self.player.get_camera(self.dimension.get_render_size())

            self.current_hud.tick(keys, events)
            self.current_hud.render(self.screen, self.font)
        else:
            self.current_ui.render(self.screen, self.font)
            if not self.current_ui.tick(pygame.key.get_pressed(), events):
                self.close_ui()
