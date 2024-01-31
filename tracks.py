from modules import *


class Tracks(pygame.sprite.Sprite):
    """Класс гусениц"""

    def __init__(self, *group):
        super(Tracks, self).__init__(*group)

        self.frames = []
        self.cut_sheet(load_image('tracks.png', (255, 255, 255)), 3, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.angle = 0
        self.character = None
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.draw = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def change_orientation(self, character):
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.rotate(self.image, -character.angle)
        if character.angle == 0:
            self.angle = 0
            self.rect.x = character.rect.x
            self.rect.y = character.rect.y + character.rect.height
        if character.angle == 90:
            self.angle = 90
            self.rect.x = character.rect.x - self.rect.height
            self.rect.y = character.rect.y
        if character.angle == 180:
            self.angle = 180
            self.rect.x = character.rect.x
            self.rect.y = character.rect.y - self.rect.height
        if character.angle == 270:
            self.angle = 270
            self.rect.x = character.rect.x + character.rect.width
            self.rect.y = character.rect.y

    def do_anim(self, character):
        if self.draw:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.change_orientation(character)

    def update(self):
        pass
