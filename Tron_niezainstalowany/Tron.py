# -*- coding: utf-8 -*-
__author__ = 'Krzysztof Szczurek'

import pygame, time

pygame.init()
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_BLUE = (0,100,250)

displayWidth=800
displayHeight=600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

pygame.display.set_caption('Tron: First Chapter')

icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

block_size=10
FPS=20

Bum = pygame.image.load('Wybuch.png')
Blue_player = pygame.image.load('Blue_player.png')
Red_player = pygame.image.load('Red_player.png')

Players={}
Players[BLUE]=Blue_player
Players[RED]=Red_player

reverse={}
reverse['left'] = 'right'
reverse['right'] = 'left'
reverse['up'] = 'down'
reverse['down'] = 'up'


def Draw_Tron(block_size, TronData, color, direction):
    if direction == 'right':
        Player = pygame.transform.rotate(Players[color],270)
    elif direction == 'down':
        Player = pygame.transform.rotate(Players[color],180)
    elif direction == 'left':
        Player = pygame.transform.rotate(Players[color],90)
    elif direction == 'up':
        Player = Players[color]

    gameDisplay.blit(Player, (TronData[-1][0],TronData[-1][1]))
    for XandY in TronData[:-1]:
        pygame.draw.rect(gameDisplay, color, [XandY[0],XandY[1],block_size,block_size])

def Display_for_time(img, coordinates, seconds):
    gameDisplay.blit(img, coordinates)
    pygame.display.update()
    time.sleep(seconds)


def message_to_screen(msg,color,size,font_type='comicsansms',x_displace=0, y_displace=0):
    font = pygame.font.SysFont(font_type, size)
    textSurf = font.render(msg, True, color)
    textRect = textSurf.get_rect()
    textRect.center = (displayWidth/2)+x_displace, (displayHeight/2)+y_displace
    gameDisplay.blit(textSurf, textRect )

def Make_Button(coordinates, x_length, y_length, text, button_color, text_color=BLACK, action = None):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if coordinates[0]+x_length > pos[0] > coordinates[0] and coordinates[1]+y_length > pos [1] > coordinates[1] and click[0]==1 and action!= None:
        if action == 'Play':
            GameLoop()
        elif action == 'Quit':
            pygame.quit()
            quit()
        elif action == 'Controls':
            Controls_Screen()
        elif action == 'Menu':
            GameIntro()
    pygame.draw.rect(gameDisplay, button_color, [coordinates[0],coordinates[1],x_length, y_length])
    x_displace=-(displayWidth/2-(displayWidth/2-(displayWidth/2-coordinates[0])+(x_length/2)))
    y_displace=(coordinates[1]+y_length/2)-displayHeight/2
    message_to_screen(text,text_color,int(y_length/4),'comicsansms',x_displace, y_displace)


def change_direction(last_direction, direction, lead_x_change, lead_y_change, block_size):
    if reverse[direction] == last_direction:
        return lead_x_change, lead_y_change
    else:
        if direction == 'left':
            lead_x_change = -block_size
            lead_y_change = 0
            return lead_x_change, lead_y_change
        elif direction == 'right':
            lead_x_change = block_size
            lead_y_change = 0
            return lead_x_change, lead_y_change
        elif direction == 'up':
            lead_y_change = -block_size
            lead_x_change = 0
            return lead_x_change, lead_y_change
        elif direction == 'down':
            lead_y_change = block_size
            lead_x_change = 0
            return lead_x_change, lead_y_change

def Controls_Screen():

    c_screen = True

    while c_screen==True:
        gameDisplay.fill(WHITE)
        message_to_screen('Gracz niebieski porusza się za pomocą znaków WSAD', BLACK, 25, y_displace=-20)
        message_to_screen('Gracz czerwony porusza się za pomocą strzałek', BLACK, 25, y_displace=20)
        Make_Button((350,450),100, 50,'MENU', LIGHT_BLUE,action='Menu')
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

def GameIntro():
    intro = True

    while intro:
        gameDisplay.fill(WHITE)
        message_to_screen('Witaj w grze Tron: First Chapter!', GREEN, 40, y_displace=-150)
        message_to_screen('Twoim zadaniem jest jak najdłużej utrzymać się na torze,', BLACK, 25, y_displace=-70)
        message_to_screen('Jeśli wpadniesz na samego siebie, przeciwnika', BLACK, 25, y_displace=-40)
        message_to_screen( 'lub poza tor przegrywasz!', BLACK, 25, y_displace=-10)
        message_to_screen('Aby zacząć kliknij START', BLACK, 25, y_displace=20)
        message_to_screen('Jesteś gotów?', GREEN, 35, y_displace=105)
        Make_Button((150,500), 100, 50, 'START', GREEN,action= 'Play')
        Make_Button((350,500), 100, 50, 'STEROWANIE',LIGHT_BLUE, action = 'Controls')
        Make_Button((550,500), 100, 50, 'WYJŚCIE', RED, action = 'Quit')
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                                
def GameLoop():
    gameExit = False
    gameOver = False

    direction1='right'
    direction2='left'

    last_direction=direction1
    last_direction2=direction2

    Tron1 = []
    Tron2 = []

    lead_x_change = block_size
    lead_y_change = 0

    lead_x_change2 = -block_size
    lead_y_change2 = 0

    lead_x=displayWidth/4
    lead_y=displayHeight/2

    lead_x2=(displayWidth/4)*3
    lead_y2=(displayHeight/2)

    Winner = ''

    while not gameExit:
        if gameOver==True:
            if Winner == 'Player2':
                Display_for_time(Bum, (lead_x, lead_y), 0.25)
            elif Winner == 'Player1':
                Display_for_time(Bum, (lead_x2, lead_y2), 0.25)
            elif Winner == 'Draw':
                Display_for_time(Bum, (lead_x2, lead_y2), 0.25)

        while gameOver == True:
            gameDisplay.fill(WHITE)
            message_to_screen('Game Over', RED, y_displace=-50, size=50)
            if Winner == 'Player2':
                message_to_screen('Gracz czerwony wygrał!', GREEN, size = 30)
            elif Winner == 'Player1':
                message_to_screen('Gracz niebieski wygrał!', GREEN, size = 30)
            elif Winner == 'Draw':
                message_to_screen('Remis!',GREEN, size = 30)
            message_to_screen('Wciśnij SPACJĘ aby zagrać jeszcze raz, Q aby wyjść',BLACK, y_displace=50, size=30)
            message_to_screen('lub też M aby wrócić do MENU',BLACK, y_displace=90, size=30)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_SPACE:
                        GameLoop()
                    elif event.key== pygame.K_m:
                        GameIntro()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    direction1 = 'left'
                    lead_x_change, lead_y_change = change_direction(last_direction,direction1,lead_x_change, lead_y_change, block_size)
                    last_direction=direction1
                elif event.key == pygame.K_d:
                    direction1 = 'right'
                    lead_x_change, lead_y_change = change_direction(last_direction,direction1,lead_x_change, lead_y_change, block_size)
                    last_direction=direction1
                elif event.key == pygame.K_w:
                    direction1 = 'up'
                    lead_x_change, lead_y_change = change_direction(last_direction,direction1,lead_x_change, lead_y_change, block_size)
                    last_direction=direction1
                elif event.key == pygame.K_s:
                    direction1 = 'down'
                    lead_x_change, lead_y_change = change_direction(last_direction,direction1,lead_x_change, lead_y_change, block_size)
                    last_direction=direction1


                if event.key == pygame.K_LEFT:
                    direction2 = 'left'
                    lead_x_change2, lead_y_change2 = change_direction(last_direction2,direction2,lead_x_change2, lead_y_change2, block_size)
                    last_direction2=direction2
                elif event.key == pygame.K_RIGHT:
                    direction2 = 'right'
                    lead_x_change2, lead_y_change2 = change_direction(last_direction2,direction2,lead_x_change2, lead_y_change2, block_size)
                    last_direction2=direction2
                elif event.key == pygame.K_UP:
                    direction2 = 'up'
                    lead_x_change2, lead_y_change2 = change_direction(last_direction2,direction2,lead_x_change2, lead_y_change2, block_size)
                    last_direction2=direction2
                elif event.key == pygame.K_DOWN:
                    direction2 = 'down'
                    lead_x_change2, lead_y_change2 = change_direction(last_direction2,direction2,lead_x_change2, lead_y_change2, block_size)
                    last_direction2=direction2

        if lead_x >= displayWidth or lead_x < 0 or lead_y < 0 or lead_y >= displayHeight:
             gameOver=True
             Winner = 'Player2'

        if lead_x2 >= displayWidth or lead_x2 < 0 or lead_y2 < 0 or lead_y2 >= displayHeight:
             gameOver=True
             Winner = 'Player1'

        lead_x += lead_x_change
        lead_y += lead_y_change

        lead_x2 += lead_x_change2
        lead_y2 += lead_y_change2

        gameDisplay.fill(WHITE)

        Actual_block1 = []
        Actual_block1.append(lead_x)
        Actual_block1.append(lead_y)
        Tron1.append(Actual_block1)

        Actual_block2 = []
        Actual_block2.append(lead_x2)
        Actual_block2.append(lead_y2)
        Tron2.append(Actual_block2)

        Draw_Tron(block_size,Tron1, BLUE, direction1)
        Draw_Tron(block_size,Tron2, RED, direction2)
        pygame.display.update()

        Condition1 = False
        Condition2 = False

        for XandY in Tron2:
            if lead_x == XandY[0] and lead_y == XandY[1]:
                Condition1 = True
                Winner = 'Player2'
                gameOver = True

        for Segment in Tron1[:-1]:
            if Segment == Actual_block1:
                Winner = 'Player2'
                gameOver=True

        if Winner == 'Player2':
            if lead_x2 == lead_x and lead_y2 == lead_y:
                Condition2 = True
        else:
            for XandY in Tron1:
                if lead_x2 == XandY[0] and lead_y2 == XandY[1]:
                    Condition2 = True
                    Winner = 'Player1'
                    gameOver = True

            for Segment in Tron2[:-1]:
                if Segment == Actual_block2:
                    Winner = 'Player1'
                    gameOver=True

        Winner = 'Draw' if Condition1 == True and Condition2 == True else Winner

        clock.tick(FPS)

    pygame.quit()
    quit()

GameIntro()
