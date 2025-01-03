import pygame

import I18n
from render import Renderer


class ParticleManager:

    particles = []

    def tick(self):
        for i in self.particles:
            i.tick()
            if i.is_end():
                self.particles.remove(i)
                del i

    def render(self, screen, font: pygame.font.Font):
        for i in self.particles:
            i.render(screen, font)

    def add(self, particle):
        self.particles.append(particle)

    def clear(self):
        self.particles.clear()


UI_PARTICLES = ParticleManager()
ENV_PARTICLES = ParticleManager()


class Particle:

    def __init__(self, pos, duration):
        self.pos = pos
        self.duration = duration
        self.timer = 0

    def tick(self):
        self.timer = min(self.timer + 1, self.duration)

    def is_end(self):
        return self.timer >= self.duration

    def render(self, screen, font: pygame.font.Font):
        pass


class DamageParticle(Particle):

    def __init__(self, damage, pos, duration, is_crt=False, color=(255, 0, 0)):
        super().__init__(pos, duration)
        self.damage = damage
        self.color = color
        self.alpha = 255
        self.is_crt = is_crt
        self.x, self.y = pos

    def tick(self):
        super().tick()
        self.y -= 1
        self.alpha -= 255 / self.duration

    def render(self, screen, font: pygame.font.Font):
        txt_surface = font.render(
            (I18n.text('crt_hit').get() + ' ' if self.is_crt else '') + f"{-self.damage:.0f}", True, self.color)
        txt_surface.set_alpha(max(0, int(self.alpha)))
        screen.blit(txt_surface, (self.x, self.y))


class AnimationParticle(Particle):

    def __init__(self, images, pos, duration):
        super().__init__(pos, duration)
        self.images = images
        self.index = 0

    def tick(self):
        super().tick()
        self.index = min(self.timer * (len(self.images) - 1) / self.duration, len(self.images) - 1)

    def render(self, screen, font: pygame.font.Font):
        screen.blit(self.images[self.index], self.pos)


class LaserCannonParticle(AnimationParticle):

    def __init__(self, pos, duration):
        images = Renderer.load_images_from_sprite('./assets/laser_cannon.png', (207, 102), (207, 102))
        super().__init__(images, pos, duration)
