import pygame
from network import Network
from button import Button
from bcolors import BColors as bc
pygame.font.init()

# === GLOBAL VARIABLES === #

client_number = 0

buttons = [Button("Rock", 25, 300, (0, 0, 0)),
           Button("Scissor", 187.5, 300, (255, 0, 0)),
           Button("Paper", 350, 300, (0, 255, 0))]

# ======================== #

# Creating a Canvas/Window #
width = 500
height = 500
display_size = (width, height)

win = pygame.display.set_mode(display_size)

pygame.display.set_caption("Client")
# ======================== #


def redraw_window(win, game, player):
    win.fill((255, 255, 255))

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Waiting for a Player", True, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Your move", True, (0, 255, 255))
        win.blit(text, (25, 100))

        text = font.render("Opponent's move", True, (0, 255, 255))
        win.blit(text, (237.5, 100))

        move_1 = game.get_player_move(0)
        move_2 = game.get_player_move(1)

        if game.both_went():
            text_1 = font.render(move_1, True, (0, 0, 0))
            text_2 = font.render(move_2, True, (0, 0, 0))
        else:
            if game.p1_went and player == 0:
                text_1 = font.render(move_1, True, (0, 0, 0))
            elif game.p1_went:
                text_1 = font.render("Locked In", True, (0, 0, 0))
            else:
                text_1 = font.render("Waiting...", True, (0, 0, 0))

            if game.p2_went and player == 1:
                text_2 = font.render(move_2, True, (0, 0, 0))
            elif game.p2_went:
                text_2 = font.render("Locked In", True, (0, 0, 0))
            else:
                text_2 = font.render("Waiting...", True, (0, 0, 0))

        if player == 1:
            win.blit(text_2, (35, 200))
            win.blit(text_1, (275, 200))
        else:
            win.blit(text_1, (35, 200))
            win.blit(text_2, (275, 200))

        for button in buttons:
            button.draw(win)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_p())
    print(f"You are player {player}")

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print(bc.FAIL + "Couldn't get game." + bc.END)
            break

        if game.both_went():
            redraw_window(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print(bc.FAIL + "Couldn't get game." + bc.END)
                break

            font = pygame.font.SysFont("comicsans", 70)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", True, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", True, (255, 0, 0))
            else:
                text = font.render("You Lost!", True, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1_went:
                                n.send(button.text)
                        else:
                            if not game.p2_went:
                                n.send(button.text)

        redraw_window(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    win.fill((128, 128, 128))
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Click to Play!", True, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


# Initializing the game
while True:
    menu_screen()
