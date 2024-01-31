from modules import *
from bush import Bush
from tracks import Tracks
from hero import Hero


def make_barrier(*group, x, y):
    barrier = pygame.sprite.Sprite(*group)
    barrier.image = load_image('barrier.png')
    barrier.rect = barrier.image.get_rect()
    barrier.rect.x, barrier.rect.y = x, y


def make_grass(*group, x, y):
    grass = pygame.sprite.Sprite(*group)
    grass.image = load_image('grass.png')
    grass.rect = grass.image.get_rect()
    grass.rect.x, grass.rect.y = x, y


def load_level(name: str, bgcolor=HERBAL_COLOR) -> (pygame.surface.Surface, Hero):
    """Загрузка карты уровня из папки levels"""
    hero = None
    enemies_spawns = []
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
                    enemies_spawns.append((j * SELL_SIZE[0], i * SELL_SIZE[1]))
                elif elem == '1':
                    make_barrier(barriers, all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])
                elif elem == '2':
                    make_grass(all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])
                    bush = Bush(all_sprites)
                    bush.rect.x, bush.rect.y = j * SELL_SIZE[0], i * SELL_SIZE[1]
                elif elem == '3':
                    make_grass(all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1])
                    for sprite in chain(hero_group, hero_tracks_group):
                        sprite.kill()
                    hero_tracks = Tracks(hero_tracks_group)
                    hero = Hero(hero_group, all_sprites, x=j * SELL_SIZE[0], y=i * SELL_SIZE[1], tracks=hero_tracks)

    return screen, hero, enemies_spawns

