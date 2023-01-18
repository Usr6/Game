import sys

import pygame
import os
from random import randint


pygame.init()
card = []
kletka = [[[(0, 0), (0, 0, 0, 0), '-', '-']] * 10 for i in range(10)]
army = [[['-', (0, 0), (0, 0), None, '-', 0, 0]] * 10 for _ in range(10)]
running_units = []
player_turn = True  # Если True то ходит 1 игрок, если False то ходит 2 игрок
player1_money = 100
player1_derev = 0
player1_zamk = 0
player2_money = 100
player2_derev = 0
player2_zamk = 0
notex = True
boarder = True
a = pygame.image.load('data/gameElements/blue/castle.png')
pygame.display.set_icon(a)
pygame.display.set_caption('Very Long War')


def restart():
    global card, kletka, army, running_units, \
        player_turn, player1_money, player1_derev, \
        player1_zamk, player2_money, player2_derev, \
        player2_zamk
    card = []
    kletka = [[[(0, 0), (0, 0, 0, 0), '-', '-']] * 10 for i in range(10)]
    army = [[['-', (0, 0), (0, 0), None, '-', 0, 0]] * 10 for _ in range(10)]
    running_units = []
    player_turn = True  # Если True то ходит 1 игрок, если False то ходит 2 игрок
    player1_money = 100
    player1_derev = 0
    player1_zamk = 0
    player2_money = 100
    player2_derev = 0
    player2_zamk = 0


def load_image(name, path, color_key=None):  # Загрузка картинок
    fullname = os.path.join('data', path, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def underLoad(name, path, sz):
    tim = load_image(name, path)
    return tim, tim.get_rect(bottomright=sz)


tile_width = tile_height = 80


class Board:
    def __init__(self, file, screen, turn):
        self.filename = 'data/' + 'maps/' + file
        self.screen = screen
        self.turn = turn

    def load_level(self):
        global card, boarder
        with open(self.filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        card = list(map(lambda tile: tile.ljust(max_width, '.'), level_map))  # Создание списка из прочитанной карты.
        x, y = 0, 0
        surf, rect = 0, 0
        for i in range(len(card)):
            for i1 in range(len(card[0])):
                ready = False
                if card[i][i1] == '-':
                    surf, rect = underLoad('Water.png', 'gameElements', ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                elif card[i][i1] == '#':
                    surf, rect = underLoad('grass.png', 'gameElements', ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                elif card[i][i1] == '<':
                    surf, rect = underLoad('home.png', os.path.join('gameElements', 'blue'), ((i1 + 1) * tile_width,
                                                                                              (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                elif card[i][i1] == '>':
                    surf, rect = underLoad('enemy.png', os.path.join('gameElements', 'red'), ((i1 + 1) * tile_width,
                                                                                              (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                elif card[i][i1] == '^':
                    surf, rect = underLoad('forest.png', 'gameElements', ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                if kletka[i][i1][2] == '!':
                    pygame.draw.rect(self.screen, pygame.Color("yellow"), (x, y, 80, 80))
                    kletka[i][i1] = [(i1, i), (i1 * 80, i * 80, (i1 + 1) * 80, (i + 1) * 80), '!', kletka[i][i1][3]]
                    ready = True
                elif kletka[i][i1][2] == '|':
                    pygame.draw.rect(self.screen, pygame.Color("yellow"), (x, y, 80, 80))
                    kletka[i][i1] = [(i1, i), (i1 * 80, i * 80, (i1 + 1) * 80, (i + 1) * 80), '|', kletka[i][i1][3]]
                    ready = True
                elif kletka[i][i1][2] == ':':
                    if kletka[i][i1][3] == 'blue':
                        surf, rect = underLoad('homeDerev.png', 'gameElements/blue',
                                               ((i1 + 1) * tile_width, (i + 1) * tile_height))
                        kletka[i][i1] = [(i1, i), (i1 * 80, i * 80, (i1 + 1) * 80, (i + 1) * 80), ':', 'blue']
                    elif kletka[i][i1][3] == 'red':
                        surf, rect = underLoad('enemyDerev.png', 'gameElements/red',
                                               ((i1 + 1) * tile_width, (i + 1) * tile_height))
                        kletka[i][i1] = [(i1, i), (i1 * 80, i * 80, (i1 + 1) * 80, (i + 1) * 80), ':', 'red']
                    self.screen.blit(surf, rect)
                    ready = True
                elif kletka[i][i1][2] == ';':
                    surf, rect = underLoad('castle.png', os.path.join('gameElements', kletka[i][i1][3]),
                                           ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                    pygame.draw.circle(self.screen, pygame.Color(kletka[i][i1][3]), (x + 10, y + 10), 20)
                    kletka[i][i1] = [(i1, i), (i1 * 80, i * 80, (i1 + 1) * 80, (i + 1) * 80), ';', kletka[i][i1][3]]
                    ready = True
                elif kletka[i][i1][2] == 'x':
                    surf, rect = underLoad('atck.png', 'gameElements',
                                           ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    kletka[i][i1] = [(i1, i), (i1 * 80, i * 80, (i1 + 1) * 80, (i + 1) * 80), 'x', kletka[i][i1][3]]
                    self.screen.blit(surf, rect)
                    ready = True
                if army[i][i1][0] == '/':
                    if army[i][i1][4] == 'blue':
                        timebank = 'builds.png'
                    else:
                        timebank = 'enemyBuilds.png'
                    surf, rect = underLoad(timebank, os.path.join('gameElements', army[i][i1][4]),
                                           ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                    pygame.draw.rect(self.screen, pygame.Color('black'), (x + 5, y + 5, 70, 10))
                    pygame.draw.rect(self.screen, pygame.Color('red'), (x + 8, y + 7, 64, 6))
                elif army[i][i1][0] == '}':
                    surf, rect = underLoad('sword.png', os.path.join('gameElements', army[i][i1][4]),
                                           ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                    minushp = 64 // 3 * army[i][i1][5]
                    pygame.draw.rect(self.screen, pygame.Color('black'), (x + 5, y + 5, 70, 10))
                    pygame.draw.rect(self.screen, pygame.Color('red'), (x + 8, y + 7, minushp, 6))
                elif army[i][i1][0] == ']':
                    surf, rect = underLoad('archer.png', os.path.join('gameElements', army[i][i1][4]),
                                           ((i1 + 1) * tile_width, (i + 1) * tile_height))
                    self.screen.blit(surf, rect)
                    minushp = 64 // 2 * army[i][i1][5]
                    pygame.draw.rect(self.screen, pygame.Color('black'), (x + 5, y + 5, 70, 10))
                    pygame.draw.rect(self.screen, pygame.Color('red'), (x + 8, y + 7, minushp, 6))
                if not ready:
                    kletka[i][i1] = [(i1, i), (i1 * 80, i * 80, (i1 + 1) * 80, (i + 1) * 80), card[i][i1], '-']
                if self.turn:
                    pygame.draw.circle(self.screen, pygame.Color('blue'), (760, 120), 20)
                else:
                    pygame.draw.circle(self.screen, pygame.Color('red'), (760, 120), 20)
                if boarder:
                    pygame.draw.rect(self.screen, pygame.Color('black'), (x, y, 80, 80), 1)
                x += 80
            y += 80
            x = 0
        return

    @staticmethod
    def clicked(x, y):  # Проверка на что кликнула мышка во время игры
        for i in range(len(kletka)):
            for i1 in range(len(kletka[0])):
                x1, y1 = kletka[i][i1][1][0], kletka[i][i1][1][1]
                x2, y2 = kletka[i][i1][1][2], kletka[i][i1][1][3]
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return kletka[i][i1][0], kletka[i][i1][1], kletka[i][i1][2]


class Windows:  # Все игровые циклы
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(self.size)

    def menu(self):  # проверка на взаимодействие во время нахождения в меню
        global notex
        running = True
        x, y = 0, 0
        tutorial = False
        n_tut = 0
        first_surf, first_rect = None, None
        btnStart_surf, btnStart_rect = None, None
        btnExit_surf, btnExit_rect = None, None
        btnSet_surf, btnSet_rect = None, None
        car_surf, car_rect = None, None
        while running:
            if not tutorial:
                first_surf, first_rect = underLoad("ZastavkaZ.png", "menu", self.size)
                btnStart_surf, btnStart_rect = underLoad('Start.png', "menu", (550, 400))
                btnExit_surf, btnExit_rect = underLoad('Exit.png', "menu", (520, 750))
                btnSet_surf, btnSet_rect = underLoad('settings.png', "menu", (570, 550))
            else:
                car_surf, car_rect = underLoad('cart' + str(n_tut) + '.png', "tutorial", self.size)
            if 250 < x < 550 and 300 < y < 400:
                btnStart_surf = load_image('Start2.png', "menu")
            elif 220 < x < 525 and 650 < y < 750:
                btnExit_surf = load_image('Exit2.png', "menu")
            elif 220 < x < 570 and 450 < y < 550:
                btnSet_surf, btnSet_rect = underLoad('settings2.png', "menu", (570, 550))
            if not tutorial:
                self.screen.blit(first_surf, first_rect)
                self.screen.blit(btnStart_surf, btnStart_rect)
                self.screen.blit(btnExit_surf, btnExit_rect)
                self.screen.blit(btnSet_surf, btnSet_rect)
            else:
                self.screen.blit(car_surf, car_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 250 < x < 550 and 300 < y < 400 and not tutorial:
                        first_surf, first_rect = None, None
                        btnStart_surf, btnStart_rect = None, None
                        btnExit_surf, btnExit_rect = None, None  # Реакция на кнопку "Начать"
                        notex = True
                        Windows(self.size).mapChoice()
                    elif 220 < x < 525 and 650 < y < 750 and not tutorial:
                        running = False  # Реакция на кнопку "Выход"
                    elif 220 < x < 570 and 450 < y < 550 and not tutorial:
                        tutorial = True  # Реакция на кнопку "Обучение"
                    if tutorial:
                        n_tut += 1
            if n_tut == 6:
                n_tut = 0
                tutorial = False
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def mapChoice(self):  # проверка на взаимодействие во время выбора карты
        global notex
        mapRunning = True
        menuMap_surf, menuMap_rect = underLoad("mapMenu.png", "menu", self.size)
        ex_surf, ex_rect = underLoad("exit.png", "gameElements", (800, 50))
        x, y = 0, 0
        while mapRunning:
            map1_surf, map1_rect = underLoad("map1.png", "menu", (225, 770))
            map2_surf, map2_rect = underLoad("map2.png", "menu", (475, 770))
            map3_surf, map3_rect = underLoad("map3.png", "menu", (725, 770))
            if 50 < x < 225 and 170 < y < 770:
                map1_surf = load_image('map12.png', "menu")
            elif 300 < x < 475 and 170 < y < 770:
                map2_surf = load_image('map22.png', "menu")
            elif 550 < x < 725 and 170 < y < 770:
                map3_surf = load_image('map32.png', "menu")
            self.screen.blit(menuMap_surf, menuMap_rect)
            self.screen.blit(map1_surf, map1_rect)
            self.screen.blit(map2_surf, map2_rect)
            self.screen.blit(map3_surf, map3_rect)
            self.screen.blit(ex_surf, ex_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 50 < x < 225 and 170 < y < 770:
                        menuMap_surf, menuMap_rect = None, None
                        map1_surf, map1_rect = None, None
                        mapRunning = False  # Взаимодействие с первой картой
                        Windows(self.size).game("map1.map")
                    elif 300 < x < 475 and 170 < y < 770:
                        menuMap_surf, menuMap_rect = None, None
                        map2_surf, map2_rect = None, None
                        mapRunning = False
                        Windows(self.size).game("map2.map")
                    elif 550 < x < 725 and 170 < y < 770:
                        menuMap_surf, menuMap_rect = None, None
                        map3_surf, map3_rect = None, None
                        mapRunning = False
                        Windows(self.size).game("map3.map")
                    elif 750 < x < 800 and 0 < y < 50:
                        mapRunning = False
            if not notex:
                mapRunning = False
            pygame.display.flip()

    def game(self, map):  # Игровой цикл во время игровой сессии
        global player1_money, player2_money, player_turn, running_units, notex
        gameRunning = True
        menu_surf, menu_rect = None, None
        armyMenu_surf, armyMenu_rect = None, None
        middleX, middleY = 0, 0
        coordX, coordY = -1, -1
        seen = False
        font = pygame.font.Font(None, 30)
        tapping = False
        zatr = 0
        svor = False
        uni = 0
        number_units = 0
        troop = '-'
        hp = 1
        atck = True
        while gameRunning:
            global notex
            if player_turn:
                string_rendered = font.render(str(player1_money), True, pygame.Color('white'))
            else:
                string_rendered = font.render(str(player2_money), True, pygame.Color('white'))
            self.screen.fill((0, 0, 0))
            Board(map, self.screen, player_turn).load_level()
            next_surf, next_rect = underLoad('next.png', 'gameElements', (800, 800))
            self.screen.blit(next_surf, next_rect)
            for i in range(1, len(running_units), 2):
                res = Animation(self.screen, (None, None), (None, None), 20).running_animation(player_turn,
                                                                                               running_units[i])
                running_units[i] = res
            if menu_surf is not None and menu_rect is not None:
                self.screen.blit(menu_surf, menu_rect)
            if armyMenu_surf is not None and armyMenu_rect is not None:
                if not seen:
                    Animation(self.screen, (0, 800), (200, 800), 1000).sliding_animation(('army.png', 'gameElements'))
                    seen = True
                self.screen.blit(armyMenu_surf, armyMenu_rect)
                money_rect = string_rendered.get_rect()
                money_rect.top = 725
                money_rect.x = 25
                self.screen.blit(string_rendered, money_rect)
            elif svor:
                svor_surf, svor_rect = underLoad('svor.png', 'gameElements', (150, 50))
                self.screen.blit(svor_surf, svor_rect)
            elif tapping:
                exit_surf, exit_rect = underLoad('exit.png', 'gameElements', (50, 50))
                self.screen.blit(exit_surf, exit_rect)
            mn_surf, mn_rect = underLoad('menu.png', 'gameElements', (800, 80))
            self.screen.blit(mn_surf, mn_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    number, coord, znak = Board(map, self.screen, player_turn).clicked(x, y)
                    if kletka[number[1]][number[0]][2] == ';' and atck:
                        Unit(';', self.screen, number).bunker(map)
                        atck = False
                    if player_turn and army[number[1]][number[0]][0] != '-' and army[number[1]][number[0]][3] and \
                            army[number[1]][number[0]][4] == 'blue' and armyMenu_rect is None \
                            and not tapping:  # Проверка на взаимодействие - юнит
                        Unit(army[number[1]][number[0]], self.screen, number).movement(map, player_turn)
                        menu_surf, menu_rect = None, None
                    elif not player_turn and army[number[1]][number[0]][0] != '-' and \
                            army[number[1]][number[0]][3] and \
                            army[number[1]][number[0]][4] == 'red' and armyMenu_rect is None and not tapping:
                        Unit(army[number[1]][number[0]], self.screen, number).movement(map, player_turn)
                        menu_surf, menu_rect = None, None
                    if kletka[number[1]][number[0]][2] == '!' and uni == 1:  # Проверка на возможность - поставить юнит
                        middleX, middleY = coord[0] + (coord[2] - coord[0]) // 2, coord[1] + (coord[3] - coord[1]) // 2
                        number_units += 1
                        if troop == '/':
                            hp = 1
                        elif troop == '}':
                            hp = 3
                        elif troop == ']':
                            hp = 2
                        if player_turn:
                            army[number[1]][number[0]] = [troop, (coord[2] - 40, coord[3] - 40), number, False, 'blue',
                                                          hp, number_units]
                            color = 'blue'
                        else:
                            army[number[1]][number[0]] = [troop, (coord[2] - 40, coord[3] - 40), number, False, 'red',
                                                          hp, number_units]
                            color = 'red'
                        running_units.append(number_units)
                        running_units.append([[middleX + randint(-30, 30), middleY + randint(-30, 30)], coord,
                                              [1, -1], [middleX + randint(-30, 30), middleY + randint(-30, 30)],
                                              coord, [-1, -1],
                                              [middleX + randint(-30, 30), middleY + randint(-30, 30)],
                                              coord, [1, 1], pygame.Color(color)])
                        if kletka[coordX][coordY - 1][2] == '!':
                            kletka[coordX][coordY - 1][2] = '#'
                        if kletka[coordX][coordY + 1][2] == '!':
                            kletka[coordX][coordY + 1][2] = '#'
                        if kletka[coordX - 1][coordY][2] == '!':
                            kletka[coordX - 1][coordY][2] = '#'
                        if kletka[coordX + 1][coordY][2] == '!':
                            kletka[coordX + 1][coordY][2] = '#'
                        tapping = False
                    if middleX - 100 < x < middleX and middleY - 100 < y < middleY and menu_rect is not None and \
                            armyMenu_rect is None:  # проверка на взаимодействие - меню
                        menu_surf, menu_rect = None, None
                        armyMenu_surf, armyMenu_rect = underLoad('army.png', 'gameElements', (200, 800))
                        continue
                    elif 25 < x < 175 and 100 < y < 200 and armyMenu_rect is not None and \
                            ((player_turn and player1_money >= 50) or (not player_turn and player2_money >= 50)):
                        # Проверка на взаимодействие - покупка строителей
                        coordX, coordY, troop = Unit('/', self.screen, number).unlocking(player_turn)
                        uni = 1
                        armyMenu_surf, armyMenu_rect = None, None
                        menu_surf, menu_rect = None, None
                        tapping = True
                        zatr = 50
                        if player_turn:
                            player1_money -= zatr
                        else:
                            player2_money -= zatr
                    elif 25 < x < 175 and 250 < y < 350 and armyMenu_rect is not None and \
                            ((player_turn and player1_money >= 100) or (not player_turn and player2_money >= 100)):
                        # Проверка на взаимодействие - покупка мечников
                        coordX, coordY, troop = Unit('}', self.screen, number).unlocking(player_turn)
                        uni = 1
                        armyMenu_surf, armyMenu_rect = None, None
                        menu_surf, menu_rect = None, None
                        tapping = True
                        zatr = 100
                        if player_turn:
                            player1_money -= zatr
                        else:
                            player2_money -= zatr
                    elif 25 < x < 175 and 400 < y < 500 and armyMenu_rect is not None and \
                            ((player_turn and player1_money >= 100) or (not player_turn and player2_money >= 100)):
                        # Проверка на взаимодействие - покупка лучников
                        coordX, coordY, troop = Unit(']', self.screen, number).unlocking(player_turn)
                        uni = 1
                        armyMenu_surf, armyMenu_rect = None, None
                        menu_surf, menu_rect = None, None
                        tapping = True
                        zatr = 100
                        if player_turn:
                            player1_money -= zatr
                        else:
                            player2_money -= zatr
                    elif 0 < x < 50 and 0 < y < 50:  # Проверка на взаимодействие - выход
                        armyMenu_surf, armyMenu_rect = None, None
                        menu_surf, menu_rect = None, None
                        if kletka[coordX][coordY - 1][2] == '!':
                            kletka[coordX][coordY - 1][2] = '#'
                        if kletka[coordX][coordY + 1][2] == '!':
                            kletka[coordX][coordY + 1][2] = '#'
                        if kletka[coordX - 1][coordY][2] == '!':
                            kletka[coordX - 1][coordY][2] = '#'
                        if kletka[coordX + 1][coordY][2] == '!':
                            kletka[coordX + 1][coordY][2] = '#'
                        if player_turn:
                            player1_money += zatr
                        else:
                            player2_money += zatr
                        zatr = 0
                        tapping = False
                    elif 100 < x < 150 and 0 < y < 50:  # Проверка на взаимодействие - свернуть
                        if svor:
                            armyMenu_surf, armyMenu_rect = underLoad('army.png', 'gameElements', (200, 800))
                            svor = False
                        else:
                            armyMenu_surf, armyMenu_rect = None, None
                            svor = True
                    else:
                        menu_surf, menu_rect = None, None
                    middleX, middleY = coord[0] + (coord[2] - coord[0]) // 2, coord[1] + (coord[3] - coord[1]) // 2
                    if armyMenu_rect is None and znak == '<' and not tapping and player_turn:
                        # Проверка на взаимодействие - замок {ход синих}
                        menu_surf, menu_rect = \
                            underLoad('armyMenu.png', 'gameElements', (middleX, middleY))
                    elif armyMenu_rect is None and znak == '>' and not tapping and not player_turn:
                        # Проверка на взаимодействие - замок {ход красных}
                        menu_surf, menu_rect = \
                            underLoad('armyMenu.png', 'gameElements', (middleX, middleY))
                    if 640 < x < 800 and 720 < y < 800:
                        next_turn()
                        zatr = 0
                        atck = True
                    elif 720 < x < 800 and 0 < y < 80:
                        pause(self.screen)
            if not notex:
                gameRunning = False
            pygame.display.flip()


class Unit:
    def __init__(self, troop, screen, number):
        self.troop = troop
        self.screen = screen
        self.number = number

    def unlocking(self, turn):
        find = False
        ras1, ras2 = 0, 0
        for i in range(len(kletka)):
            for i1 in range(len(kletka[i])):
                if find:
                    break
                if kletka[i][i1][2] == '<' and turn:
                    ras1, ras2 = i, i1
                    find = True
                elif kletka[i][i1][2] == '>' and not turn:
                    ras1, ras2 = i, i1
                    find = True
            if find:
                break
        if army[ras1][ras2 - 1][0] == '-' and (kletka[ras1][ras2 - 1][2] == '#' or kletka[ras1][ras2 - 1][2] == '^'):
            kletka[ras1][ras2 - 1][2] = '!'
        if army[ras1][ras2 + 1][0] == '-' and (kletka[ras1][ras2 + 1][2] == '#' or kletka[ras1][ras2 + 1][2] == '^'):
            kletka[ras1][ras2 + 1][2] = '!'
        if army[ras1 - 1][ras2][0] == '-' and (kletka[ras1 - 1][ras2][2] == '#' or kletka[ras1 - 1][ras2][2] == '^'):
            kletka[ras1 - 1][ras2][2] = '!'
        if army[ras1 + 1][ras2][0] == '-' and (kletka[ras1 + 1][ras2][2] == '#' or kletka[ras1 + 1][ras2][2] == '^'):
            kletka[ras1 + 1][ras2][2] = '!'
        return ras1, ras2, self.troop

    def movement(self, map, turn):
        global player1_derev, player1_zamk, player2_derev, player2_zamk, notex
        moving = True
        timebank, timebank1, timebank2, timebank3 = '-', '-', '-', '-'
        timebank4, timebank5, timebank6, timebank7 = '-', '-', '-', '-'
        timebank8, timebank9, timebank10, timebank11 = '-', '-', '-', '-'
        atkrange = 0
        if self.troop[0] == '}':
            atkrange = 0
        elif self.troop[0] == ']':
            atkrange = 1
            if kletka[self.number[1] + atkrange][self.number[0] + atkrange][2] != '-':
                timebank4 = kletka[self.number[1] + atkrange][self.number[0] + atkrange][2]
                if army[self.number[1] + atkrange][self.number[0] + atkrange][0] != '-' and \
                        army[self.number[1] + atkrange][self.number[0] + atkrange][4] != self.troop[4]:
                    kletka[self.number[1] + atkrange][self.number[0] + atkrange][2] = 'x'
            if kletka[self.number[1] - atkrange][self.number[0] + atkrange][2] != '-':
                timebank5 = kletka[self.number[1] - atkrange][self.number[0] + atkrange][2]
                if army[self.number[1] - atkrange][self.number[0] + atkrange][0] != '-' and \
                        army[self.number[1] - atkrange][self.number[0] + atkrange][4] != self.troop[4]:
                    kletka[self.number[1] - atkrange][self.number[0] + atkrange][2] = 'x'
            if kletka[self.number[1] - atkrange][self.number[0] - atkrange][2] != '-':
                timebank6 = kletka[self.number[1] - atkrange][self.number[0] - atkrange][2]
                if army[self.number[1] - atkrange][self.number[0] - atkrange][0] != '-' and \
                        army[self.number[1] - atkrange][self.number[0] - atkrange][4] != self.troop[4]:
                    kletka[self.number[1] - atkrange][self.number[0] - atkrange][2] = 'x'
            if kletka[self.number[1] + atkrange][self.number[0] - atkrange][2] != '-':
                timebank7 = kletka[self.number[1] + atkrange][self.number[0] - atkrange][2]
                if army[self.number[1] + atkrange][self.number[0] - atkrange][0] != '-' and \
                        army[self.number[1] + atkrange][self.number[0] - atkrange][4] != self.troop[4]:
                    kletka[self.number[1] + atkrange][self.number[0] - atkrange][2] = 'x'
            if kletka[self.number[1] + 1][self.number[0]][2] != '-':
                timebank = kletka[self.number[1] + 1][self.number[0]][2]
                if army[self.number[1] + 1][self.number[0]][0] != '-' and \
                        army[self.number[1] + 1][self.number[0]][4] != self.troop[4]:
                    kletka[self.number[1] + 1][self.number[0]][2] = 'x'
            if kletka[self.number[1] - 1][self.number[0]][2] != '-':
                timebank1 = kletka[self.number[1] - 1][self.number[0]][2]
                if army[self.number[1] - 1][self.number[0]][0] != '-' and \
                        army[self.number[1] - 1][self.number[0]][4] != self.troop[4]:
                    kletka[self.number[1] - 1][self.number[0]][2] = 'x'
            if kletka[self.number[1]][self.number[0] + 1][2] != '-':
                timebank2 = kletka[self.number[1]][self.number[0] + 1][2]
                if army[self.number[1]][self.number[0] + 1][0] != '-' and \
                        army[self.number[1]][self.number[0] + 1][4] != self.troop[4]:
                    kletka[self.number[1]][self.number[0] + 1][2] = 'x'
            if kletka[self.number[1]][self.number[0] - 1][2] != '-':
                timebank3 = kletka[self.number[1]][self.number[0] - 1][2]
                if army[self.number[1]][self.number[0] - 1][0] != '-' and \
                        army[self.number[1]][self.number[0] - 1][4] != self.troop[4]:
                    kletka[self.number[1]][self.number[0] - 1][2] = 'x'
        if kletka[self.number[1] + 1][self.number[0]][2] != '-' and \
                ((turn and kletka[self.number[1] + 1][self.number[0]][2] != '<') or
                 (not turn and kletka[self.number[1] + 1][self.number[0]][2] != '>')):
            if timebank == '-':
                timebank = kletka[self.number[1] + 1][self.number[0]][2]
            timebank8 = kletka[self.number[1] + 1 + atkrange][self.number[0]][2]
            if kletka[self.number[1] + 1][self.number[0]][2] == ':' and \
                    army[self.number[1] + 1][self.number[0]][0] == '-':
                kletka[self.number[1] + 1][self.number[0]][2] = '|'
            elif army[self.number[1] + 1][self.number[0]][0] == '-':
                kletka[self.number[1] + 1][self.number[0]][2] = '!'
            if army[self.number[1] + 1 + atkrange][self.number[0]][0] != '-' and \
                    army[self.number[1] + 1 + atkrange][self.number[0]][4] != self.troop[4] and \
                    army[self.number[1]][self.number[0]][0] != '/':
                kletka[self.number[1] + 1 + atkrange][self.number[0]][2] = 'x'
        if kletka[self.number[1] - 1][self.number[0]][2] != '-' and \
                ((turn and kletka[self.number[1] - 1][self.number[0]][2] != '<') or
                 (not turn and kletka[self.number[1] - 1][self.number[0]][2] != '>')):
            if timebank1 == '-':
                timebank1 = kletka[self.number[1] - 1][self.number[0]][2]
            timebank9 = kletka[self.number[1] - 1 - atkrange][self.number[0]][2]
            if kletka[self.number[1] - 1][self.number[0]][2] == ':' and \
                    army[self.number[1] - 1][self.number[0]][0] == '-':
                kletka[self.number[1] - 1][self.number[0]][2] = '|'
            elif army[self.number[1] - 1][self.number[0]][0] == '-':
                kletka[self.number[1] - 1][self.number[0]][2] = '!'
            if army[self.number[1] - 1 - atkrange][self.number[0]][0] != '-' and \
                    army[self.number[1] - 1 - atkrange][self.number[0]][4] != self.troop[4] and \
                    army[self.number[1]][self.number[0]][0] != '/':
                kletka[self.number[1] - 1 - atkrange][self.number[0]][2] = 'x'
        if kletka[self.number[1]][self.number[0] + 1][2] != '-' and \
                ((turn and kletka[self.number[1]][self.number[0] + 1][2] != '<') or
                 (not turn and kletka[self.number[1]][self.number[0] + 1][2] != '>')):
            if timebank2 == '-':
                timebank2 = kletka[self.number[1]][self.number[0] + 1][2]
            timebank10 = kletka[self.number[1]][self.number[0] + 1 + atkrange][2]
            if kletka[self.number[1]][self.number[0] + 1][2] == ':' and \
                    army[self.number[1]][self.number[0] + 1][0] == '-':
                kletka[self.number[1]][self.number[0] + 1][2] = '|'
            elif army[self.number[1]][self.number[0] + 1][0] == '-':
                kletka[self.number[1]][self.number[0] + 1][2] = '!'
            if army[self.number[1]][self.number[0] + 1 + atkrange][0] != '-' and \
                    army[self.number[1]][self.number[0] + 1 + atkrange][4] != self.troop[4] and \
                    army[self.number[1]][self.number[0]][0] != '/':
                kletka[self.number[1]][self.number[0] + 1 + atkrange][2] = 'x'
        if kletka[self.number[1]][self.number[0] - 1][2] != '-' and \
                ((turn and kletka[self.number[1]][self.number[0] - 1][2] != '<') or
                 (not turn and kletka[self.number[1]][self.number[0] - 1][2] != '>')):
            if timebank3 == '-':
                timebank3 = kletka[self.number[1]][self.number[0] - 1][2]
            timebank11 = kletka[self.number[1]][self.number[0] - 1 - atkrange][2]
            if kletka[self.number[1]][self.number[0] - 1][2] == ':' and \
                    army[self.number[1]][self.number[0] - 1][0] == '-':
                kletka[self.number[1]][self.number[0] - 1][2] = '|'
            elif army[self.number[1]][self.number[0] - 1][0] == '-':
                kletka[self.number[1]][self.number[0] - 1][2] = '!'
            if army[self.number[1]][self.number[0] - 1 - atkrange][0] != '-' and \
                    army[self.number[1]][self.number[0] - 1 - atkrange][4] != self.troop[4] and \
                    army[self.number[1]][self.number[0]][0] != '/':
                kletka[self.number[1]][self.number[0] - 1 - atkrange][2] = 'x'
        sver = False
        choosing = False
        seen = False
        kingdom = False
        font = pygame.font.Font(None, 30)
        x, y = 0, 0
        cor = (0, 0, 0, 0)
        attack = 1
        png = ''
        if self.troop[0] == '}':
            attack = 2
        elif self.troop[0] == ']':
            attack = 1
        while moving:
            if turn:
                string_rendered = font.render(str(player1_money), True, pygame.Color('white'))
            else:
                string_rendered = font.render(str(player2_money), True, pygame.Color('white'))
            Board(map, self.screen, turn).load_level()
            if self.troop[0] == '/' and kletka[self.number[1]][self.number[0]][2] == '#' and \
                    kletka[self.number[1] - 1][self.number[0]][2] != '<' and \
                    kletka[self.number[1] - 1][self.number[0]][2] != '>' and \
                    kletka[self.number[1] + 1][self.number[0]][2] != '<' and \
                    kletka[self.number[1] + 1][self.number[0]][2] != '>' and \
                    kletka[self.number[1]][self.number[0] - 1][2] != '<' and \
                    kletka[self.number[1]][self.number[0] - 1][2] != '>' and \
                    kletka[self.number[1]][self.number[0] + 1][2] != '<' and \
                    kletka[self.number[1]][self.number[0] + 1][2] != '>' and not sver:
                buildMenu_surf, buildMenu_rect = underLoad('Building.png', 'gameElements', (200, 800))
                kingdom = True
                if not seen:
                    el = 'gameElements'
                    Animation(self.screen, (0, 800), (200, 800), 1000).sliding_animation(('Building.png', el))
                    seen = True
                self.screen.blit(buildMenu_surf, buildMenu_rect)
                money_rect = string_rendered.get_rect()
                money_rect.top = 725
                money_rect.x = 25
                self.screen.blit(string_rendered, money_rect)
            else:
                sver = True
                exit_surf, exit_rect = underLoad('exit.png', 'gameElements', (50, 50))
                self.screen.blit(exit_surf, exit_rect)
            if sver and kingdom and self.troop[0] == '/':  # Проверка на существование - Свернуть
                svor_surf, svor_rect = underLoad('svor.png', 'gameElements', (150, 50))
                self.screen.blit(svor_surf, svor_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if turn:
                        color = 'blue'
                        if self.troop[0] == '/':
                            png = 'builds.png'
                        elif self.troop[0] == '}':
                            png = 'sword.png'
                        elif self.troop[0] == ']':
                            png = 'archer.png'
                    else:
                        color = 'red'
                        if self.troop[0] == '/':
                            png = 'enemyBuilds.png'
                        elif self.troop[0] == '}':
                            png = 'sword.png'
                        elif self.troop[0] == ']':
                            png = 'archer.png'
                    surf, rect = underLoad(png, os.path.join('gameElements', color),
                                           (x + 40, y + 40))
                    self.screen.blit(surf, rect)
                    choosing = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    num, cor, zn = Board(map, self.screen, player_turn).clicked(x, y)
                    if 25 < x < 175 and 100 < y < 200 and not sver:  # Проверка на взаимодействие - дом
                        if turn:
                            kletka[self.number[1]][self.number[0]][2] = ':'
                            kletka[self.number[1]][self.number[0]][3] = 'blue'
                            player1_derev += 1
                        else:
                            kletka[self.number[1]][self.number[0]][2] = ':'
                            kletka[self.number[1]][self.number[0]][3] = 'red'
                            player2_derev += 1
                        running_units.pop(running_units.index(army[self.number[1]][self.number[0]][6]) + 1)
                        running_units.pop(running_units.index(army[self.number[1]][self.number[0]][6]))
                        army[self.number[1]][self.number[0]] = ['-', (0, 0), (0, 0), None, '-', 0, 0]
                        moving = False
                    elif 25 < x < 175 and 250 < y < 350 and not sver:
                        if turn:
                            kletka[self.number[1]][self.number[0]][2] = ';'
                            kletka[self.number[1]][self.number[0]][3] = 'blue'
                            player1_zamk += 1
                        else:
                            kletka[self.number[1]][self.number[0]][2] = ';'
                            kletka[self.number[1]][self.number[0]][3] = 'red'
                            player2_zamk += 1
                        running_units.pop(running_units.index(army[self.number[1]][self.number[0]][6]) + 1)
                        running_units.pop(running_units.index(army[self.number[1]][self.number[0]][6]))
                        army[self.number[1]][self.number[0]] = ['-', (0, 0), (0, 0), None, '-', 0, 0]
                        moving = False
                    elif 100 < x < 150 and 0 < y < 50:
                        if not sver:
                            buildMenu_surf, buildMenu_rect = False, False
                            sver = True
                        elif sver and self.troop[0] == '/':
                            sver = False
                            svor_surf, svor_rect = False, False
                    elif kletka[num[1]][num[0]][2] == '!' or kletka[num[1]][num[0]][2] == '|':
                        army[num[1]][num[0]] = self.troop
                        army[num[1]][num[0]][3] = False
                        kletka[self.number[1] + 1][self.number[0]][2] = timebank
                        kletka[self.number[1] - 1][self.number[0]][2] = timebank1
                        kletka[self.number[1]][self.number[0] + 1][2] = timebank2
                        kletka[self.number[1]][self.number[0] - 1][2] = timebank3
                        running_units[running_units.index(army[num[1]][num[0]][6]) + 1][1] = cor
                        running_units[running_units.index(army[num[1]][num[0]][6]) + 1][4] = cor
                        running_units[running_units.index(army[num[1]][num[0]][6]) + 1][7] = cor
                        moving = False
                        choosing = False
                        army[self.number[1]][self.number[0]] = ['-', (0, 0), (0, 0), None, '-', 0, 0]
                        if card[num[1]][num[0]] == '<':
                            win('<', self.screen)
                        elif card[num[1]][num[0]] == '>':
                            win('>', self.screen)
                        elif (kletka[num[1]][num[0]][2] == ';' or kletka[num[1]][num[0]][2] == ':') and \
                                self.troop[4] != kletka[num[1]][num[0]][3]:
                            if self.troop[4] == 'blue' and kletka[num[1]][num[0]][2] == ';':
                                player2_zamk -= 1
                            elif self.troop[4] == 'red' and kletka[num[1]][num[0]][2] == ';':
                                player1_zamk -= 1
                            elif self.troop[4] == 'blue' and kletka[num[1]][num[0]][2] == ':':
                                player2_derev -= 1
                            elif self.troop[4] == 'red' and kletka[num[1]][num[0]][2] == ':':
                                player1_derev -= 1
                            if timebank == ';' or timebank == ':':
                                timebank = '#'
                            elif timebank1 == ';' or timebank1 == ':':
                                timebank1 = '#'
                            elif timebank2 == ';' or timebank2 == ':':
                                timebank2 = '#'
                            elif timebank3 == ';' or timebank3 == ':':
                                timebank3 = '#'
                            kletka[num[1]][num[0]] = [(0, 0), (0, 0, 0, 0), '-', '-']
                    elif kletka[num[1]][num[0]][2] == '|':
                        if turn:
                            army[num[1]][num[0]] = self.troop
                        else:
                            army[num[1]][num[0]] = self.troop
                        moving = False
                        choosing = False
                        army[self.number[1]][self.number[0]] = ['-', (0, 0), (0, 0), None, '-', 0, 0]
                    elif kletka[num[1]][num[0]][2] == 'x' and army[self.number[1]][self.number[0]][0] != '/':
                        if card[num[1]][num[0]] != '^' or army[self.number[1]][self.number[0]][0] != ']':
                            army[num[1]][num[0]][5] -= attack
                            if army[num[1]][num[0]][5] <= 0:
                                running_units.pop(running_units.index(army[num[1]][num[0]][6]) + 1)
                                running_units.pop(running_units.index(army[num[1]][num[0]][6]))
                                army[num[1]][num[0]] = ['-', (0, 0), (0, 0), None, '-', 0, 0]
                        army[self.number[1]][self.number[0]][3] = False
                        moving = False
                    if 0 < x < 50 and 0 < y < 50:
                        army[self.number[1]][self.number[0]] = self.troop
                        moving = False
            if turn:
                color = 'blue'
                if self.troop[0] == '/':
                    png = 'builds.png'
                elif self.troop[0] == '}':
                    png = 'sword.png'
                elif self.troop[0] == ']':
                    png = 'archer.png'
            else:
                color = 'red'
                if self.troop[0] == '/':
                    png = 'enemyBuilds.png'
                elif self.troop[0] == '}':
                    png = 'sword.png'
                elif self.troop[0] == ']':
                    png = 'archer.png'
            if choosing:
                surf, rect = underLoad(png, os.path.join('gameElements', color),
                                       (x + 40, y + 40))
                self.screen.blit(surf, rect)
            pygame.display.flip()
        kletka[self.number[1] + 1][self.number[0]][2] = timebank
        kletka[self.number[1] - 1][self.number[0]][2] = timebank1
        kletka[self.number[1]][self.number[0] + 1][2] = timebank2
        kletka[self.number[1]][self.number[0] - 1][2] = timebank3
        if self.troop[0] == ']':
                kletka[self.number[1] + 1][self.number[0] + 1][2] = timebank4
                kletka[self.number[1] - 1][self.number[0] + 1][2] = timebank5
                kletka[self.number[1] - 1][self.number[0] - 1][2] = timebank6
                kletka[self.number[1] + 1][self.number[0] - 1][2] = timebank7
                try:
                    kletka[self.number[1] + 2][self.number[0]][2] = timebank8
                except Exception:
                    pass
                try:
                    kletka[self.number[1] - 2][self.number[0]][2] = timebank9
                except Exception:
                    pass
                try:
                    kletka[self.number[1]][self.number[0] + 2][2] = timebank10
                except Exception:
                    pass
                try:
                    kletka[self.number[1]][self.number[0] - 2][2] = timebank11
                except Exception:
                    pass
        return cor

    def bunker(self, map):
        timebank, timebank1, timebank2, timebank3 = '-', '-', '-', '-'
        if army[self.number[1] + 1][self.number[0]][2] != '-':
            timebank = kletka[self.number[1] + 1][self.number[0]][2]
            if army[self.number[1] + 1][self.number[0]][0] != '-' and \
                    army[self.number[1] + 1][self.number[0]][4] != kletka[self.number[1]][self.number[0]][3]:
                kletka[self.number[1] + 1][self.number[0]][2] = 'x'
        if kletka[self.number[1] - 1][self.number[0]][2] != '-':
            timebank1 = kletka[self.number[1] - 1][self.number[0]][2]
            if army[self.number[1] - 1][self.number[0]][0] != '-' and \
                    army[self.number[1] - 1][self.number[0]][4] != kletka[self.number[1]][self.number[0]][3]:
                kletka[self.number[1] - 1][self.number[0]][2] = 'x'
        if kletka[self.number[1]][self.number[0] - 1][2] != '-':
            timebank2 = kletka[self.number[1]][self.number[0] - 1][2]
            if army[self.number[1]][self.number[0] - 1][0] != '-' and \
                    army[self.number[1]][self.number[0] - 1][4] != kletka[self.number[1]][self.number[0]][3]:
                kletka[self.number[1]][self.number[0] - 1][2] = 'x'
        if kletka[self.number[1]][self.number[0] + 1][2] != '-':
            timebank3 = kletka[self.number[1]][self.number[0] + 1][2]
            if army[self.number[1]][self.number[0] + 1][0] != '-' and \
                    army[self.number[1]][self.number[0] + 1][4] != kletka[self.number[1]][self.number[0]][3]:
                kletka[self.number[1]][self.number[0] + 1][2] = 'x'
        housemovin = True
        while housemovin:
            Board(map, self.screen, player_turn).load_level()
            exit_surf, exit_rect = underLoad('exit.png', 'gameElements', (50, 50))
            self.screen.blit(exit_surf, exit_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    num, cor, zn = Board(map, self.screen, player_turn).clicked(x, y)
                    if kletka[num[1]][num[0]][2] == 'x':
                        army[num[1]][num[0]][5] -= 1
                        if army[num[1]][num[0]][5] <= 0:
                            running_units.pop(running_units.index(army[num[1]][num[0]][6]) + 1)
                            running_units.pop(running_units.index(army[num[1]][num[0]][6]))
                            army[num[1]][num[0]] = ['-', (0, 0), (0, 0), None, '-', 0, 0]
                    housemovin = False
                    if 0 < x < 50 and 0 < y < 50:
                        housemovin = False
            pygame.display.flip()
        kletka[self.number[1] + 1][self.number[0]][2] = timebank
        kletka[self.number[1] - 1][self.number[0]][2] = timebank1
        kletka[self.number[1]][self.number[0] - 1][2] = timebank2
        kletka[self.number[1]][self.number[0] + 1][2] = timebank3


class Animation:
    def __init__(self, screen, start_pos, end_pos, speed):
        self.screen = screen
        self.start_x, self.start_y = start_pos[0], start_pos[1]
        self.end_x, self.end_y = end_pos[0], end_pos[1]
        self.speed = speed

    def sliding_animation(self, object):
        clock = pygame.time.Clock()
        fps = 60
        x_pos = self.start_x
        if len(object) == 2:
            while x_pos < self.end_x:
                surf, rect = None, None
                x_pos += self.speed / fps
                clock.tick(fps)
                surf, rect = underLoad(object[0], object[1], (x_pos, self.start_y))
                self.screen.blit(surf, rect)
                pygame.display.flip()

    def running_animation(self, turn, objects):
        fps = 60
        result = []
        for i in range(3):
            plavx, plavy = objects[i * 3 + 2][0], objects[i * 3 + 2][1]
            objects[i * 3][0] += self.speed * plavx / fps
            objects[i * 3][1] += self.speed * plavy / fps
            if objects[i * 3][0] <= objects[1][0]:
                plavx = 1
            elif objects[i * 3][0] >= objects[1][2]:
                plavx = -1
            if objects[i * 3][1] <= objects[1][1]:
                plavy = 1
            elif objects[i * 3][1] >= objects[1][3]:
                plavy = -1
            result.append([objects[i * 3][0], objects[i * 3][1]])
            result.append([objects[1][0], objects[1][1], objects[1][2], objects[1][3]])
            result.append([plavx, plavy])
            pygame.draw.circle(self.screen, objects[-1], (objects[i * 3][0], objects[i * 3][1]), 5)
        result.append(objects[-1])
        return result


def next_turn():
    global player_turn, player1_money, player2_money, player1_derev, player2_derev, player1_zamk, player2_zamk
    for i in range(len(army)):
        for i1 in range(len(army[i])):
            if army[i][i1][3] is None:
                pass
            elif army[i][i1][3] is False:
                army[i][i1][3] = True
    if player_turn:
        player_turn = False
        player1_money = player1_money + 20 + 10 * player1_derev - 30 * player1_zamk
    else:
        player_turn = True
        player2_money = player2_money + 20 + 10 * player2_derev - 30 * player2_zamk


def pause(screen):
    global notex, boarder
    contin = False
    x, y = 0, 0
    men_surf, men_rect = underLoad('openmenu.png', 'gameElements', (600, 600))
    boarder_surf, boarder_rect = underLoad('boraderswitch.png', 'gameElements', (550, 590))
    while notex:
        screen.blit(men_surf, men_rect)
        if 250 < x < 550 and 450 < y < 530:
            ex_surf, ex_rect = underLoad('menuexit2.png', 'gameElements', (550, 530))
        else:
            ex_surf, ex_rect = underLoad('menuexit1.png', 'gameElements', (550, 530))
        if 250 < x < 550 and 350 < y < 430:
            con_surf, con_rect = underLoad('menuprod2.png', 'gameElements', (550, 430))
        else:
            con_surf, con_rect = underLoad('menuprod1.png', 'gameElements', (550, 430))
        if boarder:
            hal_surf, hal_rect = underLoad('hal.png', 'gameElements', (310, 590))
        else:
            hal_surf, hal_rect = None, None
        screen.blit(ex_surf, ex_rect)
        screen.blit(con_surf, con_rect)
        screen.blit(boarder_surf, boarder_rect)
        if hal_surf is not None:
            screen.blit(hal_surf, hal_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 250 < x < 550 and 450 < y < 530:
                    restart()
                    notex = False
                elif 300 < x < 550 and 350 < y < 430:
                    notex = False
                    contin = True
                elif 250 < x < 300 and 540 < y < 590:
                    if boarder:
                        boarder = False
                    else:
                        boarder = True
        pygame.display.flip()
    if contin:
        notex = True


def win(winner, screen):
    global notex
    x, y = 0, 0
    while notex:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 250 < x < 550 and 450 < y < 530:
                    restart()
                    notex = False
        if winner == '>':
            men_surf, men_rect = underLoad('winblue.png', 'gameElements', (600, 600))
        else:
            men_surf, men_rect = underLoad('winred.png', 'gameElements', (600, 600))
        if 250 < x < 550 and 450 < y < 530:
            ex_surf, ex_rect = underLoad('menuexit2.png', 'gameElements', (550, 530))
        else:
            ex_surf, ex_rect = underLoad('menuexit1.png', 'gameElements', (550, 530))
        screen.blit(men_surf, men_rect)
        screen.blit(ex_surf, ex_rect)
        pygame.display.flip()


Windows((800, 800)).menu()
