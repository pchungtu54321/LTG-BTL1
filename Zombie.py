import pygame
import os
from enum import Enum

ZOMBIE_WIDTH = 128
ZOMBIE_HEIGHT = 158
DEFAULT_ALPHA = 255
MAX_TIME_LAST = 30
HOLE_WIDTH = 200
HOLE_HEIGHT = 100
ZOMBIE_MAX_HEIGHT = 100

class ZombieState(Enum):
    GO_UP = 0
    NEED_SLAM = 1
    IS_SLAMED = 2
    GO_DOWN = 3
    NONE = 4
class Zombie:
    def __init__(self, x, y, screen):
        self.state = ZombieState.GO_UP
        self.x = x
        self.y = y
        self.screen = screen
        self.y_rise = ZOMBIE_MAX_HEIGHT
        self.alpha = DEFAULT_ALPHA
        self.time_last = MAX_TIME_LAST
        self.hit_time = 0

    def reset(self):
        self.state = ZombieState.NONE
        self.y_rise = ZOMBIE_MAX_HEIGHT
        self.alpha = DEFAULT_ALPHA
        self.time_last = MAX_TIME_LAST

    def is_slamed(self, eventlist):
        if self.state != ZombieState.NEED_SLAM:
            return False 
        for event in eventlist:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.x <= pos[0] and pos[0] <= self.x + ZOMBIE_WIDTH and self.y <= pos[1] and pos[1] <= self.y + ZOMBIE_HEIGHT:
                    return True
        return False 

    def change_state(self, new_state):
        self.state = new_state

    def draw(self):
        surface = pygame.Surface((ZOMBIE_WIDTH,ZOMBIE_HEIGHT))
        zombie = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath('Zombie.py')), "Assets/ZOMBIE.png" 
                                                if self.state != ZombieState.IS_SLAMED else "Assets/zombie_stun.png"))
        
        zombie = pygame.transform.scale(zombie, (ZOMBIE_WIDTH,ZOMBIE_HEIGHT))   
        zombie_sur = zombie.convert_alpha()
        zombie_sur.set_alpha(self.alpha)  
        surface.fill((255,255,255))
        surface.set_colorkey((255,255,255))
        surface.blit(zombie_sur, (0, self.y_rise))
        if self.state == ZombieState.GO_UP:
            zombie_rect = zombie.get_rect()
            zombie_center = zombie_rect.center
            self.screen.blit(surface, (self.x - zombie_center[0], self.y - zombie_center[1]))
            self.go_up()
        if self.state == ZombieState.IS_SLAMED:
            self.screen.blit(surface, (self.x, self.y))
            self.fade()
        

    def go_up(self):
        if self.y_rise == 0:
            return
        self.y_rise -= 20 

    def fade(self): 
        if self.alpha == 0:
            self.y_rise = ZOMBIE_MAX_HEIGHT
            self.state = ZombieState.NONE
            self.alpha = DEFAULT_ALPHA
            return 
        self.alpha -= 51    