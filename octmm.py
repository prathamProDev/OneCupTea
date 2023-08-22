import os
import pygame
import sys
import json
import oct

datasrc = open('data.json')
data = json.load(datasrc)

title = data['title']
icon = pygame.image.load(data['icon'])
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(title)
pygame.display.set_icon(icon)

class octmainmenu:

    # Main menu of game

    def main_menu():
        while True:
            oct.draw(oct.BACKGROUND, 0, 0)

            MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = pygame.transform.scale(
                oct.FONT.render("MAIN MENU", True, "#000000"), (180, 40))
            MENU_RECT = MENU_TEXT.get_rect(
                center=(WIDTH / 2, HEIGHT / 2 - 100))

            PLAY_BUTTON = oct.Button(image=pygame.transform.scale(pygame.image.load("images/play_btn.png"), (180, 140)), pos=(500, 300),
                                 text_input="", font=oct.get_font(75), base_color="#d7fcd4", hovering_color="white")
            PLAY_ENDLESS_BUTTON = oct.Button(image=pygame.transform.scale(pygame.image.load("images/play_endless_btn.png"), (180, 140)), pos=(500, 380),
                                         text_input="", font=oct.get_font(75), base_color="#d7fcd4", hovering_color="white")

            WIN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(WIN)
            for button in [PLAY_ENDLESS_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(WIN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("money.json", "r+") as dmf:
                        json.dump(oct.dataMoney, dmf)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MOUSE_POS):
                        oct.octgame.main()
                    if PLAY_ENDLESS_BUTTON.checkForInput(MOUSE_POS):
                        oct.octgame.endless()

            pygame.display.update()
