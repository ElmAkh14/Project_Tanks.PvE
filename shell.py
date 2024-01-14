from modules import *


class Shell(pygame.sprite.Sprite):
    def __init__(self, character, *group):
        super(Shell, self).__init__(*group)
        self.image = load_image('shell.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.image = pygame.transform.rotate(self.image, character.angle)
        if character.angle == 0:
            self.angle = 0
            self.rect.x = character.rect.x + 12
            self.rect.y = character.rect.y
        if character.angle == 90:
            self.angle = 90
            self.rect.x = character.rect.x + 30
            self.rect.y = character.rect.y + 12
        if character.angle == 180:
            self.angle = 180
            self.rect.x = character.rect.x + 12
            self.rect.y = character.rect.y + 30
        if character.angle == 270:
            self.angle = 270
            self.rect.x = character.rect.x
            self.rect.y = character.rect.y + 12

    def update(self):
        if self.angle == 0:
            do_up(self, is_shell=True)
        if self.angle == 90:
            do_right(self, is_shell=True)
        if self.angle == 180:
            do_down(self, is_shell=True)
        if self.angle == 270:
            do_left(self, is_shell=True)
        self.check_pos()

    def check_pos(self):
        if not (-self.rect.width <= self.rect.x <= WINDOW_SIZE[0]
                and -self.rect.height <= self.rect.y <= WINDOW_SIZE[1]):
            self.kill()
