import pygame

import config


class Particle:

    def __init__(self, pos, duration):
        self.pos = pos
        self.duration = duration
        self.timer = 0

    def tick(self):
        self.timer = min(self.timer + 1, self.duration)
        if self.timer >= self.duration:
            remove_played_particles()

    def is_end(self):
        return self.timer >= self.duration

    def render(self, screen, font: pygame.font.Font):
        pass


def add_particle(particle: Particle):
    config.PARTICLES.append(particle)


def remove_all_particles():
    config.PARTICLES.clear()


def remove_played_particles():
    for i in config.PARTICLES:
        if i.is_end():
            config.PARTICLES.remove(i)
            del i


def render_particles(screen, font: pygame.font.Font):
    for i in config.PARTICLES:
        i.render(screen, font)


def tick_particles():
    for i in config.PARTICLES:
        i.tick()


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
            ('暴击 ' if self.is_crt else '') + f"{-self.damage:.0f}", True, self.color)
        txt_surface.set_alpha(max(0, int(self.alpha)))
        screen.blit(txt_surface, (self.x, self.y))


