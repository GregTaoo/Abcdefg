import random

import pygame

import UI
import animation
import worlds
from block import Blocks
from config import MAP_WIDTH, MAP_HEIGHT
from dimension import Dimension
from entity import Entity
from hud import MainHud

CLIENT = None


def generate_the_world():
    mp = Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [
        Blocks.GRASS_BLOCK, Blocks.LAVA, Blocks.STONE, Blocks.WATER
    ], [150, 2, 2, 1])
    mp[random.randint(0, MAP_WIDTH - 1)][random.randint(0, MAP_HEIGHT - 1)] = Blocks.NETHER_PORTAL
    # mp[10][10] = Blocks.NETHER_PORTAL
    return mp


def generate_the_end():
    mp = Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [Blocks.END_STONE], [1])
    mp[MAP_WIDTH // 2][MAP_HEIGHT // 2] = Blocks.NETHER_BACK_PORTAL
    return mp


class Client:

    def __init__(self, screen, clock, font, player, dimension):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.player = player
        self.current_ui = None
        self.current_hud = MainHud(player)
        worlds.WORLDS.append(Dimension('the_world', MAP_WIDTH, MAP_HEIGHT, generate_the_world()))
        worlds.WORLDS.append(Dimension('the_end', MAP_WIDTH, MAP_HEIGHT, generate_the_end()))
        self.dimension = worlds.get_world(dimension)
        self.camera = self.player.get_camera(self.dimension.get_render_size())

    def spawn_entity(self, entity):
        self.dimension.spawn_entity(entity)

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
        for i in self.dimension.entities:
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
                if self.dimension.nearest_entity(self.player.get_pos()).is_nearby(self.player):
                    self.current_ui = UI.InputTextUI()
            if keys[pygame.K_b]:
                nearest = self.dimension.nearest_entity(self.player.get_pos())
                if nearest.is_nearby(self.player):
                    if nearest.name == '刁民':
                        iron_golem = Entity('Iron Golem', nearest.get_right_bottom_pos(),
                                            pygame.transform.scale(pygame.image.load("assets/iron_golem.png"),
                                                                   (50, 50)), atk=8)
                        self.spawn_entity(iron_golem)
                        self.current_ui = UI.BattleUI(self.player, iron_golem)
                    else:
                        self.current_ui = UI.BattleUI(self.player, nearest)

            # 踩岩浆扣血
            # for k in range(50):
            #     if (dimension.get_block_from_pos((player.x + k, player.y + k)) == Blocks.LAVA or
            #             dimension.get_block_from_pos((player.x + 50 - k, player.y + k)) == Blocks.LAVA):
            #         player.hp -= 1 / 90
            # player.hp = max(0, player.hp)
            self.player.tick(self.dimension)
            for i in animation.get_all_animations():
                i.tick()
            for i in self.dimension.entities:
                i.tick(self.dimension, self.player)

            # 更新摄像机位置
            self.camera = self.player.get_camera(self.dimension.get_render_size())

            self.current_hud.tick(keys, events)
            self.current_hud.render(self.screen, self.font)
        else:
            self.current_ui.render(self.screen, self.font)
            if not self.current_ui.tick(pygame.key.get_pressed(), events):
                self.close_ui()
