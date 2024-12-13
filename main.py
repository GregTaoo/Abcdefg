import pygame
import sys

from block import Blocks
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from dimension import Dimension
from player import Player


def main():
    pygame.init()
    pygame.display.set_caption("Minecraft (FAKE)")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player("Steve", (100, 100),
                    pygame.transform.scale(pygame.image.load("assets/player.png"), (20, 20)))
    dimension = Dimension(60, 60, Dimension.generate_map(60, 60, [
        Blocks.GRASS_BLOCK, Blocks.LAVA
    ], [4, 1]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # 向上移动
            player.move(4, dimension)
        if keys[pygame.K_s]:  # 向下移动
            player.move(3, dimension)
        if keys[pygame.K_a]:  # 向左移动
            player.move(2, dimension)
        if keys[pygame.K_d]:  # 向右移动
            player.move(1, dimension)

        # 更新摄像机位置
        camera = player.get_camera(dimension.get_render_size())

        dimension.render(screen, camera)

        player.render(screen, camera)

        pygame.display.flip()
        clock.tick(90)


if __name__ == "__main__":
    main()
