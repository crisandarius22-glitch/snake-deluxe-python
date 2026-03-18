import random
import pygame
import os
import sys

pygame.init()

# Culori
CULORI = {
    "fundal": (30, 30, 30),
    "snake": (0, 255, 100),
    "fruct": (255, 50, 50),
    "text": (255, 255, 255),
    "game_over": (255, 0, 0),
    "bordura": (100, 100, 100)
}

# Bloc și ecran
bloc = 20
ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
latime, inaltime = ecran.get_size()
latime = (latime // bloc) * bloc
inaltime = (inaltime // bloc) * bloc
ecran = pygame.display.set_mode((latime, inaltime), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Deluxe")

# Fonturi
font_text = pygame.font.SysFont("consolas", 20)
font_mare = pygame.font.SysFont("consolas", 40)

# Highscore
def citeste_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def salveaza_highscore(nou_scor):
    with open("highscore.txt", "w") as f:
        f.write(str(nou_scor))

# Obstacole
obstacole = []

def adauga_obstacol(snake, fruct_x, fruct_y):
    while True:
        ox = random.randint(0, (latime - bloc) // bloc) * bloc
        oy = random.randint(0, (inaltime - bloc) // bloc) * bloc
        if [ox, oy] not in snake and [ox, oy] != [fruct_x, fruct_y] and [ox, oy] not in obstacole:
            obstacole.append([ox, oy])
            break

def draw_obstacole():
    for obs in obstacole:
        pygame.draw.rect(ecran, CULORI["bordura"], [obs[0], obs[1], bloc, bloc])

def scorul(val, scor_maxim):
    text = font_text.render(f"Scor: {val}", True, CULORI["text"])
    text_max = font_text.render(f"Max: {scor_maxim}", True, CULORI["text"])
    ecran.blit(text, [10, 10])
    ecran.blit(text_max, [10, 35])

def draw_snake(snake_bloc, snake_lista):
    for segment in snake_lista:
        pygame.draw.rect(ecran, CULORI["snake"], [segment[0], segment[1], snake_bloc, snake_bloc])

def mesaj(text, culoare, sus=True):
    message = font_mare.render(text, True, culoare)
    y_pos = inaltime / 3 if sus else inaltime / 2
    ecran.blit(message, [latime / 6, y_pos])

def joc(viteza_initiala=10):
    game_over = False
    game_close = False

    def normalize(val):
        return (val // bloc) * bloc

    x = normalize(latime // 2)
    y = normalize(inaltime // 2)
    x_schimbare = bloc
    y_schimbare = 0

    snake = []
    lungime = 1
    viteza = viteza_initiala
    scor_maxim = citeste_highscore()
    afiseaza_plus = False
    plus_timer = 0

    fruct_x = normalize(random.randint(0, (latime - bloc) // bloc) * bloc)
    fruct_y = normalize(random.randint(0, (inaltime - bloc) // bloc) * bloc)

    obstacole.clear()
    adauga_obstacol(snake, fruct_x, fruct_y)

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            ecran.fill(CULORI["fundal"])
            mesaj("Ai pierdut! C - Continua | Q - Iesi", CULORI["game_over"], sus=False)
            scorul(lungime - 1, scor_maxim)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        joc()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_LEFT and x_schimbare == 0:
                    x_schimbare = -bloc
                    y_schimbare = 0
                elif event.key == pygame.K_RIGHT and x_schimbare == 0:
                    x_schimbare = bloc
                    y_schimbare = 0
                elif event.key == pygame.K_UP and y_schimbare == 0:
                    x_schimbare = 0
                    y_schimbare = -bloc
                elif event.key == pygame.K_DOWN and y_schimbare == 0:
                    x_schimbare = 0
                    y_schimbare = bloc

        cap_nou = [x + x_schimbare, y + y_schimbare]

        if cap_nou[0] >= latime or cap_nou[0] < 0 or cap_nou[1] >= inaltime or cap_nou[1] < 0:
            game_close = True

        for obs in obstacole:
            if cap_nou[0] == obs[0] and cap_nou[1] == obs[1]:
                game_close = True

        if cap_nou in snake[:-1]:
            game_close = True

        x, y = cap_nou
        cap = [x, y]
        snake.append(cap)

        if len(snake) > lungime:
            del snake[0]

        ecran.fill(CULORI["fundal"])
        pygame.draw.rect(ecran, CULORI["fruct"], [fruct_x, fruct_y, bloc, bloc])
        draw_obstacole()
        draw_snake(bloc, snake)

        if afiseaza_plus:
            elapsed = pygame.time.get_ticks() - plus_timer
            if elapsed < 500:
                plus_text = font_text.render("+1", True, (255, 255, 100))
                ecran.blit(plus_text, [x + bloc, y - bloc])
            else:
                afiseaza_plus = False

        scorul(lungime - 1, scor_maxim)
        pygame.display.update()

        snake_rect = pygame.Rect(x, y, bloc, bloc)
        fruct_rect = pygame.Rect(fruct_x, fruct_y, bloc, bloc)

        if snake_rect.colliderect(fruct_rect):
            lungime += 1
            fruct_x = normalize(random.randint(0, (latime - bloc) // bloc) * bloc)
            fruct_y = normalize(random.randint(0, (inaltime - bloc) // bloc) * bloc)
            adauga_obstacol(snake, fruct_x, fruct_y)

            afiseaza_plus = True
            plus_timer = pygame.time.get_ticks()

            if lungime - 1 > scor_maxim:
                scor_maxim = lungime - 1
                salveaza_highscore(scor_maxim)

            if lungime % 5 == 0:
                viteza += 2

        clock.tick(viteza)

    pygame.quit()
    sys.exit()

joc()
