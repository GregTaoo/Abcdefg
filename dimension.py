from typing import Tuple

import pygame

from block import Block
import random

from config import BLOCK_SIZE


class Dimension:

    def __init__(self, width: int, height: int, blocks: list[list[Block]]):
        self.width = width
        self.height = height
        self.blocks = blocks

    def get_render_size(self):
        return self.width * BLOCK_SIZE, self.height * BLOCK_SIZE

    @staticmethod
    def generate_map(width: int, height: int, blocks: list[Block], weights: list[int]):
        return [random.choices(blocks, weights, k=height) for _ in range(width)]

    def render(self, screen: pygame.Surface, camera_pos: Tuple[int, int]):
        for x in range(self.width):
            for y in range(self.height):
                self.blocks[x][y].render(screen, (x * BLOCK_SIZE - camera_pos[0], y * BLOCK_SIZE - camera_pos[1]))

    @staticmethod
    def get_block_index(pos: Tuple[int, int]):
        return pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE

    def get_block_from_pos(self, pos: Tuple[int, int]):
        x, y = self.get_block_index(pos)
        return self.blocks[x][y]

    def get_block_from_index(self, xy: Tuple[int, int]):
        return self.blocks[xy[0]][xy[1]]
