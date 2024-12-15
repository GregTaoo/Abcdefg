from typing import Tuple

import pygame

import animation
from config import BLOCK_SIZE


class Block:

    def __init__(self, name: str, image, is_animation=False, obstacle=False):
        self.name = name
        self.image = image
        self.is_animation = is_animation
        self.path = obstacle

    @staticmethod
    def get_rect(block_pos: Tuple[int, int]):
        return pygame.Rect(block_pos, (BLOCK_SIZE, BLOCK_SIZE))

    def on_entity(self, block_pos: Tuple[int, int], mob):
        pass

    def render(self, screen: pygame.Surface, pos: Tuple[int, int]):
        if self.is_animation:
            self.image.render(screen, pos)
        else:
            screen.blit(self.image, pos)


class LavaBlock(Block):

    def on_entity(self, block_pos: Tuple[int, int], mob):
        mob.fire_tick = 450
        overlap = mob.get_rect().clip(self.get_rect(block_pos))
        mob.hp -= (overlap.width * overlap.height) / BLOCK_SIZE ** 2 / 3
        mob.hp = max(0, mob.hp)


class WaterBlock(Block):

    def on_entity(self, block_pos: Tuple[int, int], mob):
        mob.fire_tick = 0
        overlap = mob.get_rect().clip(self.get_rect(block_pos))
        mob.hp += (overlap.width * overlap.height) / BLOCK_SIZE ** 2 / 5
        mob.hp = min(100, mob.hp)


class Blocks:

    @staticmethod
    def create_image(file: str):
        return pygame.transform.scale(pygame.image.load("assets/" + file), (BLOCK_SIZE, BLOCK_SIZE))

    GRASS_BLOCK = Block("grass_block", create_image("grass_block.png"))
    STONE = Block("stone", create_image("stone.png"), obstacle=True)
    LAVA = LavaBlock("lava", animation.Animations.LAVA, True)
    WATER = WaterBlock("water", animation.Animations.WATER, True)

