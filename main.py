import pygame
import pygame_gui.elements

from modules import *
from player import *
from enemy import *
from shell import *
from bush import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tanks.PvE')
    size = width, height = WINDOW_SIZE
    screen = pygame.display.set_mode(size)
    screen.fill(HERBAL_COLOR)

    show_manager_flag = True

    manager = pygame_gui.UIManager(WINDOW_SIZE)
    start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 500), (200, 50)),
                                         text='Начать игру',
                                         manager=manager,
                                         tool_tip_text='Кнопка начала игры')
    frequency = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((200, 300), (200, 50)),
                                                   options_list=['5', '10', '15'],
                                                   starting_option='5',
                                                   manager=manager)

    clock = pygame.time.Clock()
    pygame.time.set_timer(NEWENEMYEVENT, 0)
    # font = pygame.font.Font('fonts/unicephalon.otf')
    #
    # title = font.render('Танки.PvE', 1, (32, 58, 39))
    # screen.blit(title, (0, 0))

    hero = Hero(hero_group, all_sprites)
    cursor = pygame.sprite.Sprite(cursor_group)
    cursor.image = load_image("arrow.png")
    cursor.rect = cursor.image.get_rect()
    for _ in range(15):
        bush = Bush(all_sprites)
        bush.rect.x = randint(0, WINDOW_SIZE[0] - bush.rect.width)
        bush.rect.y = randint(0, WINDOW_SIZE[1] - bush.rect.height)

    all_sprites.draw(screen)

    pygame.display.flip()

    running = True
    while running:
        time_delta = clock.tick(60)
        pygame.time.set_timer(NEWENEMYEVENT, 10)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.angle = 0
                    hero.do_up = True
                if event.key == pygame.K_d:
                    hero.angle = 90
                    hero.do_right = True
                if event.key == pygame.K_s:
                    hero.angle = 180
                    hero.do_down = True
                if event.key == pygame.K_a:
                    hero.angle = 270
                    hero.do_left = True
                if keys[pygame.K_w] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_a]:
                    shell = Shell(hero, shells_group, all_sprites)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.do_up = False
                if event.key == pygame.K_d:
                    hero.do_right = False
                if event.key == pygame.K_s:
                    hero.do_down = False
                if event.key == pygame.K_a:
                    hero.do_left = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == frequency:
                        print(event.text)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start:
                        ENEMYAPPEARANCE = int(frequency.current_state.selected_option) * 1000
                        pygame.time.set_timer(NEWENEMYEVENT, ENEMYAPPEARANCE)
                        show_manager_flag = False
            if event.type == NEWENEMYEVENT:
                pass
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]
            manager.process_events(event)
        manager.update(time_delta)
        screen.fill(HERBAL_COLOR)
        if show_manager_flag:
            manager.draw_ui(screen)
        else:
            all_sprites.draw(screen)
            all_sprites.update()
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            cursor_group.draw(screen)
        pygame.display.flip()
    pygame.quit()