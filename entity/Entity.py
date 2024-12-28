import random
from typing import Tuple

import pygame
from pygame import Rect

from render import Action, Renderer
import Config
from Config import BLOCK_SIZE, INTERACTION_DISTANCE
from ui.BattleUI import BattleUI


def render_dialog_at_absolute_pos(text, screen, pos, font: pygame.font):
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (pos[0] - text_rect.width // 2, pos[1])

    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(17, 17), border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(15, 15), border_radius=8)
    screen.blit(text_surface, text_rect.topleft)


class Entity:

    def __init__(self, name: str, pos: Tuple[int, int], renderer: Renderer, actions: list[Action] = None,
                 atk: float = 1.0, crt: float = 0.0, coins: int = 0, max_hp: float = 100, size: Tuple[int, int] = None):
        self.name = name
        self.x, self.y = pos
        self.renderer = renderer
        self.size = size or renderer.get_size()
        self.mirror = False
        self.hp = self.max_hp = max_hp
        self.fire_tick = 0
        self.atk = atk
        self.crt = crt
        self.moving = False
        self.crt_damage = 2.0
        self.coins = coins
        self.interact = False
        self.battle = True
        self.actions = actions if actions is not None else [Action.ATTACK_LEFT]

    def damage(self, damage: float):
        self.hp = max(0.0, self.hp - damage)

    def cure(self, cure: float):
        self.hp = min(self.max_hp, self.hp + cure)

    def move(self, direction: int, dimension, speed: int = 4):
        if not (1 <= direction <= 4):
            return

        self.moving = True
        # 获取移动方向的左右两格方块，并判断碰撞箱，如果该方块被标记为障碍物则无法通过
        block_x, block_y = dimension.get_block_index((self.x, self.y))
        block2_x, block2_y = block_x, block_y

        if direction == 1:
            self.x += speed
            self.mirror = False
            block_x += 1
            block2_x, block2_y = block_x, block_y + 1
        elif direction == 2:
            self.x -= speed
            self.mirror = True
            block_x -= 1
            block2_x, block2_y = block_x, block_y + 1
        elif direction == 3:
            self.y += speed
            block_y += 1
            block2_x, block2_y = block_x + 1, block_y
        elif direction == 4:
            self.y -= speed
            block_y -= 1
            block2_x, block2_y = block_x + 1, block_y

        # 地图边界
        limit_x, limit_y = dimension.get_render_size()
        self.x = max(0, min(limit_x - self.size[0], self.x))
        self.y = max(0, min(limit_y - self.size[1], self.y))

        # 障碍物处理
        rect = self.get_rect()
        if ((rect.colliderect(Rect(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) and
             dimension.get_block_from_index((block_x, block_y)).path) or
                (rect.colliderect(Rect(block2_x * BLOCK_SIZE, block2_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) and
                 dimension.get_block_from_index((block2_x, block2_y)).path)):
            if direction == 1:
                self.x -= self.x + self.size[0] - block_x * BLOCK_SIZE
            elif direction == 2:
                self.x += block_x * BLOCK_SIZE - self.x + BLOCK_SIZE
            elif direction == 3:
                self.y -= self.y + self.size[1] - block_y * BLOCK_SIZE
            elif direction == 4:
                self.y += block_y * BLOCK_SIZE - self.y + BLOCK_SIZE

    def tick(self, dimension, player=None):
        self.moving = False
        for i in {dimension.get_block_index(self.get_left_top_pos()),
                  dimension.get_block_index(self.get_left_bottom_pos()),
                  dimension.get_block_index(self.get_right_top_pos()),
                  dimension.get_block_index(self.get_right_bottom_pos())}:
            blk = dimension.get_block_from_index(i)
            if blk is not None:
                blk.on_entity(dimension.get_pos_from_index(i), self)
        if self.fire_tick > 0:
            self.fire_tick -= 1
            self.damage(1 / 12)

    def respawn_at_pos(self, pos: Tuple[int, int]):
        self.x, self.y = pos
        self.hp = self.max_hp
        self.fire_tick = 0

    def get_pos(self):
        return self.x, self.y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def get_left_top_pos(self):
        return self.x, self.y

    def get_left_bottom_pos(self):
        return self.x, self.y + self.size[1] - 1

    def get_right_top_pos(self):
        return self.x + self.size[0] - 1, self.y

    def get_right_bottom_pos(self):
        return self.x + self.size[0] - 1, self.y + self.size[1] - 1

    def is_nearby(self, entity, distance=INTERACTION_DISTANCE):
        return abs(self.x - entity.x) + abs(self.y - entity.y) < distance * BLOCK_SIZE

    def render(self, screen: pygame.Surface, camera: Tuple[int, int]):
        self.renderer.render(screen, (self.x - camera[0], self.y - camera[1]), self.mirror, not self.moving)
        if self.fire_tick > 0:
            Renderer.FIRE.render(screen, (self.x - camera[0], self.y - camera[1]))
        self.render_hp_bar(screen, (self.x - camera[0], self.y - camera[1] - 10), Config.FONT)

    def render_at_absolute_pos(self, screen: pygame.Surface, pos: Tuple[int, int], use_mirror=False, hp_bar=True):
        self.renderer.render(screen, pos, use_mirror, True)
        if hp_bar:
            self.render_hp_bar(screen, (pos[0], pos[1] - 10), Config.FONT)

    def render_hp_bar(self, screen: pygame.Surface, pos: Tuple[int, int], font=None):
        bar_width, bar_height = self.size[0], 5
        hp_rect = pygame.Rect(pos[0], pos[1], bar_width * min(1.0, self.hp / self.max_hp), bar_height)
        border_rect = pygame.Rect(pos[0], pos[1], bar_width, bar_height)
        pygame.draw.rect(screen, ((0, 255, 0) if self.hp >= 60 else (255, 255, 0)) if self.hp >= 30 else (255, 0, 0),
                         hp_rect)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 1)

        # hp_text = f"HP: {self.hp} / 100"
        # text_surface = font.render(hp_text, True, (255, 255, 255))
        # text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        # screen.blit(text_surface, text_rect)

    def on_interact(self, player):
        pass

    def on_battle(self, player):
        Config.CLIENT.open_ui(BattleUI(player, self))

    def can_interact(self):
        return self.interact

    def can_battle(self):
        return self.battle


class Monster(Entity):
    direction = 0

    def tick(self, dimension, player=None):
        super().tick(dimension, player)
        self.move(self.direction, dimension, 1)
        if random.randint(0, 450) == 0:
            if random.randint(0, 5) == 0:
                self.direction = random.randint(1, 4)
            else:
                self.direction = 0
