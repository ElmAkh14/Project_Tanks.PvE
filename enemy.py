from modules import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Enemy, self).__init__(*group)

        self.frames = []
        self.cut_sheet(load_image('enemies.png', (255, 255, 255)), 3, 1)
        self.cur_frame = 0

        self.image = load_image('enemy.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.is_destroyed = False
        self.do_anim_flag = True
        self.sec_before_kill = 0
        self.do_up = False
        self.do_right = False
        self.do_down = False
        self.do_left = False

        from_where_list = ['up', 'down', 'right', 'left']
        ch = choice(from_where_list)
        self.angle = 0
        x, y = 0, 0
        if ch == 'up':
            self.angle = 180
            x, y = randint(0, WINDOW_SIZE[0] - self.rect.width), 0
        elif ch == 'down':
            self.angle = 0
            x, y = randint(0, WINDOW_SIZE[0] - self.rect.width), WINDOW_SIZE[1] - self.rect.height
        elif ch == 'right':
            self.angle = 270
            x, y = WINDOW_SIZE[0] - self.rect.width, randint(0, WINDOW_SIZE[1] - self.rect.height)
        elif ch == 'left':
            self.angle = 90
            x, y = 0, randint(0, WINDOW_SIZE[0] - self.rect.height)
        self.rect.x, self.rect.y = x, y
        self.image = load_image('enemy.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, self.angle)

    def update(self):
        for sprite in hero_shells:
            if pygame.sprite.collide_mask(self, sprite):
                self.is_destroyed = True
                self.destroy()
                sprite.kill()
        if self.is_destroyed:
            self.destroy()
            return

        if self.do_anim_flag:
            pass
        #     self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        #     self.image = self.frames[self.cur_frame]
        #     self.image = pygame.transform.rotate(self.image, -self.angle)
        else:
            self.image = load_image('enemy.png', (255, 255, 255))
            self.image = pygame.transform.rotate(self.image, -self.angle)

        # self.image = load_image('enemy.png', (255, 255, 255))
        # self.image = pygame.transform.rotate(self.image, -self.angle)
        if self.do_up:
            do_up(self)
        if self.do_right:
            do_right(self)
        if self.do_down:
            do_down(self)
        if self.do_left:
            do_left(self)
        for sprite in barriers:
            if pygame.sprite.collide_mask(self, sprite):
                if self.do_up:
                    do_down(self)
                if self.do_right:
                    do_left(self)
                if self.do_down:
                    do_up(self)
                if self.do_left:
                    do_right(self)
        self.rect.x %= WINDOW_SIZE[0]
        self.rect.y %= WINDOW_SIZE[1]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def destroy(self):
        self.image = load_image('destroyed enemy.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, -self.angle)

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
        return True

    def do_anim(self):
        if self.do_anim_flag:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.rotate(self.image, -self.angle)
