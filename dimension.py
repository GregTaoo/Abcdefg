from typing import Tuple

import pygame

import block
import random

from config import BLOCK_SIZE


class Dimension:

    def __init__(self, width: int, height: int, blocks: list[list[block.Block]]):
        self.width = width
        self.height = height
        self.blocks = blocks

    def get_render_size(self):
        return self.width * BLOCK_SIZE, self.height * BLOCK_SIZE

    @staticmethod
    def generate_map(width: int, height: int, blocks: list[block.Block], weights: list[int]):
        return [random.choices(blocks, weights, k=height) for _ in range(width)]
        # 最简单的地图生成器，可自定义权重

    def render(self, screen: pygame.Surface, camera: Tuple[int, int]):
        for x in range(self.width):
            for y in range(self.height):
                self.blocks[x][y].render(screen, (x * BLOCK_SIZE - camera[0], y * BLOCK_SIZE - camera[1]))
                # 并没有优化

    @staticmethod
    def get_block_index(pos: Tuple[int, int]):
        return pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE
        # 取整，根据实际位置获得方块坐标

    @staticmethod
    def get_pos_from_index(i: Tuple[int, int]):
        return i[0] * BLOCK_SIZE, i[1] * BLOCK_SIZE

    def get_block_from_pos(self, pos: Tuple[int, int]):
        x, y = self.get_block_index(pos)
        return self.blocks[x][y]
        # 根据实际位置获得方块

    def get_block_from_index(self, xy: Tuple[int, int]):
        if 0 <= xy[0] < self.width and 0 <= xy[1] < self.height:
            return self.blocks[xy[0]][xy[1]]
        else:
            return None
        # 根据方块坐标获得方块
