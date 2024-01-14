import pygame

from modules import *


class Bush(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Bush, self).__init__(*group)
        self.image = load_image('bush.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        for sprite in shells_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.kill()
                sprite.kill()
        for sprite in hero_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.kill()

