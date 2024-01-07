import pygame
import time
import random

pygame.font.init()

# Screen attributes
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid colliding with Jude")

# Background variable
BG = pygame.transform.scale(pygame.image.load("road.png"), (WIDTH, HEIGHT))

# Setting a variable for the pygame to load up my image
player_img = pygame.transform.scale(pygame.image.load("car.png"), (100, 100))

JUDE_WIDTH = 62
JUDE_HEIGHT = 63
JUDE_VEL = 3

jude_img = pygame.transform.scale(pygame.image.load("jude_image.jpg"), (JUDE_WIDTH, JUDE_HEIGHT))

PLAYER_VEL = 5

FONT = pygame.font.SysFont("calibri", 30)

# Load PNG image for start screen
start_screen_img = pygame.transform.scale(pygame.image.load("start_screen.png"), (WIDTH, HEIGHT))

# Load PNG image for game over screen
game_over_img = pygame.transform.scale(pygame.image.load("game_over.png"), (WIDTH, HEIGHT))

# For drawing the objects on the screen
def draw(player, elapsed_time, judes):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    WIN.blit(time_text, (10, 10))

    # This is for displaying my image
    WIN.blit(player_img, (player.x, player.y))

    for jude in judes:
        # Draw jude image
        WIN.blit(jude_img, (jude.x, jude.y))

    pygame.display.update()

def start_screen():
    run_start = True

    while run_start:
        WIN.blit(start_screen_img, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# Game over screen with play again and exit buttons
def game_over_screen():
    run_game_over = True

    while run_game_over:
        WIN.blit(game_over_img, (0, 0))

        play_again_button = pygame.Rect(300, 500, 200, 50)
        exit_button = pygame.Rect(600, 500, 200, 50)

        pygame.draw.rect(WIN, (0, 128, 255), play_again_button)
        pygame.draw.rect(WIN, (255, 0, 0), exit_button)

        play_again_text = FONT.render("Play Again", 1, "white")
        WIN.blit(play_again_text, (play_again_button.x + play_again_button.width / 2 - play_again_text.get_width() / 2,
                                   play_again_button.y + play_again_button.height / 2 - play_again_text.get_height() / 2))

        exit_text = FONT.render("Exit", 1, "white")
        WIN.blit(exit_text, (exit_button.x + exit_button.width / 2 - exit_text.get_width() / 2,
                             exit_button.y + exit_button.height / 2 - exit_text.get_height() / 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    return True
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

MIN_DISTANCE = 300

# Main game loop
def main():
    run = True

    player = pygame.Rect(480, HEIGHT - 60, 40, 60)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    jude_add_increment = 2000
    jude_count = 0

    judes = []
    hit = False

    start_screen()

    while run:
        jude_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if jude_count > jude_add_increment:
            for _ in range(3):
                jude_x = random.randint(0, WIDTH - JUDE_WIDTH)
                jude_y = -JUDE_HEIGHT

                while any(jude.colliderect(pygame.Rect(jude_x, jude_y, JUDE_WIDTH, JUDE_HEIGHT)) for jude in judes):
                    jude_x = random.randint(0, WIDTH - JUDE_WIDTH)
                    jude_y = -JUDE_HEIGHT

                judes.append(pygame.Rect(jude_x, jude_y, JUDE_WIDTH, JUDE_HEIGHT))

            jude_add_increment = max(200, jude_add_increment - 50)
            jude_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Programming keystrokes
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 165:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH - 156:
            player.x += PLAYER_VEL

        for jude in judes[:]:
            jude.y += JUDE_VEL
            if jude.y > HEIGHT:
                judes.remove(jude)
            elif jude.colliderect(player) and (jude.y + JUDE_HEIGHT) >= player.y:
                judes.remove(jude)
                hit = True
                break

        if hit:
            draw(player, elapsed_time, judes)
            pygame.display.update()
            pygame.time.delay(1000)  
            if game_over_screen():
                player.x = 480
                start_time = time.time()
                elapsed_time = 0
                jude_add_increment = 2000
                jude_count = 0
                judes = []
                hit = False
            else:
                break

        draw(player, elapsed_time, judes)

    pygame.quit()

if __name__ == "__main__":
    main()
