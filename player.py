from typing import Tuple

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from entity import Entity


class Player(Entity):

    def get_camera(self, limit: Tuple[int, int]):
        return (max(0, min(limit[0] - SCREEN_WIDTH, self.x + self.size[0] // 2 - SCREEN_WIDTH // 2)),
                max(0, min(limit[1] - SCREEN_HEIGHT, self.y + self.size[1] // 2 - SCREEN_HEIGHT // 2)))
        # 获得摄像头应该在的位置
