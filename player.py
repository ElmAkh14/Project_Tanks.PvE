from modules import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Hero, self).__init__(*group)
        self.angle = 0
        self.image = load_image('hero.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = (WINDOW_SIZE[0] - self.rect.width) // 2
        self.rect.y = (1.5 * WINDOW_SIZE[1] - self.rect.height) // 2
        self.is_destroyed = False
        self.do_up = False
        self.do_right = False
        self.do_down = False
        self.do_left = False

    def update(self):
        if self.is_destroyed:
            self.desrtoy()
            return
        self.image = load_image('hero.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, -self.angle)
        if self.do_up:
            do_up(self)
        if self.do_right:
            do_right(self)
        if self.do_down:
            do_down(self)
        if self.do_left:
            do_left(self)
        self.rect.x %= WINDOW_SIZE[0]
        self.rect.y %= WINDOW_SIZE[1]

    def desrtoy(self):
        self.image = load_image('destroyed hero.png', (255, 255, 255))