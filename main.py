from modules import *
from enemy import *
from shell import *

if __name__ == '__main__':
    pygame.display.set_caption('Tanks.PvE')
    size = width, height = WINDOW_SIZE
    screen = pygame.display.set_mode(size)
    screen.fill(HERBAL_COLOR)

    # hero = Hero(hero_group, all_sprites)
    game_screen, hero = load_level('level1.txt')
    cursor = pygame.sprite.Sprite(cursor_group)
    cursor.image = load_image("arrow.png")
    cursor.rect = cursor.image.get_rect()

    all_sprites.draw(screen)
    pygame.display.flip()

    running = True
    while running:
        time_delta = clock.tick(60)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]
            if event.type == pygame.KEYDOWN:
                if show_pause_flag:
                    continue
                if keys[pygame.K_w] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_a]:
                    if hero.is_destroyed:
                        continue
                    hero.do_up, hero.do_right, hero.do_down, hero.do_left = False, False, False, False
                    hero.do_anim_flag = True
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
                    shell = Shell(hero, hero_shells, shells_group, all_sprites)
            if event.type == pygame.KEYUP:
                if show_pause_flag:
                    continue
                if not (keys[pygame.K_w] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_a]):
                    if hero.is_destroyed:
                        continue
                    hero.do_up, hero.do_right, hero.do_down, hero.do_left = False, False, False, False
                    hero.do_anim_flag = False

                if event.key == pygame.K_w:
                    hero.do_up = False
                if event.key == pygame.K_d:
                    hero.do_right = False
                if event.key == pygame.K_s:
                    hero.do_down = False
                if event.key == pygame.K_a:
                    hero.do_left = False
            if event.type in [NEWENEMYEVENT, ENEMYCHANGEMOVE, DELETEENEMY, ANIMAION]:
                if game_over or show_pause_flag:
                    continue
            if event.type == NEWENEMYEVENT:
                if len(enemies) < 20:
                    enemy = Enemy(enemies, all_sprites)
                    enemy.change_move()
            if event.type == ANIMAION:
                hero.do_anim()
                for enemy in enemies:
                    if not enemy.is_destroyed:
                        enemy.do_anim()
            if event.type == ENEMYCHANGEMOVE:
                for i in enemies:
                    if i.change_move():
                        shell = Shell(i, enemy_shells, shells_group, all_sprites)
            if event.type == DELETEENEMY:
                for sprite in enemies:
                    if sprite.is_destroyed:
                        sprite.sec_before_kill += 1
                        if sprite.sec_before_kill == 3:
                            sprite.kill()
                            killed_enemies_sprites += 1
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start:
                        for sprite in all_sprites:
                            sprite.kill()
                        show_in_game_flag = True
                        game_screen, hero = load_level(level.current_state.selected_option + ".txt")
                        pygame.time.set_timer(NEWENEMYEVENT,
                                              int(frequency_new_enemy.current_state.selected_option) * 1000)
                        show_manager_flag = False
                        enemy = Enemy(enemies, all_sprites)
                        enemy.change_move()
                    if event.ui_element == pause:
                        show_in_game_flag = False
                        show_pause_flag = True
                    if event.ui_element == again:
                        killed_enemies_sprites = 0
                        for sprite in all_sprites:
                            sprite.kill()
                        show_in_game_flag = True
                        show_pause_flag = False
                        game_screen, hero = load_level(level.current_state.selected_option + ".txt")
                        show_manager_flag = False
                        enemy = Enemy(enemies, all_sprites)
                        enemy.change_move()
                    if event.ui_element == resume:
                        show_in_game_flag = True
                        show_pause_flag = False
                    if event.ui_element == in_main_menu:
                        killed_enemies_sprites = 0
                        show_manager_flag = True
                        show_in_game_flag = False
                        show_pause_flag = False
                        screen.fill(HERBAL_COLOR)
                        for sprite in all_sprites:
                            sprite.kill()
                        manager.draw_ui(screen)
                    if event.ui_element == in_main_menu_game_over:
                        killed_enemies_sprites = 0
                        show_manager_flag = True
                        show_in_game_flag = False
                        show_pause_flag = False
                        game_over = False
                        screen.fill(HERBAL_COLOR)
                        for sprite in all_sprites:
                            sprite.kill()
                        manager.draw_ui(screen)
                    if event.ui_element == again_game_over:
                        killed_enemies_sprites = 0
                        for sprite in all_sprites:
                            sprite.kill()
                        show_in_game_flag = True
                        game_over = False
                        game_screen, hero = load_level(level.current_state.selected_option + ".txt")
                        show_manager_flag = False
                        enemy = Enemy(enemies, all_sprites)
                        enemy.change_move()
            manager.process_events(event)
            in_game_manager.process_events(event)
            pause_manager.process_events(event)
            game_over_manager.process_events(event)
        manager.update(time_delta)
        in_game_manager.update(time_delta)
        pause_manager.update(time_delta)
        game_over_manager.update(time_delta)
        screen.fill(HERBAL_COLOR)
        if show_manager_flag:
            show_main_manager(screen)
        else:
            screen.blit(game_screen, (0, 0))
            all_sprites.draw(screen)
            shells_group.draw(screen)
            enemies.draw(screen)
            hero_group.draw(screen)
            game_over_group.draw(screen)
            if hero.is_destroyed:
                if not game_over:
                    game_over = True
                show_game_over_manager(screen)
            else:
                if show_pause_flag:
                    show_pause_manager(screen)
                elif show_in_game_flag:
                    all_sprites.update()
                    show_in_game_manager(screen, killed_enemies_sprites)
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            cursor_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
