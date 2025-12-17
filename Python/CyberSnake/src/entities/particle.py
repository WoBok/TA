import random
import pygame

class Particle:
    """Single particle for explosion/shine effects."""
    def __init__(self, x, y, color, vx, vy, life):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.size = random.randint(3, 8)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        # gravity and damping
        self.vy += 0.2
        self.vx *= 0.98
    
    def is_alive(self):
        return self.life > 0
    
    def draw(self, surface: pygame.Surface):
        alpha = int(255 * (self.life / self.max_life))
        color_with_alpha = (*self.color, alpha)
        size = int(self.size * (self.life / self.max_life))
        if size > 0:
            s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_with_alpha, (size, size), size)
            surface.blit(s, (int(self.x - size), int(self.y - size)))


class ParticleSystem:
    """Particle system manager."""
    def __init__(self):
        self.particles: list[Particle] = []
    
    def emit(self, x, y, color, count=20):
        for _ in range(count):
            speed = random.uniform(2, 8)
            vx = speed * random.uniform(-1, 1)
            vy = speed * random.uniform(-3, 0)
            life = random.randint(20, 40)
            self.particles.append(Particle(x, y, color, vx, vy, life))
    
    def update(self):
        self.particles = [p for p in self.particles if p.is_alive()]
        for p in self.particles:
            p.update()
    
    def draw(self, surface: pygame.Surface):
        for p in self.particles:
            p.draw(surface)

