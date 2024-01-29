import pygame
import sys
import math
import random
import os
from dataclasses import dataclass

from Zombie import Zombie, ZombieState


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (34, 9, 44)
ORANGE = (240, 89, 65)
RED = (184, 0, 0)
GREY = (77, 63, 90)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
TEXT = "Smash The Zombie"


class SoundEffect:
    def __init__(self):
        pygame.mixer.init()
        self.typingSound = pygame.mixer.Sound("sounds/typing.wav")
        self.mainTrack = pygame.mixer.Sound("sounds/themesong.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")

    def playTyping(self):
        self.typingSound.play()

    def stopTyping(self):
        self.typingSound.stop()

    def playLevelUp(self):
        self.levelSound.play()


sound_effects = SoundEffect()

# image


class Sprite:
    def __init__(self):
        self.menu = pygame.image.load("./Assets/MENU_SCREEN.png")
        self.gameplay_background = pygame.image.load(
            "./Assets/GAME_SCREEN.png")
        self.zombie = pygame.image.load("./Assets/ZOMBIE.png")
        self.play_game_button = pygame.image.load("./Assets/PLAYGAME.png")
        self.sword = pygame.image.load("./Assets/SWORD.png")
        self.setting_icon = pygame.image.load("./Assets/SETTING_ICON.png")
        self.game_over = pygame.image.load("./Assets/GAME_OVER_SCREEN.png")
        self.volume_on = pygame.image.load("./Assets/VOLUME_ON_ICON.png")
        self.volume_off = pygame.image.load("./Assets/VOLUME_OFF_ICON.png")


image = Sprite()


class Game:  # this is the main game class
    def __init__(self):
        # game initiallize
        self.clock = pygame.time.Clock()
        pygame.init()

        # window setting
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TEXT)

        self.game_state_manager = gameStateManager('intro')
        self.intro = Intro(self.screen, self.game_state_manager)
        self.menu = Menu(self.screen, self.game_state_manager)
        self.game_play = GamePlay(self.screen, self.game_state_manager)
        self.game_over = GameOver(self.screen, self.game_state_manager, self.game_play)
        self.pause = Pause(self.screen, self.game_state_manager, self.game_play)

        self.states = {'intro': self.intro, 'menu': self.menu,
                       'game_play': self.game_play, 'game_over': self.game_over, 'pause': self.pause}

    def run(self):

        while True:  # this while will loop every 1/60 sec

            # evoke run() function in class
            self.states[self.game_state_manager.getState()].run()

            pygame.display.update()
            self.clock.tick(FPS)


class Intro:
    def __init__(self, display, game_state_manager):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager

        # time configuration
        self.interval = 500  # time to display the first letter
        self.char_delay = 100  # time between characters
        self.current_time = pygame.time.get_ticks()
        self.next_char_time = self.current_time + self.interval
        self.char_index = 0
        # fade out ef
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill(BLACK)
        self.fade_alpha = 0

        self.font = pygame.font.SysFont('jollylodger', 50)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if any(pygame.key.get_pressed()) or any(pygame.mouse.get_pressed()):
            self.game_state_manager.setState('menu')  # switch screen
            sound_effects.mainTrack.play(-1)

        # take time since the game run
        self.current_time = pygame.time.get_ticks()

        # character iterator
        if self.current_time >= self.next_char_time and self.char_index < len(TEXT):
            self.char_index += 1
            self.next_char_time = self.current_time + self.char_delay

            sound_effects.playTyping()

        # output
        self.display.fill(BLACK)
        rendered_text = self.font.render(TEXT[:self.char_index], True, WHITE)
        text_rect = rendered_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.display.blit(rendered_text, text_rect)

        # fade to black ef
        if self.char_index >= len(TEXT):
            # increase opacity
            self.fade_alpha += 2
            self.fade_surface.set_alpha(self.fade_alpha)

            if self.fade_alpha > 255:
                self.game_state_manager.setState('menu')
                sound_effects.mainTrack.play(-1)

            # output
            self.display.blit(self.fade_surface, (0, 0))

            sound_effects.stopTyping()


class Menu:
    def __init__(self, display, game_state_manager):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager

        self.font_main = pygame.font.SysFont('trashhand', 70)
        self.font_sub = pygame.font.SysFont('trashhand', 40)

        self.text_play = self.font_main.render("P L A Y", True, DARK)
        self.text_game = self.font_main.render("G A M E",  True, DARK)

        self.text_how = self.font_sub.render("H O W", True, WHITE)
        self.text_to_play = self.font_sub.render("T O  P L A Y", True, WHITE)

        self.text_quit = self.font_sub.render("Q U I T", True, DARK)
        self.text_high_score = self.font_sub.render(
            "H I G H  S C O R E", True, DARK)

    def run(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if (mouse_pos[0] >= 297) and (mouse_pos[0] <= 730) and (mouse_pos[1] >= 577) and (mouse_pos[1] <= 746):  # play game button
                        self.game_state_manager.setState('game_play')

                    if (mouse_pos[0] >= 31) and (mouse_pos[0] <= 118) and (mouse_pos[1] >= 464) and (mouse_pos[1] <= 500):  # exit button
                        pygame.quit()
                        sys.exit()

        self.display.blit(image.menu, (0, 0))

        self.display.blit(self.text_play, (438, 597))
        self.display.blit(self.text_game, (425, 660))

        self.display.blit(self.text_how, (155, 558))
        self.display.blit(self.text_to_play, (116, 608))

        self.display.blit(self.text_quit, (31, 467))
        self.display.blit(self.text_high_score, (580, 456))

        if (mouse_pos[0] >= 297) and (mouse_pos[0] <= 730) and (mouse_pos[1] >= 577) and (mouse_pos[1] <= 746):
            self.display.blit(image.play_game_button, (289, 564))

        if (mouse_pos[0] >= 129) and (mouse_pos[0] <= 268) and (mouse_pos[1] >= 562) and (mouse_pos[1] <= 644):
            self.text_how = self.font_sub.render("H O W", True, DARK)
            self.text_to_play = self.font_sub.render(
                "T O  P L A Y", True, DARK)

        else:
            self.text_how = self.font_sub.render("H O W", True, WHITE)
            self.text_to_play = self.font_sub.render(
                "T O  P L A Y", True, WHITE)

        if (mouse_pos[0] >= 31) and (mouse_pos[0] <= 118) and (mouse_pos[1] >= 464) and (mouse_pos[1] <= 500):
            self.text_quit = self.font_sub.render("Q U I T", True, RED)

        else:
            self.text_quit = self.font_sub.render("Q U I T", True, DARK)

        if (mouse_pos[0] >= 580) and (mouse_pos[0] <= 772) and (mouse_pos[1] >= 457) and (mouse_pos[1] <= 491):
            self.text_high_score = self.font_sub.render(
                "H I G H  S C O R E", True, ORANGE)

        else:
            self.text_high_score = self.font_sub.render(
                "H I G H  S C O R E", True, DARK)


class HowToPlay:
    def __init__(self) -> None:
        pass


ZOMBIE_WIDTH = 100
ZOMBIE_HEIGHT = 100
DELAY_BEFORE_REMOVAL = 2000


class GamePlay:

    def __init__(self, display, game_state_manager):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager

        self.TIMER = 20  # game play duration
        self.timer_countdown = self.TIMER

        self.NUM_ROW = 3
        self.NUM_COL = 3

        self.setting_icon = pygame.transform.scale(
            image.setting_icon, (35, 37))
        self.setting_icon_rect = self.setting_icon.get_rect(center =(35, 35))

        self.cursor_img = image.sword
        self.cursor_img_rect = self.cursor_img.get_rect()

        self.font_main = pygame.font.SysFont('trashhand', 70)
        self.font_sub = pygame.font.SysFont('trashhand', 40)

        self.score_value = 0
        self.nb_of_click = 0

        self.zombies = []  # init a list to store current zombies on the screen

        self.ZOMBIE_LIFE_SPANS = 1 * 1000
        self.ZOMBIE_RADIUS = max(image.zombie.get_width(), image.zombie.get_height()) * 0.4
        self.GENERATE_ZOMBIE = pygame.USEREVENT + 1
        self.APPEAR_INTERVAL = 2 * 1000

        self.zombies_position = [(142, 125), (405, 125), (659, 125), (142, 372), (405, 372), (
            659, 372), (142, 620), (405, 620), (659, 620)]  # init a list to store position of zombie

        pygame.time.set_timer(self.GENERATE_ZOMBIE, self.APPEAR_INTERVAL)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def resetInitialState(self):
        self.timer_countdown = self.TIMER
        self.nb_of_click = 0
        self.score_value = 0

    def getScore(self):
        return self.score_value
    
    def getMissedClick(self):
        return self.nb_of_click - self.score_value

    def checkExist(self, pos):
        for zombie in self.zombies:
            if pos == (zombie.x, zombie.y):
                return True
        return False

    def generateNextEnemyPos(self):
        new_pos = ()  # init an empty tuple
        while True:
            # random a number from 0 to 8
            grid_index = random.randint(0, self.NUM_ROW * self.NUM_COL - 1)
            new_pos = self.zombies_position[grid_index]
            if not self.checkExist(new_pos):
                break
        # return position that able to generate new zombie and time
        return new_pos, pygame.time.get_ticks()

    def drawZombies(self):
        for zombie in self.zombies:
            zombie.draw()

    def checkCollision(self, clickX, clickY, enemyX, enemyY):
        zombie_rect = image.zombie.get_rect()
        enemy_center = (
            enemyX + zombie_rect.center[0] - 20, enemyY + zombie_rect.center[1] - 50)
        distance = math.sqrt(math.pow(
            enemy_center[0] - clickX, 2) + (math.pow(enemy_center[1] - clickY, 2)))
        return distance < self.ZOMBIE_RADIUS

    def checkZombiesCollision(self, click_pos):
        current_time = pygame.time.get_ticks()
        for zombie in self.zombies:
            if self.checkCollision(click_pos[0], click_pos[1], zombie.x, zombie.y) and zombie.state == ZombieState.GO_UP:
                self.score_value += 1
                zombie.change_state(ZombieState.IS_SLAMED)
                sound_effects.playLevelUp()
                zombie.draw()
                zombie.hit_time = current_time
            
    def removePreviousZombie(self):
        for zombie in self.zombies:
            current_time = pygame.time.get_ticks()
            if zombie.need_go_down():
                zombie.change_state(ZombieState.GO_DOWN)
                zombie.draw()
                zombie.go_down_time = current_time
            if current_time - zombie.go_down_time >= DELAY_BEFORE_REMOVAL and zombie.state == ZombieState.NONE:
                self.zombies.remove(zombie)
            if current_time - zombie.hit_time >= DELAY_BEFORE_REMOVAL and zombie.state == ZombieState.IS_SLAMED:
                self.zombies.remove(zombie)

    def displayMissedClicks(self):
        missed_clicks = self.font_sub.render(
            "M i s s e d :  " + str(self.nb_of_click - self.score_value), True, WHITE)
        text_rect = missed_clicks.get_rect(center=(120, 775))
        self.display.blit(missed_clicks, text_rect)

    def displayScore(self):
        score = self.font_sub.render(
            "S c o r e :  " + str(self.score_value), True, WHITE)
        text_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 775))
        self.display.blit(score, text_rect)

    def displayTime(self):
        time = self.font_sub.render(
            "T i m e :  " + str(self.timer_countdown), True, WHITE)
        text_rect = time.get_rect(center=(680, 775))
        self.display.blit(time, text_rect)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_pos = pygame.mouse.get_pos()
                    if self.setting_icon_rect.collidepoint(click_pos):
                        self.game_state_manager.setState('pause')
                    else:
                        self.nb_of_click += 1
                        self.checkZombiesCollision(click_pos)

            if event.type == self.GENERATE_ZOMBIE:
                self.removePreviousZombie()
                if len(self.zombies) < self.NUM_COL * self.NUM_ROW:
                    new_pos, time_of_birth = self.generateNextEnemyPos()
                    self.zombies.append(
                        Zombie(x=new_pos[0], y=new_pos[1], screen=self.display))

            if event.type == pygame.USEREVENT:
                self.timer_countdown -= 1
                if self.timer_countdown <= 0:
                    self.zombies.clear()
                    self.game_state_manager.setState('game_over')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game_state_manager.setState('pause')  

        self.display.blit(image.gameplay_background, (0, 0))

        self.display.blit(self.setting_icon, self.setting_icon_rect)

        self.drawZombies()
        self.displayMissedClicks()
        self.displayScore()
        self.displayTime()

        # cursor customize
        pygame.mouse.set_visible(False)  # make cursor invisible
        self.cursor_img_rect.center = pygame.mouse.get_pos()
        self.display.blit(self.cursor_img, self.cursor_img_rect)


class Pause:
    def __init__(self, display, game_state_manager, game_play):
        self.display = display
        self.game_state_manager = game_state_manager

        self.game_play = game_play

        self.font_main = pygame.font.SysFont('jollylodger', 70)
        self.font_sub = pygame.font.SysFont('jollylodger', 54)

        self.game_over_center = image.game_over.get_rect().center
        self.position = 0
        self.transition_speed = 10

        self.pause_game = self.font_main.render("P a u s e  g a m e", True, DARK)
        self.pause_game_rect = self.pause_game.get_rect(
                center=(SCREEN_WIDTH // 2, 280))

        self.continue_game = self.font_sub.render("C o n t i n u e", True, DARK)
        self.continue_game_rect = self.continue_game.get_rect(center=(SCREEN_WIDTH // 2, 420))

        self.menu = self.font_sub.render("M e n u", True, GREY)
        self.menu_rect = self.menu.get_rect(center = (SCREEN_WIDTH // 2, 580))

        self.volume_icon = image.volume_on
        self.volume_icon_rect = self.volume_icon.get_rect(center = (SCREEN_WIDTH // 2, 645))

    def resetInitialState(self):
        self.position = 0

    def run(self):
        pygame.mouse.set_visible(True)  # make cursor invisible

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.resetInitialState()
                    self.game_state_manager.setState("game_play")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_pos[0] >= 290 and mouse_pos[0] <= 510 and mouse_pos[1] >= 395 and mouse_pos[1] <= 445:
                        self.game_state_manager.setState("game_play")

                    if mouse_pos[0] >= 340 and mouse_pos[0] <= 460 and mouse_pos[1] >= 555 and mouse_pos[1] <= 605:
                        self.game_play.resetInitialState()
                        self.game_state_manager.setState("menu")

                    if self.volume_icon_rect.collidepoint(mouse_pos):
                        if self.volume_icon == image.volume_on:
                            self.volume_icon = image.volume_off
                            sound_effects.mainTrack.stop()
                        else:
                            self.volume_icon = image.volume_on
                            sound_effects.mainTrack.play(-1)

        self.display.blit(image.gameplay_background, (0, 0))
        self.display.blit(image.game_over, (SCREEN_WIDTH // 2 -
                    self.game_over_center[0], (SCREEN_HEIGHT - self.game_over_center[1]) - self.position))

        if (SCREEN_HEIGHT - self.game_over_center[1] - self.position) > ((SCREEN_HEIGHT // 2 - self.game_over_center[1]) + 50):
            self.position += self.transition_speed
        
        else:
            self.display.blit(self.pause_game, self.pause_game_rect)
            self.display.blit(self.continue_game, self.continue_game_rect)
            self.display.blit(self.menu, self.menu_rect)
            self.display.blit(self.volume_icon, self.volume_icon_rect)

            if mouse_pos[0] >= 290 and mouse_pos[0] <= 510 and mouse_pos[1] >= 395 and mouse_pos[1] <= 445:
                self.continue_game = self.font_sub.render("C o n t i n u e", True, WHITE)
            else:
                self.continue_game = self.font_sub.render("C o n t i n u e", True, DARK)

            if mouse_pos[0] >= 340 and mouse_pos[0] <= 460 and mouse_pos[1] >= 555 and mouse_pos[1] <= 605:
                self.menu = self.font_sub.render("M e n u", True, WHITE)
            else: 
                self.menu = self.font_sub.render("M e n u", True, GREY)

class GameOver:
    def __init__(self, display, game_state_manager, game_play):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager
        self.game_play = game_play

        self.font_main = pygame.font.SysFont('jollylodger', 70)
        self.font_sub = pygame.font.SysFont('jollylodger', 54)

        self.game_over_center = image.game_over.get_rect().center
        self.position = 0
        self.transition_speed = 10

        self.new_record = self.font_main.render(
            "N e w  r e c o r d", True, DARK)
        self.game_over = self.font_main.render("G a m e  O v e r", True, DARK)
        self.play_again = self.font_sub.render(
            "P l a y  A g a i n", True, GREY)
        self.menu = self.font_sub.render("M e n u", True, GREY)

    def resetInitialState(self):
        self.position = 0

    def run(self):
        pygame.mouse.set_visible(True)  # make cursor invisible
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if (mouse_pos[0] >= 240) and (mouse_pos[0] <= 560) and (mouse_pos[1] >= 550) and (mouse_pos[1] <= 610):
                        self.game_play.resetInitialState()
                        self.resetInitialState()
                        self.game_state_manager.setState('game_play')

                    if (mouse_pos[0] >= 345) and (mouse_pos[0] <= 465) and (mouse_pos[1] >= 620) and (mouse_pos[1] <= 670):
                        self.game_play.resetInitialState()
                        self.resetInitialState()
                        self.game_state_manager.setState('menu')

        self.display.blit(image.gameplay_background, (0, 0))
        self.display.blit(image.game_over, (SCREEN_WIDTH // 2 -
                          self.game_over_center[0], (SCREEN_HEIGHT - self.game_over_center[1]) - self.position))

        # transition effect continue to increase position every time
        if (SCREEN_HEIGHT - self.game_over_center[1] - self.position) > ((SCREEN_HEIGHT // 2 - self.game_over_center[1]) + 50):
            self.position += self.transition_speed

        else:
            new_record_rect = self.new_record.get_rect(
                center=(SCREEN_WIDTH // 2, 280))
            self.display.blit(self.new_record, new_record_rect)

            self.score = self.font_sub.render(
                "S c o r e :  " + str(self.game_play.getScore()), True, DARK)
            score_rect = self.score.get_rect(center=(SCREEN_WIDTH // 2, 390))
            self.display.blit(self.score, score_rect)

            self.missed_clicks = self.font_sub.render(
                "M i s s e d :  " + str(self.game_play.getMissedClick()), True, DARK)
            missed_clicks_rect = self.missed_clicks.get_rect(center=(SCREEN_WIDTH // 2, 450))
            self.display.blit(self.missed_clicks, missed_clicks_rect)

            play_again_rect = self.play_again.get_rect(
                center=(SCREEN_WIDTH // 2, 580))
            self.display.blit(self.play_again, play_again_rect)

            menu_rect = self.menu.get_rect(center=(SCREEN_WIDTH // 2, 645))
            self.display.blit(self.menu, menu_rect)

            if (mouse_pos[0] >= 240) and (mouse_pos[0] <= 560) and (mouse_pos[1] >= 550) and (mouse_pos[1] <= 610):
                self.play_again = self.font_sub.render(
                    "P l a y  A g a i n", True, WHITE)
            else:
                self.play_again = self.font_sub.render(
                    "P l a y  A g a i n", True, GREY)

            if (mouse_pos[0] >= 345) and (mouse_pos[0] <= 465) and (mouse_pos[1] >= 620) and (mouse_pos[1] <= 670):
                self.menu = self.font_sub.render("M e n u", True, WHITE)
            else:
                self.menu = self.font_sub.render("M e n u", True, GREY)


class gameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def getState(self):
        return self.current_state

    def setState(self, state):
        self.current_state = state


if __name__ == "__main__":  # run the class Game
    game = Game()
    game.run()
