import settings

from numba import jit, njit
from numba.experimental import jitclass

import pygame
from pygame.locals import *
import time

try:
    from .anim_sprite import *
except Exception as ex:
    # Ignore error if compiled
    print(f"Unknown Exception - {ex}")
    pass


class FPSCounter(AnimSprite):
    # anim_clock = cython.declare(object)
    # screen = cython.declare(object)
    # update_freq = cython.declare(cython.int)
    # font_name = cython.declare(str)
    # font_size = cython.declare(cython.int)
    # color = cython.declare(tuple)
    # text = cython.declare(str)
    # last_fps = cython.declare(cython.double)
    # frame_count = cython.declare(cython.int)
    # time_elapsed = cython.declare(cython.double)
    # font = cython.declare(object)
    
    # Already declared in base class
    #x = cython.declare(cython.int)
    #y = cython.declare(cython.int)
    #speed = cython.declare(cython.int)
    #display_bounding_box = cython.declare(cython.bint)
    

    
    def __init__(self, x, y, font_name='calibri', font_size=24,
                 color=(255, 255, 255), anim_clock=None, screen=None, update_freq=50):
        super().__init__()
        self.anim_clock = anim_clock
        self.screen = screen
        self.update_freq = update_freq
        self.x = x
        self.y = y
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.text = "FPS OBJECT!"
        self.speed = 0
        self.last_fps = 0
        self.frame_count = 0
        self.time_elapsed = 0.0001

        self.display_bounding_box = False
        
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

        #self.font.set_bold(True)
    
    #@jit
    def redraw_surface(self):
        self.text = "FPS: " + str("%.2f" % float(self.anim_clock.get_fps()))
        # if cython.compiled:
        #     self.text += " - (cython)"
        #print("redraw..." + self.text)
        image = self.font.render(self.text, True, self.color)  #.convert_alpha()
        tmp = pygame.Surface(image.get_size()).convert() #.convert_alpha()
        # Fill with grey
        tmp.fill((96, 96, 96, 200))
        tmp.blit(image, (0, 0))
        self.image = tmp # .convert_alpha()
        #self.calculate_bounding_box()
        #self.image = pygame.Surface((200, 200))
        #self.image.fill((200, 200, 200))

    # @cython.ccall
    # def update(self):
    #     #super().update(time_elapsed_seconds)
    #     self.redraw_surface()
    
    #@jit
    def draw_self(self):
        self.redraw_surface()
        #super().draw(self.screen)
        self.draw(self.screen)

        
        