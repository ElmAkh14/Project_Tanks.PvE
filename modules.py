import pygame
import pygame_gui
import sys
import os
from random import randint, choice


pygame.init()


# Константы
HERBAL_COLOR = (93, 161, 48)
TEXT_COLOR = (76, 80, 82)
WINDOW_SIZE = (600, 720)
SELL_SIZE = (30, 30)
ELEMRECT = (200, 50)
NEWENEMYEVENT = pygame.USEREVENT + 5
ENEMYCHANGEMOVE = pygame.USEREVENT + 6
DELETEENEMY = pygame.USEREVENT + 7
ANIMAION = pygame.USEREVENT + 8
STEP_TANK = 1
STEP_SHELL = 10

# Группы спрайтов
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
shells_group = pygame.sprite.Group()
hero_shells = pygame.sprite.Group()
enemy_shells = pygame.sprite.Group()
barriers = pygame.sprite.Group()
game_over_group = pygame.sprite.Group()

# Шрифты
big_font = pygame.font.Font('fonts/unicephalon.otf', 50)
medium_font = pygame.font.Font('fonts/unicephalon.otf', 24)

# Переменные
game_screen = None
show_manager_flag = True
show_in_game_flag = False
show_pause_flag = False
game_over = False
killed_enemies_sprites = 0

# Часы и таймеры
clock = pygame.time.Clock()
pygame.time.set_timer(NEWENEMYEVENT, 0)
pygame.time.set_timer(ENEMYCHANGEMOVE, 5000)
pygame.time.set_timer(DELETEENEMY, 1000)
pygame.time.set_timer(ANIMAION, 100)


def load_image(name: str, colorkey=None) -> pygame.surface.Surface:
    """Загрузка изображения из папки data"""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def make_barrier(*group, x, y):
    barrier = pygame.sprite.Sprite(*group)
    barrier.image = load_image('boost.png')
    barrier.rect = barrier.image.get_rect()
    barrier.rect.x, barrier.rect.y = x, y


def make_grass(*group, x, y):
    grass = pygame.sprite.Sprite(*group)
    grass.image = load_image('grass.png')
    grass.rect = grass.image.get_rect()
    grass.rect.x, grass.rect.y = x, y


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
        for sprite in enemies:
            if pygame.sprite.collide_mask(self, sprite):
                self.kill()


class Hero(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super(Hero, self).__init__(*group)

        self.frames = []
        self.cut_sheet(load_image('heroes.png', (255, 255, 255)), 3, 1)
        self.cur_frame = 0

        self.angle = 0
        self.image = load_image('hero.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y
        self.do_anim_flag = False
        self.is_destroyed = False
        self.go_back = False
        self.do_up = False
        self.do_right = False
        self.do_down = False
        self.do_left = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        for sprite in enemy_shells:
            if pygame.sprite.collide_mask(self, sprite):
                self.is_destroyed = True
                self.destroy()
        if self.is_destroyed:
            self.destroy()
            return
        if not self.do_anim_flag:
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

    def destroy(self):
        global game_over
        self.image = load_image('destroyed hero.png', (255, 255, 255))
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.do_anim_flag = False
        game_over = True

    def do_anim(self):
        if self.do_anim_flag:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.rotate(self.image, -self.angle)


def load_level(name: str, bgcolor=HERBAL_COLOR) -> (pygame.surface.Surface, Hero):
    """Загрузка карты уровня из папки levels"""
    hero = None
    size = width, height = WINDOW_SIZE
    screen = pygame.display.set_mode(size)
    screen.fill(bgcolor)
    fullname = os.path.join('levels', name)
    if not os.path.isfile(fullname):
        print(f"Файл с картой '{fullname}' не найден")
        sys.exit()
    with open(fullname, 'r') as map_file:
        for i in range(WINDOW_SIZE[1] // SELL_SIZE[1]):
            line = map_file.readline()
            for j, elem in enumerate(line):
                if elem == '0':
                    make_grass(all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])
                elif elem == '1':
                    make_barrier(barriers, all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])
                elif elem == '2':
                    make_grass(all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])
                    bush = Bush(all_sprites)
                    bush.rect.x, bush.rect.y = j * SELL_SIZE[0], i * SELL_SIZE[1]
                elif elem == '3':
                    make_grass(all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])
                    for sprite in hero_group:
                        sprite.kill()
                    hero = Hero(hero_group, all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])

    return screen, hero

# Менеджер главного меню
manager = pygame_gui.UIManager(WINDOW_SIZE)
start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WINDOW_SIZE[0] - ELEMRECT[0]) // 2,
                                                                500),
                                                               ELEMRECT),
                                     text='Начать игру',
                                     manager=manager)
frequency_new_enemy = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(((WINDOW_SIZE[0] - 2.5
                                                                                    * ELEMRECT[0]) // 2,
                                                                                    (WINDOW_SIZE[1] -
                                                                                    1.7 * ELEMRECT[1]) // 2),
                                                                                   ELEMRECT),
                                                         options_list=['2', '5', '10', '15'],
                                                         starting_option='2',
                                                         manager=manager)

level = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(((WINDOW_SIZE[0] + 0.5 * ELEMRECT[0]) // 2,
                                                                      (WINDOW_SIZE[1] -
                                                                       1.7 * ELEMRECT[1]) // 2),
                                                                     ELEMRECT),
                                           options_list=[x[:-4] for x in os.listdir('levels')],
                                           starting_option=[x[:-4] for x in os.listdir('levels')][0],
                                           manager=manager)


title = big_font.render('Танки.PvE', True, TEXT_COLOR)
frequency_new_enemy_label = medium_font.render('       Частота\nпоявления врагов', True, TEXT_COLOR)
level_label = medium_font.render('Уровень', True, TEXT_COLOR)


def show_main_manager(screen: pygame.surface.Surface) -> None:
    """Прорисовка менеджера главного меню"""
    manager.draw_ui(screen)
    screen.blit(title, ((WINDOW_SIZE[0] - title.get_width()) // 2, (0.5 * WINDOW_SIZE[1] - title.get_height()) // 2))
    screen.blit(frequency_new_enemy_label, ((WINDOW_SIZE[0] - 2.9 * ELEMRECT[0]) // 2,
                                            (WINDOW_SIZE[1] - 4 * ELEMRECT[1]) // 2))
    screen.blit(level_label, ((WINDOW_SIZE[0] + 0.87 * ELEMRECT[0]) // 2, (WINDOW_SIZE[1] - 3 * ELEMRECT[1]) // 2))


# Менеджер в игре
in_game_manager = pygame_gui.UIManager(WINDOW_SIZE)
pause = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (ELEMRECT[0] // 2, ELEMRECT[1] // 2)),
                                     text='Пауза',
                                     manager=in_game_manager)


def show_in_game_manager(screen: pygame.surface.Surface, killed_enemies_sprites) -> None:
    """Прорисовка менеджера во время игры"""
    in_game_manager.draw_ui(screen)
    text =\
        f"Уничтожено врагов:\n{len(list(filter(lambda sprite:sprite.is_destroyed, enemies))) + killed_enemies_sprites}"
    killed_enemies_counter_label = medium_font.render(text, True, TEXT_COLOR)
    screen.blit(killed_enemies_counter_label, ((WINDOW_SIZE[0] - killed_enemies_counter_label.get_width()), 0))


# Менеджер на паузе
pause_manager = pygame_gui.UIManager(WINDOW_SIZE)
again = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WINDOW_SIZE[0] - ELEMRECT[0]) // 2,
                                                                500),
                                                               ELEMRECT),
                                     text='Начать заново',
                                     manager=pause_manager)

resume = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WINDOW_SIZE[0] - ELEMRECT[0]) // 2,
                                                                400),
                                                               ELEMRECT),
                                      text='Продолжить',
                                      manager=pause_manager)

in_main_menu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WINDOW_SIZE[0] - ELEMRECT[0]) // 2,
                                                                300),
                                                               ELEMRECT),
                                            text='В главное меню',
                                            manager=pause_manager)

pause_label = big_font.render('Пауза', True, TEXT_COLOR)


def show_pause_manager(screen: pygame.surface.Surface) -> None:
    """Прорисовка менеджера на паузе"""
    pause_manager.draw_ui(screen)
    screen.blit(pause_label,
                ((WINDOW_SIZE[0] - pause_label.get_width()) // 2,
                 (0.5 * WINDOW_SIZE[1] - pause_label.get_height()) // 2))


# Менеджер при поражении
game_over_manager = pygame_gui.UIManager(WINDOW_SIZE)
in_main_menu_game_over = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WINDOW_SIZE[0] - 2.5
                                                                                    * ELEMRECT[0]) // 2,
                                                                                    500),
                                                                                   ELEMRECT),
                                                      text='В главное меню',
                                                      manager=game_over_manager)
again_game_over = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WINDOW_SIZE[0] + 0.5
                                                                                    * ELEMRECT[0]) // 2,
                                                                                    500),
                                                                                   ELEMRECT),
                                               text='Начать заново',
                                               manager=game_over_manager)


def show_game_over_manager(screen: pygame.surface.Surface) -> None:
    """Прорисовка менеджера при поражении"""

    gameover = pygame.sprite.Sprite(game_over_group, all_sprites)
    gameover.image = load_image('game_over.png', 'black')
    gameover.rect = gameover.image.get_rect()
    gameover.rect.x, gameover.rect.y = (WINDOW_SIZE[0] - gameover.rect.width) // 2,\
                                       (WINDOW_SIZE[1] - gameover.rect.height) // 2
    game_over_manager.draw_ui(screen)


def do_up(character, is_shell=False) -> None:
    """Перемещение объекта вверх"""
    character.rect.y -= STEP_TANK if not is_shell else STEP_SHELL


def do_right(character, is_shell=False) -> None:
    """Перемещение объекта вправо"""
    character.rect.x += STEP_TANK if not is_shell else STEP_SHELL


def do_down(character, is_shell=False) -> None:
    """Перемещение объекта вниз"""
    character.rect.y += STEP_TANK if not is_shell else STEP_SHELL


def do_left(character, is_shell=False) -> None:
    """Перемещение объекта влево"""
    character.rect.x -= STEP_TANK if not is_shell else STEP_SHELL
