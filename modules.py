import pygame
import pygame_gui
import sys
import os
from random import randint, choice
from itertools import chain


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


# Константы
HERBAL_COLOR = (93, 161, 48)
TEXT_COLOR = (76, 80, 82)
WINDOW_SIZE = (600, 720)
SELL_SIZE = (30, 30)
ELEMRECT = (200, 50)
NEWENEMYEVENT = pygame.USEREVENT + 3
ENEMYCHANGEMOVE = pygame.USEREVENT + 4
DELETEENEMY = pygame.USEREVENT + 5
ANIMAION = pygame.USEREVENT + 6
RAIN = pygame.USEREVENT + 7
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
tracks_group = pygame.sprite.Group()
hero_tracks_group = pygame.sprite.Group()

# Шрифты
big_font = pygame.font.Font('fonts/unicephalon.otf', 50)
medium_font = pygame.font.Font('fonts/unicephalon.otf', 24)

# Звуки
shot = pygame.mixer.Sound('sounds/shot.ogg')
shot.set_volume(0.01)

# Переменные
game_screen = None
show_manager_flag = True
show_in_game_flag = False
show_pause_flag = False
game_over = False
rain = False
play_shot = False
killed_enemies_sprites = 0

# Часы и таймеры
clock = pygame.time.Clock()
pygame.time.set_timer(NEWENEMYEVENT, 0)
pygame.time.set_timer(ENEMYCHANGEMOVE, 5000)
pygame.time.set_timer(DELETEENEMY, 1000)
pygame.time.set_timer(ANIMAION, 100)
pygame.time.set_timer(RAIN, 30000)


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


# Класс симулятора дождя
class RainSimulator:
    def __init__(self, screen):
        self.blue = '#4169e1'

        # Параметры дождевых капель
        self.drops = []
        self.drops_per_pixel = 100
        self.screen = screen

    def add_drop(self):
        """Добавление новых капель дождя"""
        self.drops.append([randint(0, WINDOW_SIZE[0]), 0])

    def draw_drops(self):
        """Отрисовка капель"""
        for drop in self.drops:
            pygame.draw.line(self.screen, self.blue, (drop[0], drop[1]), (drop[0], drop[1] + 5), 2)

    def update_drops(self):
        """Удаление капель"""
        for drop in self.drops:
            drop[1] += 5
            if drop[1] >= WINDOW_SIZE[1]:
                self.drops.remove(drop)

    def run_rain(self):
        """Запуск симулятора"""
        self.add_drop()
        self.update_drops()
        self.draw_drops()


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
level_label = medium_font.render('Карта', True, TEXT_COLOR)


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


def show_in_game_manager(screen: pygame.surface.Surface, killed_enemies_spr) -> None:
    """Прорисовка менеджера во время игры"""
    in_game_manager.draw_ui(screen)
    text =\
        f"Уничтожено врагов:\n{len(list(filter(lambda sprite:sprite.is_destroyed, enemies))) + killed_enemies_spr}"
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
    for sprite in game_over_group:
        sprite.kill()
    gameover = pygame.sprite.Sprite(game_over_group, all_sprites)
    gameover.image = load_image('game_over.png', 'black')
    gameover.rect = gameover.image.get_rect()
    gameover.rect.x, gameover.rect.y = (WINDOW_SIZE[0] - gameover.rect.width) // 2,\
                                       (WINDOW_SIZE[1] - gameover.rect.height) // 2
    game_over_group.draw(screen)
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
