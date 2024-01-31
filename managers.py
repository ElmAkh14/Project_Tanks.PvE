from modules import *


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

    # game_over_group.clear()
    gameover = pygame.sprite.Sprite(game_over_group, all_sprites)
    gameover.image = load_image('game_over.png', 'black')
    gameover.rect = gameover.image.get_rect()
    gameover.rect.x, gameover.rect.y = (WINDOW_SIZE[0] - gameover.rect.width) // 2,\
                                       (WINDOW_SIZE[1] - gameover.rect.height) // 2
    game_over_manager.draw_ui(screen)