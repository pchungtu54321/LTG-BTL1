import pygame
import random
import math
from enum import Enum
from dataclasses import dataclass

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (24, 9, 48)

pygame.init()
clock = pygame.time.Clock()

#import sprite, assets
saver_image = pygame.image.load("./image/SCREENSAVER.png")

bg_image = pygame.image.load("./image/background.png")
bg_image = pygame.transform.scale(bg_image, (saver_image.get_width(), saver_image.get_height()))

enemy_image = pygame.image.load("./image/character_1.png")
enemy_image = pygame.transform.scale(enemy_image, (enemy_image.get_width(), enemy_image.get_height()))

font = pygame.font.SysFont('jollylodger', 32)

#setting scale window
pygame.display.set_caption("Zombie Smash Game")
screen = pygame.display.set_mode((saver_image.get_width(), saver_image.get_height()))

#coordinates of score display
score_value = 0
textX = 10
textY = 10

#
enemies = []

NUM_COL = 3
NUM_ROW = 3

ENEMY_LIFE_SPAN = 5 * 1000
@dataclass
class Enemy:
    x: int
    y: int
    life: int = ENEMY_LIFE_SPAN

ENEMY_RADIUS = min(enemy_image.get_width(), enemy_image.get_height()) // 2.5
ENEMY_COLOR = (255, 0, 0)
GENERATE_ENEMY = pygame.USEREVENT + 1
APPEAR_INTERVAL = 2 * 1000
pygame.time.set_timer(GENERATE_ENEMY, APPEAR_INTERVAL)

# AGE_ENEMY, AGE_INTERVAL = pygame.USEREVENT + 2, 1 * 1000
# pygame.time.set_timer(AGE_ENEMY, AGE_INTERVAL)

possible_enemy_pos = [(70, 25), (70, 210), (70, 415), (380, 25), (380, 210), (380, 415), (710, 25), (710, 210), (710, 415) ]

def check_exist(pos):
    for enemy in enemies:
        if pos == (enemy.x, enemy.y):
            return True
    return False


def generate_next_enemy_pos():
    new_pos = ()
    while True:
        grid_index = random.randint(0, NUM_ROW * NUM_COL - 1)
        new_pos = possible_enemy_pos[grid_index]
        if not check_exist(new_pos):
            break
    return new_pos


def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy_image, (enemy.x, enemy.y))


def show_score(x, y):
    global score_value
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def check_enemy_collision(clickX, clickY, enemyX, enemyY):
    enemyX, enemyY = enemyX + ENEMY_RADIUS, enemyY + ENEMY_RADIUS
    distance = math.sqrt(math.pow(enemyX - clickX, 2) + (math.pow(enemyY - clickY, 2)))
    return distance < ENEMY_RADIUS


def check_enemies_collision(click_pos, enemies):
    for enemy in enemies:
        if check_enemy_collision(click_pos[0], click_pos[1], enemy.x, enemy.y):
            global score_value
            score_value += 1
            enemies.remove(enemy)

def age_enemies():
    for enemy in enemies:
        enemy.life = enemy.life-1000

def remove_died_enemies():
    for enemy in enemies:
        if enemy.life == 0:
            enemies.remove(enemy)

class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("sounds/themesong.wav")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.fireSound.set_volume(1.0)
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        pygame.mixer.music.play(-1)

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.sop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

#FSM
class GameState(Enum):
    SAVER_SCREEN = 1
    GAME_SCREEN = 2
    GAMEOVER_SCREEN = 3
current_state = GameState.SAVER_SCREEN

start = font.render("START", True, (255,255,255))

running = True
while running:
    #saver screen
    if current_state == GameState.SAVER_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos() 
                if (click_pos[0] > (saver_image.get_width() - 150) // 2) and (click_pos[0] < (((saver_image.get_width() - 150) // 2) + 150)) and (click_pos[1] > 500) and (click_pos[1] < 500 + 50):
                    current_state = GameState.GAME_SCREEN

        screen.blit(saver_image, (0, 0))

        pygame.draw.rect(screen, DARK, ((saver_image.get_width() - 150) // 2, 500, 150, 50)) # 2 CON SO DAU TIEN LA DIEM TREN CUNG BEN TRAI
        pygame.draw.rect(screen, WHITE, ((saver_image.get_width() - 150) // 2, 500, 150, 50), 1) # 2 CON SO DAU TIEN LA DIEM TREN CUNG BEN TRAI
        screen.blit(start, ((saver_image.get_width() - 60) // 2, 505))

    #game play
    if current_state == GameState.GAME_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN: # mouse click
                click_pos = pygame.mouse.get_pos() 
                print(click_pos)
                check_enemies_collision(click_pos, enemies)

            if event.type == GENERATE_ENEMY: # zombie spawn
                if len(enemies) < NUM_COL * NUM_ROW:
                    new_pos = generate_next_enemy_pos()
                    # print(new_pos)
                    enemies.append(Enemy(new_pos[0], new_pos[1]))
        screen.blit(bg_image, (0, 0))
        draw_enemies()
        show_score(textX, textY)


    pygame.display.update()
    clock.tick(60)


