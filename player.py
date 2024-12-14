from typing import Tuple

import client
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import entity


class Player(entity.Entity):

    def __init__(self, name: str, respawn_pos: Tuple[int, int], pos: Tuple[int, int], image):
        super().__init__(name, pos, image)
        self.respawn_pos = respawn_pos

    def get_camera(self, limit: Tuple[int, int]):
        return self.x + self.size[0] // 2 - SCREEN_WIDTH // 2, self.y + self.size[1] // 2 - SCREEN_HEIGHT // 2
        # return (max(0, min(limit[0] - SCREEN_WIDTH, self.x + self.size[0] // 2 - SCREEN_WIDTH // 2)),
        #         max(0, min(limit[1] - SCREEN_HEIGHT, self.y + self.size[1] // 2 - SCREEN_HEIGHT // 2)))
        # 获得摄像头应该在的位置

    def respawn(self):
        self.respawn_at_pos(self.respawn_pos)

    def tick(self, dimension, player=None):
        super().tick(dimension, player)
        if self.hp <= 0:
            client.CLIENT.open_death_ui()
