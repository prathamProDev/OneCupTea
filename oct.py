import os
import pygame
import sys
import json
import time
import random
from tkinter import messagebox
from button import Button
import octmm

pygame.init()
pygame.font.init()
pygame.mixer.init()

# json files

datasrc = open('data.json')
data = json.load(datasrc)

dataMoney = {
    "coins": 0
}


with open("money.json", "r+") as dmf:
    dataMoney = json.load(dmf)

# Properties of images and window

title = data['title']
icon = pygame.image.load(data['icon'])
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(title)
pygame.display.set_icon(icon)

BACKGROUND = pygame.transform.scale(
    pygame.image.load(data['background-img']), (WIDTH, HEIGHT))
GASTOVE = pygame.image.load(data['gastove'])
gastove_width = 348
CUP = pygame.transform.scale(pygame.image.load(data['cup']), (50, 40))
cup_rect = CUP.get_rect()

FONT = pygame.font.Font("./font/Square.ttf", 30)


STONE = pygame.image.load(data['stone'])
stone_rect = STONE.get_rect()

SUGAR = pygame.image.load(data['sugar'])
sugar_rect = SUGAR.get_rect()

TEA_LEAVES = pygame.image.load(data['tea_leaves'])
tea_leaves_rect = TEA_LEAVES.get_rect()

MILK = pygame.image.load(data['milk'])
milk_rect = MILK.get_rect()

WATER = pygame.image.load(data['water'])
water_rect = WATER.get_rect()

item_size = 50
item_fall_limit_right = 95
item_fall_limit_left = 280

# sounds

s = 'sounds'

cup_breaking_sound = pygame.mixer.Sound(os.path.join(s, 'cup-breaking-sound.mp3'))
item_collect_sound = pygame.mixer.Sound(os.path.join(s, 'item-collect-sound.mp3'))
tea_was_made_sound = pygame.mixer.Sound(os.path.join(s, 'tea-made-sound.wav'))
countless_mode_coin_collect_sound = pygame.mixer.Sound(os.path.join(s, 'countless-mode-coin-collect-sound.wav'))


def draw(image, coordix, coordiy):
    WIN.blit(image, (coordix, coordiy))


def get_font(size):
    return pygame.font.Font("./font/Square.ttf", size)

# Start of game


class octgame:

# Main Mode

    def main():

        MOUSE_POS = pygame.mouse.get_pos()

        STOP_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/stop_btn.png"), (100, 60)), pos=(800, 100), text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="white")

        cup_x = 450
        cup_y = 510
        CUP_X_ADDITION = 5
        gastove_x = 300

        add_number = 1

        item_x = gastove_width + round(random.uniform(item_size //
                              2, gastove_x - item_size // 2))
        stone_y = -item_size
        stone_speed = 10

        sugar_x = gastove_width + round(random.uniform(item_size //
                              2, gastove_x - item_size // 2))
        sugar_y = -item_size
        sugar_speed = 5
        sugar_count = []

        tea_leaves_x = gastove_width + \
            round(random.uniform(item_size // 2,
                  gastove_x - item_size // 2))
        tea_leaves_y = -item_size
        tea_leaves_speed = 3
        tea_leaves_count = []

        milk_x = gastove_width + round(random.uniform(item_size //
                             2, gastove_x - item_size // 2))
        milk_y = -item_size
        milk_speed = 7
        milk_count = []

        water_x = gastove_width + round(random.uniform(item_size //
                              2, gastove_x - item_size // 2))
        water_y = -item_size
        water_speed = 7
        water_count = []

        clock = pygame.time.Clock()
        start_time = time.time()
        passed_time = 0

        def addItems(number, count):
            number + 1
            count.append(number)

        def upPos():
            # update cup_rect position
            cup_rect.move_ip(cup_x - cup_rect.x, cup_y - cup_rect.y)
            stone_rect.move_ip(item_x - stone_rect.x, stone_y - stone_rect.y)
            sugar_rect.move_ip(sugar_x - sugar_rect.x, sugar_y - sugar_rect.y)
            tea_leaves_rect.move_ip(tea_leaves_x - tea_leaves_rect.x, tea_leaves_y - tea_leaves_rect.y)
            milk_rect.move_ip(milk_x - milk_rect.x, milk_y - milk_rect.y)
            water_rect.move_ip(water_x - water_rect.x, water_y - water_rect.y)

        while True:
            MONEY_TEXT = FONT.render(f"Coins: {dataMoney['coins']}", 1, "black")

            clock.tick(60)
            passed_time = time.time() - start_time
            seconds = round(passed_time) % 60
            minutes = int(round(passed_time) / 60) % 60
            hours = int(round(passed_time) / 3600)

            pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("money.json", "r+") as dmf:
                        json.dump(dataMoney, dmf)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if STOP_BUTTON.checkForInput(MOUSE_POS):
                        octmm.octmainmenu.main_menu()

            TIME_TEXT = FONT.render(f"Time: {hours}:{minutes:02}:{seconds:02}", 1, "black")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and cup_x >= gastove_x + 20:
                cup_x -= CUP_X_ADDITION
            if keys[pygame.K_RIGHT] and cup_x <= gastove_x + gastove_x+15:
                cup_x += CUP_X_ADDITION
            if keys[pygame.K_SPACE]:
                startormm = messagebox.askyesno("One Cup Tea", "The game is paused, click yes to start or no to go to main menu.")
                if not startormm:
                    octmm.octmainmenu.main_menu()

            draw(BACKGROUND, 0, 0)
            draw(GASTOVE, 300, 325)
            
            for button in [STOP_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(WIN)

            if stone_y > HEIGHT:
                item_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                stone_y = -item_size

            if sugar_y > HEIGHT:
                sugar_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                sugar_y = -item_size

            if tea_leaves_y > HEIGHT:
                tea_leaves_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                tea_leaves_y = -item_size

            if milk_y > HEIGHT:
                milk_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                milk_y = -item_size

            if water_y > HEIGHT:
                water_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                water_y = -item_size

            upPos()

            SUGAR_COUNT_TEXT = FONT.render(
                f"Sugar: {len(sugar_count)}/15", 1, "black")
            TEA_LEAVES_COUNT_TEXT = FONT.render(
                f"Tea leaves: {len(tea_leaves_count)}/6", 1, "black")
            MILK_COUNT_TEXT = FONT.render(
                f"Milk: {len(milk_count)}/20", 1, "black")
            WATER_COUNT_TEXT = FONT.render(
                f"Water: {len(water_count)}/20", 1, "black")

            if cup_rect.colliderect(sugar_rect):
                item_collect_sound.play()
                sugar_y = HEIGHT + item_size
                addItems(add_number, sugar_count)

            if cup_rect.colliderect(tea_leaves_rect):
                item_collect_sound.play()
                tea_leaves_y = HEIGHT + item_size
                addItems(add_number, tea_leaves_count)

            if cup_rect.colliderect(milk_rect):
                item_collect_sound.play()
                milk_y = HEIGHT + item_size
                addItems(add_number, milk_count)

            if cup_rect.colliderect(water_rect):
                item_collect_sound.play()
                water_y = HEIGHT + item_size
                addItems(add_number, water_count)

            if cup_rect.colliderect(stone_rect):
                cup_breaking_sound.play()
                cup_broke_msg = messagebox.askretrycancel(
                    "One Cup Tea", "The cup broke.\nDon't let the stones touch the cup, or else the cup will be broken. You need to pay 10 coins for cup.")
                if cup_broke_msg == True:
                    if (dataMoney["coins"] == 0):
                        coin_warning = messagebox.askokcancel(
                            "One Cup Tea", "There are no coins play in countless mode first to earn some coins. Press Ok to play in countless mode or Cancel to open main menu.")
                        if coin_warning == True:
                            octgame.countless()
                        elif coin_warning == False:
                            octmm.octmainmenu.main_menu()
                    else:
                        print("Retried")
                        dataMoney["coins"] -= 10
                        octgame.main()
                elif cup_broke_msg == False:
                    if (dataMoney["coins"] != 0):
                        dataMoney["coins"] -= 10
                    octmm.octmainmenu.main_menu()
                    print("Quitted")

            draw(STONE, item_x, stone_y)
            if (len(sugar_count) <= 15):
                draw(SUGAR, sugar_x, sugar_y)
            else:
                extra_sugar = messagebox.askretrycancel(
                    "One Cup Tea", "You added more sugar than required.")
                if (extra_sugar == True):
                    octgame.main()
                if (extra_sugar == False):
                    octmm.octmainmenu.main_menu()
            if (len(milk_count) <= 20):
                draw(MILK, milk_x, milk_y)
            else:
                extra_milk = messagebox.askretrycancel(
                    "One Cup Tea", "You added more milk than required.")
                if (extra_milk == True):
                    octgame.main()
                if (extra_milk == False):
                    octmm.octmainmenu.main_menu()
            if (len(water_count) <= 20):
                draw(WATER, water_x, water_y)
            else:
                extra_water = messagebox.askretrycancel(
                    "One Cup Tea", "You added more water than required.")
                if (extra_water == True):
                    octgame.main()
                if (extra_water == False):
                    octmm.octmainmenu.main_menu()
            if (len(tea_leaves_count) <= 6):
                draw(TEA_LEAVES, tea_leaves_x, tea_leaves_y)
            else:
                extra_tea_leaves = messagebox.askretrycancel(
                    "One Cup Tea", "You added more tea leaves than required.")
                if (extra_tea_leaves == True):
                    octgame.main()
                if (extra_tea_leaves == False):
                    octmm.octmainmenu.main_menu()

            if (len(sugar_count) == 15) and (len(tea_leaves_count) == 6) and (len(milk_count) == 20) and (len(water_count) == 20):
                tea_was_made_sound.play()
                tea_was_made = messagebox.askokcancel(
                    "One Cup Tea", "A cup of tea was made.\nYou get 10 coins!\nClick on Ok to continue or cancel to quit.")
                print("A cup of tea was made")
                dataMoney['coins'] += 100
                if tea_was_made == True:
                    octgame.main()
                if tea_was_made == False:
                    octmm.octmainmenu.main_menu()

            draw(MONEY_TEXT, 700, 20)
            draw(CUP, cup_x, cup_y)
            draw(TIME_TEXT, 10, 10)
            draw(SUGAR_COUNT_TEXT, 10, 40)
            draw(TEA_LEAVES_COUNT_TEXT, 10, 70)
            draw(MILK_COUNT_TEXT, 10, 100)
            draw(WATER_COUNT_TEXT, 10, 130)

            stone_y += stone_speed
            sugar_y += sugar_speed
            tea_leaves_y += tea_leaves_speed
            milk_y += milk_speed
            water_y += water_speed

            pygame.display.update()

#countless Mode

    def countless():

        MOUSE_POS = pygame.mouse.get_pos()

        STOP_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/stop_btn.png"), (100, 60)), pos=(800, 100), text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="white")

        cup_x = 450
        cup_y = 510
        CUP_X_ADDITION = 5
        gastove_x = 300

        item_x = gastove_width + round(random.uniform(item_size //
                              2, gastove_x - item_size // 2))
        stone_y = -item_size
        stone_speed = 10

        add_number = 1
        sugar_x = gastove_width + round(random.uniform(item_size //
                              2, gastove_x - item_size // 2))
        sugar_y = -item_size
        sugar_speed = 5
        sugar_count = []

        add_number = 1
        tea_leaves_x = gastove_width + \
            round(random.uniform(item_size // 2,
                  gastove_x - item_size // 2))
        tea_leaves_y = -item_size
        tea_leaves_speed = 3
        tea_leaves_count = []

        add_number = 1
        milk_x = gastove_width + round(random.uniform(item_size //
                             2, gastove_x - item_size // 2))
        milk_y = -item_size
        milk_speed = 7
        milk_count = []

        add_number = 1
        water_x = gastove_width + round(random.uniform(item_size //
                              2, gastove_x - item_size // 2))
        water_y = -item_size
        water_speed = 7
        water_count = []

        clock = pygame.time.Clock()
        start_time = time.time()
        passed_time = 0
        match_count = 1

        def addItems(number, count):
            number + 1
            count.append(number)

        def upPos():
            # update cup_rect position
            cup_rect.move_ip(cup_x - cup_rect.x, cup_y - cup_rect.y)
            stone_rect.move_ip(item_x - stone_rect.x, stone_y - stone_rect.y)
            sugar_rect.move_ip(sugar_x - sugar_rect.x, sugar_y - sugar_rect.y)
            tea_leaves_rect.move_ip(
                tea_leaves_x - tea_leaves_rect.x, tea_leaves_y - tea_leaves_rect.y)
            milk_rect.move_ip(milk_x - milk_rect.x, milk_y - milk_rect.y)
            water_rect.move_ip(water_x - water_rect.x, water_y - water_rect.y)

        while True:
            MONEY_TEXT = FONT.render(f"Coins: {dataMoney['coins']}", 1, "black")

            clock.tick(60)
            passed_time = time.time() - start_time
            seconds = round(passed_time) % 60
            minutes = int(round(passed_time) / 60) % 60
            hours = int(round(passed_time) / 3600)

            pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("money.json", "r+") as dmf:
                        json.dump(dataMoney, dmf)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if STOP_BUTTON.checkForInput(MOUSE_POS):
                        octmm.octmainmenu.mainmenu()

            TIME_TEXT = FONT.render(f"Time: {hours}:{minutes:02}:{seconds:02}", 1, "black")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and cup_x >= gastove_x + 20:
                cup_x -= CUP_X_ADDITION
            if keys[pygame.K_RIGHT] and cup_x <= gastove_x + gastove_x+15:
                cup_x += CUP_X_ADDITION
            if keys[pygame.K_SPACE]:
                startormm = messagebox.askyesno("One Cup Tea", "The game is paused, click yes to start or no to go to main menu.")
                if not startormm:
                    octmm.octmainmenu.main_menu()

            draw(BACKGROUND, 0, 0)
            draw(GASTOVE, 300, 325)

            for button in [STOP_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(WIN)

            if stone_y > HEIGHT:
                item_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                stone_y = -item_size

            if sugar_y > HEIGHT:
                sugar_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                sugar_y = -item_size

            if tea_leaves_y > HEIGHT:
                tea_leaves_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                tea_leaves_y = -item_size

            if milk_y > HEIGHT:
                milk_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                milk_y = -item_size

            if water_y > HEIGHT:
                water_x = item_fall_limit_left + \
                    round(random.uniform(item_size,
                          (gastove_x + item_fall_limit_right) - item_size))
                water_y = -item_size

            upPos()
            SUGAR_COUNT_TEXT = FONT.render(
                f"Sugar: {len(sugar_count)}", 1, "black")
            TEA_LEAVES_COUNT_TEXT = FONT.render(
                f"Tea leaves: {len(tea_leaves_count)}", 1, "black")
            MILK_COUNT_TEXT = FONT.render(
                f"Milk: {len(milk_count)}", 1, "black")
            WATER_COUNT_TEXT = FONT.render(
                f"Water: {len(water_count)}", 1, "black")

            if cup_rect.colliderect(sugar_rect):
                item_collect_sound.play()
                sugar_y = HEIGHT + item_size
                addItems(add_number, sugar_count)

            if cup_rect.colliderect(tea_leaves_rect):
                item_collect_sound.play()
                tea_leaves_y = HEIGHT + item_size
                addItems(add_number, tea_leaves_count)

            if cup_rect.colliderect(milk_rect):
                item_collect_sound.play()
                milk_y = HEIGHT + item_size
                addItems(add_number, milk_count)

            if cup_rect.colliderect(water_rect):
                item_collect_sound.play()
                water_y = HEIGHT + item_size
                addItems(add_number, water_count)

            if cup_rect.colliderect(stone_rect):
                cup_breaking_sound.play()
                cup_broke_msg = messagebox.askretrycancel(
                    "One Cup Tea", "The cup broke.\nDon't let the stones touch the cup, or else the cup will be broken.")
                if cup_broke_msg == True:
                    octgame.countless()
                    print("Retried")
                elif cup_broke_msg == False:
                    octmm.octmainmenu.main_menu()
                    print("Quitted")

            if (len(sugar_count) >= match_count) and (len(milk_count) >= match_count) and (len(water_count) >= match_count) and (len(tea_leaves_count) >= match_count):
                draw(SUGAR, sugar_x, sugar_y)
                draw(MILK, milk_x, milk_y)
                draw(WATER, water_x, water_y)
                draw(TEA_LEAVES, tea_leaves_x, tea_leaves_y)
                dataMoney["coins"] += 10
                countless_mode_coin_collect_sound.play()
                match_count += 1

            draw(MONEY_TEXT, 700, 20)
            draw(CUP, cup_x, cup_y)
            draw(TIME_TEXT, 10, 10)
            draw(STONE, item_x, stone_y)
            draw(SUGAR, sugar_x, sugar_y)
            draw(MILK, milk_x, milk_y)
            draw(WATER, water_x, water_y)
            draw(TEA_LEAVES, tea_leaves_x, tea_leaves_y)
            draw(SUGAR_COUNT_TEXT, 10, 40)
            draw(TEA_LEAVES_COUNT_TEXT, 10, 70)
            draw(MILK_COUNT_TEXT, 10, 100)
            draw(WATER_COUNT_TEXT, 10, 130)

            stone_y += stone_speed
            sugar_y += sugar_speed
            tea_leaves_y += tea_leaves_speed
            milk_y += milk_speed
            water_y += water_speed

            pygame.display.update()


pygame.display.flip()
octmm.octmainmenu.main_menu()