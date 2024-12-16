import pygame

import includes


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
    includes.PARTICLES.append(particle)


def remove_all_particles():
    includes.PARTICLES.clear()


def remove_played_particles():
    for i in includes.PARTICLES:
        if i.is_end():
            includes.PARTICLES.remove(i)
            del i


def render_particles(screen, font: pygame.font.Font):
    for i in includes.PARTICLES:
        i.render(screen, font)


def tick_particles():
    for i in includes.PARTICLES:
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


