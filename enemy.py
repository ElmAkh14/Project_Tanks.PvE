from modules import *
from shell import Shell


class Enemy(pygame.sprite.Sprite):
    """Класс противника"""
    def __init__(self, *group, pos=(0, 0), tracks=None):
        super(Enemy, self).__init__(*group)

        self.tracks = tracks
        self.image = load_image('enemy.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.is_destroyed = False
        self.do_anim_flag = True
        self.sec_before_kill = 0
        self.do_up, self.do_right, self.do_down, self.do_left = False, False, False, False
        self.change_move()

    def update(self):
        if self.is_destroyed:
            return
        self.move()
        self.rect.x %= WINDOW_SIZE[0]
        self.rect.y %= WINDOW_SIZE[1]
        self.move_back()
        self.tracks.change_orientation(self)

    def destroy(self):
        self.is_destroyed = True
        self.do_anim_flag = False
        self.image = load_image('destroyed enemy.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.tracks.kill()

    def change_move(self):
        if self.is_destroyed:
            return False
        self.do_up, self.do_right, self.do_down, self.do_left = False, False, False, False
        self.angle = choice([0, 90, 180, 270])
        if self.angle == 0:
            self.do_up = True
        elif self.angle == 90:
            self.do_right = True
        elif self.angle == 180:
            self.do_down = True
        elif self.angle == 270:
            self.do_left = True
        self.transform_image()
        return True

    def do_anim(self):
        if self.do_anim_flag:
            self.tracks.draw = True
            self.tracks.do_anim(self)

    def move(self):
        if self.do_up:
            do_up(self)
            do_up(self.tracks)
        if self.do_right:
            do_right(self)
            do_right(self.tracks)
        if self.do_down:
            do_down(self)
            do_down(self.tracks)
        if self.do_left:
            do_left(self)
            do_left(self.tracks)
        self.move_back()

    def move_back(self):
        if pygame.sprite.spritecollideany(self, barriers) or pygame.sprite.spritecollideany(self, hero_group):
            if self.do_up:
                do_down(self)
                do_down(self.tracks)
            if self.do_right:
                do_left(self)
                do_left(self.tracks)
            if self.do_down:
                do_up(self)
                do_up(self.tracks)
            if self.do_left:
                do_right(self)
                do_right(self.tracks)
            self.change_move()
            Shell(self, enemy_shells, shells_group, all_sprites)
            shot.play()

    def transform_image(self):
        self.image = load_image('enemy.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, -self.angle)
