from typing import Tuple

import pygame
from pygame import Rect

from config import BLOCK_SIZE, INTERACTION_DISTANCE
from dimension import Dimension


class Entity:

    def __init__(self, name: str, pos: Tuple[int, int], image: pygame.Surface):
        self.name = name
        self.x, self.y = pos
        self.image, self.image_mirrored = image, pygame.transform.flip(image, True, False)
        self.size = image.get_size()
        self.mirror = False
        self.hp = 100

    def move(self, direction, dimension: Dimension, speed=4):
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
        rect = self.image.get_rect()
        rect.x, rect.y = self.x, self.y
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

    def is_nearby(self, entity):
        return abs(self.x - entity.x) + abs(self.y - entity.y) < INTERACTION_DISTANCE * BLOCK_SIZE

    def render(self, screen: pygame.Surface, camera: Tuple[int, int]):
        screen.blit(self.image_mirrored if self.mirror else self.image, (self.x - camera[0], self.y - camera[1]))
