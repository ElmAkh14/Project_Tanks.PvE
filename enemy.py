from modules import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Enemy, self).__init__(*group)
        self.image = load_image('enemy.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def desrtoy(self):
        self.image = load_image('destroyed enemy.png', (255, 255, 255))