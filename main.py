import pygame
import random
import math
from pygame import mixer

# initial the game
pygame.init()

# create the game
screen = pygame.display.set_mode((800, 600))  # set_mode ((width, height))

# Add Title
pygame.display.set_caption("Space Invaders")

# Background
backgroundImg = pygame.image.load("background.png")

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)  # add -1 for playing in loop
# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))  # enemy doesn't appear close to the right part of the screen
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready means the bullet is hidden
# Fire means the bullet is travelling
bulletImg = pygame.image.load("bullet.png")
bulletX = random.randint(0, 800)
bulletX = 0
bulletY = 480
bulletY_change = 8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    game_over_text = game_over_font.render("GAME OVER:", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))  # to draw image on the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # to draw image on the screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (
        x + 16, y + 10))  # giving x+16 and y+10 because we want bullet to appear at the center of the spaceship


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it's left or right
        if event.type == pygame.KEYDOWN:  # KEYDOWN is pressing any key on the keyboard
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # KEYUP is releasing any key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Spaceship movement and check the boundaries of the space with the screen
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement and increase it's position when it hits the boundary
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # to make enemy outside the screen
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet
    # make the bullet again available to fire
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # to make the bullet appear on the screen
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
