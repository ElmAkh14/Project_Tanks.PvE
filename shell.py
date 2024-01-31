from modules import *


class Shell(pygame.sprite.Sprite):
    """Класс снаряда"""
    def __init__(self, character, *group):
        super(Shell, self).__init__(*group)
        self.image = load_image('shell.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.image = pygame.transform.rotate(self.image, -character.angle)
        if character.angle == 0:
            self.angle = 0
            self.rect.x = character.rect.x + ((character.rect.width - self.rect.width) // 2)
            self.rect.y = character.rect.y
        if character.angle == 90:
            self.angle = 90
            self.rect.x = character.rect.x + character.rect.width
            self.rect.y = character.rect.y + ((character.rect.height - self.rect.height) // 2)
        if character.angle == 180:
            self.angle = 180
            self.rect.x = character.rect.x + ((character.rect.width - self.rect.width) // 2)
            self.rect.y = character.rect.y + character.rect.height
        if character.angle == 270:
            self.angle = 270
            self.rect.x = character.rect.x
            self.rect.y = character.rect.y + ((character.rect.height - self.rect.height) // 2)

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
        for sprite in barriers:
            if pygame.sprite.collide_mask(self, sprite):
                self.kill()
        if self in hero_shells:
            for sprite in enemies:
                if pygame.sprite.collide_mask(self, sprite):
                    sprite.destroy()
                    self.kill()
        if self in enemy_shells:
            for sprite in hero_group:
                if pygame.sprite.collide_mask(self, sprite):
                    sprite.destroy()
                    self.kill()

