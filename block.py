from typing import Tuple

import pygame

import animation
import player
import worlds
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


class PortalBlock(Block):

    def __init__(self, name: str, image, is_animation=False, obstacle=False, target_dimension=None):
        super().__init__(name, image, is_animation, obstacle)
        self.target_dimension = target_dimension

    def on_entity(self, block_pos: Tuple[int, int], mob):
        if isinstance(mob, player.Player):
            mob.teleport(self.target_dimension, block_pos)


class Blocks:

    @staticmethod
    def create_image(file: str):
        return pygame.transform.scale(pygame.image.load("assets/" + file), (BLOCK_SIZE, BLOCK_SIZE))

    GRASS_BLOCK = Block("grass_block", create_image("grass_block.png"))
    STONE = Block("stone", create_image("stone.png"), obstacle=True)
    LAVA = LavaBlock("lava", animation.Animations.LAVA, True)
    WATER = WaterBlock("water", animation.Animations.WATER, True)
    NETHER_PORTAL = PortalBlock("nether_portal", animation.Animations.NETHER_PORTAL, True,
                                target_dimension='the_end')
    NETHER_BACK_PORTAL = PortalBlock("nether_portal", animation.Animations.NETHER_PORTAL, True,
                                     target_dimension='the_world')
    END_STONE = Block("end_stone", create_image("end_stone.png"))
