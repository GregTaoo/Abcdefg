from typing import Tuple


import action
import config
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import entity


class Player(entity.Entity):

    def __init__(self, name: str, respawn_pos: Tuple[int, int], pos: Tuple[int, int], image):
        super().__init__(name, pos, image, actions=[
            action.Actions.ATTACK_RIGHT, action.Actions.ULTIMATE_RIGHT
        ], crt=0.5)
        self.dialog_timer = 0
        self.respawn_pos = respawn_pos
        self.energy = 3
        self.souls = 1
        self.skill = 0
        # 0: NONE, 1: 天谴, 2: 吸血

    def get_camera(self, limit: Tuple[int, int]):
        return self.x + self.size[0] // 2 - SCREEN_WIDTH // 2, self.y + self.size[1] // 2 - SCREEN_HEIGHT // 2
        # return (max(0, min(limit[0] - SCREEN_WIDTH, self.x + self.size[0] // 2 - SCREEN_WIDTH // 2)),
        #         max(0, min(limit[1] - SCREEN_HEIGHT, self.y + self.size[1] // 2 - SCREEN_HEIGHT // 2)))
        # 获得摄像头应该在的位置

    def respawn(self):
        self.reset_energy()
        self.teleport('the_world', self.respawn_pos)
        self.respawn_at_pos(self.respawn_pos)

    def teleport(self, dimension_str, pos: Tuple[int, int]):
        dimension = config.WORLDS[dimension_str]
        if dimension is None:
            return
        config.CLIENT.set_dimension(dimension)
        self.x, self.y = pos

    def update_energy(self):
        self.energy = min(self.energy + 1, 3)

    def reset_energy(self):
        self.energy = 0

    def ultimate_available(self):
        return self.energy == 3

    def tick_second(self, dimension, player=None):
        if self.fire_tick > 0:
            config.SOUNDS['hit'].play()
