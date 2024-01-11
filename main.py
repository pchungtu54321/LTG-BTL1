import pygame
import sys
import math
import random
from enum import Enum
from dataclasses import dataclass

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (24, 9, 48)
GREY = (182, 187, 196)

# game initiallize
clock = pygame.time.Clock()
pygame.init()
pygame.mixer.init()

# window setting
width, height = 1000, 668
screen = pygame.display.set_mode((width, height))
text = "Smash The Zombie"
pygame.display.set_caption(text)

# font setting
font = pygame.font.SysFont('jollylodger', 50)

# import assets
# sound
class SoundEffect:
    def __init__(self):
        self.typingSound = pygame.mixer.Sound("sounds/typing.wav")
        self.mainTrack = pygame.mixer.Sound("sounds/themesong.wav")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")

    def playTyping(self):
        self.typingSound.play()

    def stopTyping(self):
        self.typingSound.stop()

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.stop()

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
sound_effects = SoundEffect()

# image
class Sprite:
    def __init__(self):
        self.saver_image = pygame.image.load("./image/SCREENSAVER.png")
        self.bg_image = pygame.image.load("./image/background.png")
        self.enemy_image = pygame.image.load("./image/character_1.png")
image = Sprite()


# intro
# time configuration
interval = 500  # time to display the first letter
char_delay = 100  # time between characters
current_time = pygame.time.get_ticks()
next_char_time = current_time + interval
char_index = 0
# fade out ef
fade_surface = pygame.Surface((width, height))
fade_surface.fill(BLACK)
fade_alpha = 0

# saver screen 
button_hover = False
button_width = 150
button_height = 75
button_rect = pygame.Rect((width - 150) // 2, 500, button_width, button_height)

# gameplay screen
#coordinates of score display
score_value = 0
textX = 10
textY = 10

enemies = []

NUM_COL = 3
NUM_ROW = 3

ENEMY_LIFE_SPAN = 100 * 1000
@dataclass
class Enemy:
    x: int
    y: int
    life: int = ENEMY_LIFE_SPAN
    time_of_birth: int = 0  

ENEMY_RADIUS = min(image.enemy_image.get_width(), image.enemy_image.get_height()) // 2.5
ENEMY_COLOR = (255, 0, 0)
GENERATE_ENEMY = pygame.USEREVENT + 1
APPEAR_INTERVAL = 2 * 1000
pygame.time.set_timer(GENERATE_ENEMY, APPEAR_INTERVAL)

# AGE_ENEMY, AGE_INTERVAL = pygame.USEREVENT + 2, 1 * 1000
# pygame.time.set_timer(AGE_ENEMY, AGE_INTERVAL)

possible_enemy_pos = [(70, 25), (70, 210), (70, 415), (380, 25), (380, 210), (380, 415), (710, 25), (710, 210), (710, 415)]


def draw_button(rect_color, text_color, x, y, width, height, text, hover):
    if hover:
        pygame.draw.rect(screen, WHITE, button_rect)
        text_surface = font.render(text, True, BLACK)

    else:
        pygame.draw.rect(screen, rect_color, button_rect)
        text_surface = font.render(text, True, text_color)

    # draw button
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


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
    return new_pos, pygame.time.get_ticks()  # Trả về cả vị trí và thời gian tạo nhân vật

def draw_enemies():
    for enemy in enemies:
        screen.blit(image.enemy_image, (enemy.x, enemy.y))

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

            sound_effects.playLevelUp()

def age_enemies():
    for enemy in enemies:
        enemy.life = max(0, enemy.life - (pygame.time.get_ticks() - enemy.time_of_birth))
        if enemy.life == 0:
            enemies.remove(enemy)

def remove_died_enemies():
    for enemy in enemies:
        if enemy.life == 0:
            enemies.remove(enemy)


# game state
class Game_State(Enum):
    INTRO_SCREEN = 0
    SAVER_SCREEN = 1
    GAME_SCREEN = 2
    GAMEOVER_SCREEN = 3
current_game_state = Game_State.INTRO_SCREEN
# game loop
running = True
while running:
    if current_game_state == Game_State.INTRO_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                running = False
            
            if (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN):
                current_game_state = Game_State.SAVER_SCREEN
                sound_effects.mainTrack.play(-1)

        # take time since the game run
        current_time = pygame.time.get_ticks()

        # character iterator
        if current_time >= next_char_time and char_index < len(text):
            char_index += 1
            next_char_time = current_time + char_delay

            sound_effects.playTyping()

        # output
        screen.fill(BLACK)
        rendered_text = font.render(text[:char_index], True, WHITE)
        text_rect = rendered_text.get_rect(center=(width // 2, height // 2))
        screen.blit(rendered_text, text_rect)

        # fade to black ef
        if char_index >= len(text):
            # increase opacity
            fade_alpha += 2
            fade_surface.set_alpha(fade_alpha)

            if fade_alpha > 255:
                current_game_state = Game_State.SAVER_SCREEN
                sound_effects.mainTrack.play(-1) 

            # output
            screen.blit(fade_surface, (0, 0))

            sound_effects.stopTyping()

        
    if current_game_state == Game_State.SAVER_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                if (click_pos[0] > (width - button_width) // 2) and (click_pos[0] < (((width - button_width) // 2) + button_width)) and (click_pos[1] > 500) and (click_pos[1] < (500 + button_height)):
                    current_game_state = Game_State.GAME_SCREEN

            if event.type == pygame.MOUSEMOTION:
                # Kiểm tra nếu chuột nằm trong vùng nút
                button_hover = button_rect.collidepoint(event.pos)

        # output
        screen.blit(image.saver_image, (0, 0))
        draw_button(DARK, WHITE, (width - 150) // 2, 500, button_width, button_height, "START", button_hover)


    if current_game_state == Game_State.GAME_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN: # mouse click
                click_pos = pygame.mouse.get_pos() 
                # print(click_pos)
                check_enemies_collision(click_pos, enemies)

            if event.type == GENERATE_ENEMY:
                if len(enemies) < NUM_COL * NUM_ROW:
                    new_pos, time_of_birth = generate_next_enemy_pos()
                    enemies.append(Enemy(new_pos[0], new_pos[1], ENEMY_LIFE_SPAN, time_of_birth))

        age_enemies()
        screen.blit(image.bg_image, (0, 0))
        draw_enemies()
        show_score(textX, textY)



    if current_game_state == Game_State.GAMEOVER_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()