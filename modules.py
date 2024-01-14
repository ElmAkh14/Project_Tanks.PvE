import pygame
import pygame_gui
import sys
import os
from random import randint
from PIL import Image

# Константы
HERBAL_COLOR = (93, 161, 48)
WINDOW_SIZE = (600, 700)
NEWENEMYEVENT = pygame.USEREVENT + 2
STEP_TANK = 1
STEP_SHELL = 10
ENEMYAPPEARANCE = 5000

# Группы спрайтов
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
shells_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
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


def do_up(character, is_shell=False):
    """Перемещение объекта вверх"""
    character.rect.y -= STEP_TANK if not is_shell else STEP_SHELL


def do_right(character, is_shell=False):
    """Перемещение объекта вправо"""
    character.rect.x += STEP_TANK if not is_shell else STEP_SHELL


def do_down(character, is_shell=False):
    """Перемещение объекта вниз"""
    character.rect.y += STEP_TANK if not is_shell else STEP_SHELL


def do_left(character, is_shell=False):
    """Перемещение объекта влево"""
    character.rect.x -= STEP_TANK if not is_shell else STEP_SHELL
