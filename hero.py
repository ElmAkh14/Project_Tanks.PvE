from modules import *
from tracks import Tracks


class Hero(pygame.sprite.Sprite):
    """Класс игрока"""
    def __init__(self, *group, x, y, tracks: Tracks):
        super(Hero, self).__init__(*group)

        self.tracks = tracks
        self.angle = 0
        self.image = load_image('hero.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.do_anim_flag = False
        self.is_destroyed = False
        self.do_up, self.do_right, self.do_down, self.do_left = False, False, False, False

    def update(self):
        self.move()
        self.rect.x %= WINDOW_SIZE[0]
        self.rect.y %= WINDOW_SIZE[1]
        self.tracks.change_orientation(self)

    def destroy(self):
        self.is_destroyed = True
        self.do_anim_flag = False
        self.image = load_image('destroyed hero.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.tracks.kill()

    def do_anim(self):
        if self.do_anim_flag:
            self.tracks.draw = True
            self.tracks.do_anim(self)

    def transform_image(self):
        self.image = load_image('hero.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, -self.angle)

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
        for sprite in chain(barriers, enemies):
            if pygame.sprite.collide_mask(self, sprite):
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
