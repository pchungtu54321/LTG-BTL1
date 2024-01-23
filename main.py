import pygame
import sys
import math
import random
from dataclasses import dataclass
from Zombie import Zombie


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (34, 9, 44)
MARGENTA = (135, 35, 65)
DARKORANGE = (190, 49, 68)
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
        self.menu = pygame.image.load("./Assets/MENU_SCREEN.png")
        self.gameplay_background = pygame.image.load(
            "./Assets/GAME_SCREEN.png")
        self.zombie = pygame.image.load("./Assets/ZOMBIE.png")
        self.play_game_button = pygame.image.load("./Assets/PLAYGAME.png")
        self.sword = pygame.image.load("./Assets/SWORD.png")
        self.setting_icon = pygame.image.load("./Assets/SETTING_ICON.png")


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
        self.game_over = GameOver(self.screen, self.game_state_manager)

        self.states = {'intro': self.intro, 'menu': self.menu,
                       'game_play': self.game_play, 'game_over': self.game_over}

    def run(self):
        while True:
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

        keys_pressed = pygame.key.get_pressed()
        mouses_pressed = pygame.mouse.get_pressed()
        if any(keys_pressed) or any(mouses_pressed):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.display.blit(image.menu, (0, 0))

        self.display.blit(self.text_play, (438, 597))
        self.display.blit(self.text_game, (425, 660))

        self.display.blit(self.text_how, (155, 558))
        self.display.blit(self.text_to_play, (116, 608))

        self.display.blit(self.text_quit, (31, 467))
        self.display.blit(self.text_high_score, (580, 456))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        keys = pygame.mouse.get_pressed()

        if (mouse_x >= 297) and (mouse_x <= 730) and (mouse_y >= 577) and (mouse_y <= 746):
            self.display.blit(image.play_game_button, (289, 564))
            if keys[0]:
                self.game_state_manager.setState('game_play')

        if (mouse_x >= 129) and (mouse_x <= 268) and (mouse_y >= 562) and (mouse_y <= 644):
            self.text_how = self.font_sub.render("H O W", True, DARK)
            self.text_to_play = self.font_sub.render(
                "T O  P L A Y", True, DARK)
            if keys[0]:
                self.game_state_manager.setState('')
        else:
            self.text_how = self.font_sub.render("H O W", True, WHITE)
            self.text_to_play = self.font_sub.render(
                "T O  P L A Y", True, WHITE)

        if (mouse_x >= 31) and (mouse_x <= 118) and (mouse_y >= 464) and (mouse_y <= 500):
            self.text_quit = self.font_sub.render("Q U I T", True, RED)
            if keys[0]:
                pygame.quit()
                sys.exit()

        else:
            self.text_quit = self.font_sub.render("Q U I T", True, DARK)

        if (mouse_x >= 580) and (mouse_x <= 772) and (mouse_y >= 457) and (mouse_y <= 491):
            self.text_high_score = self.font_sub.render(
                "H I G H  S C O R E", True, ORANGE)
            if keys[0]:
                self.game_state_manager.setState('')
        else:
            self.text_high_score = self.font_sub.render(
                "H I G H  S C O R E", True, DARK)


class HowToPlay:
    def __init__(self) -> None:
        pass


class GamePlay:

    def __init__(self, display, game_state_manager):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager

        self.TIMER = 30  # game play duration

        self.NUM_ROW = 3
        self.NUM_COL = 3

        self.cursor_img = image.sword
        self.cursor_img_rect = self.cursor_img.get_rect()

        self.font_main = pygame.font.SysFont('trashhand', 70)
        self.font_sub = pygame.font.SysFont('trashhand', 40)

        self.score_value = 0
        self.smash_times = 0

        self.zombies = []  # init a list to store current zombies on the screen

        self.ZOMBIE_LIFE_SPANS = 100 * 1000
        self.ZOMBIE_RADIUS = max(
            image.zombie.get_width(), image.zombie.get_height())
        self.GENERATE_ZOMBIE = pygame.USEREVENT + 1
        self.APPEAR_INTERVAL = 2 * 1000

        self.zombies_position = [(142, 125), (405, 125), (659, 125), (142, 372), (405, 372), (
            659, 372), (142, 620), (405, 620), (659, 620)]  # init a list to store position of zombie

        pygame.time.set_timer(self.GENERATE_ZOMBIE, self.APPEAR_INTERVAL)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    # if position equal with current zombie appear on the screen return true
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
        # return position that able to generate new zombie and time

    def drawZombies(self):
        for zombie in self.zombies:
            zombie_rect = image.zombie.get_rect()
            zombie_center = zombie_rect.center
            self.display.blit(
                image.zombie, (zombie.x - zombie_center[0], zombie.y - zombie_center[1]))

    def checkCollision(self, clickX, clickY, enemyX, enemyY):
        zombie_rect = image.zombie.get_rect()
        enemy_center = (
            enemyX + zombie_rect.center[0], enemyY + zombie_rect.center[1])
        distance = math.sqrt(math.pow(
            enemy_center[0] - clickX, 2) + (math.pow(enemy_center[1] - clickY, 2)))
        return distance < self.ZOMBIE_RADIUS

    def checkZombiesCollision(self, click_pos):
        for zombie in self.zombies:
            if self.checkCollision(click_pos[0], click_pos[1], zombie.x, zombie.y):
                self.score_value += 1
                self.zombies.remove(zombie)
                sound_effects.playHurt()

    def timerZombie(self):
        for zombie in self.zombies:
            zombie.life = max(
                0, zombie.life - (pygame.time.get_ticks() - zombie.time_of_birth))
            if zombie.life == 0:
                self.zombies.remove(zombie)

    def displayScore(self):
        score = self.font_sub.render(
            "S c o r e :  " + str(self.score_value), True, WHITE)
        text_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 775))
        self.display.blit(score, text_rect)

    def displayTime(self):
        time = self.font_sub.render(
            "T i m e :  " + str(self.TIMER), True, WHITE)
        text_rect = time.get_rect(center=(680, 775))
        self.display.blit(time, text_rect)

    def run(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                sound_effects.playHurt()
                click_pos = pygame.mouse.get_pos()
                self.checkZombiesCollision(click_pos)

            if event.type == self.GENERATE_ZOMBIE:
                if len(self.zombies) < self.NUM_COL * self.NUM_ROW:
                    new_pos, time_of_birth = self.generateNextEnemyPos()
                    self.zombies.append(Zombie(
                        x=new_pos[0], y=new_pos[1], screen=self.display, time_of_birth=time_of_birth))

            if event.type == pygame.USEREVENT:  # Timer
                self.TIMER -= 1
                if self.TIMER == 0:
                    self.game_state_manager.setState('game_over')

        self.display.blit(image.gameplay_background, (0, 0))
        image.setting_icon = pygame.transform.scale(
            image.setting_icon, (35, 37))
        self.display.blit(image.setting_icon, (25, 25))

        self.timerZombie()
        self.drawZombies()
        self.displayScore()
        self.displayTime()

        # cursor customize
        pygame.mouse.set_visible(False)  # make cursor invisible
        self.cursor_img_rect.center = pygame.mouse.get_pos()
        self.display.blit(self.cursor_img, self.cursor_img_rect)


class GameOver:
    def __init__(self, display, game_state_manager):
        self.display = display  # similar to screen variable
        self.game_state_manager = game_state_manager

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.display.fill(WHITE)


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
