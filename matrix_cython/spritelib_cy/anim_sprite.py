import pygame
from pygame.locals import *
import time
import math
import cython


@cython.cclass
class AnimTimer():
    # timer_name = cython.declare(str, visibility='public')
    # created_on=cython.declare(cython.int, visibility='public')
    # last_update=cython.declare(cython.int, visibility='public')
    # delay=cython.declare(cython.int, visibility='public')
    # last_elapsed_time=cython.declare(cython.int, visibility='public')

    def __init__(self, timer_name="<TIMER>", delay=200) -> None:
        self.timer_name = timer_name
        self.created_on = pygame.time.get_ticks()
        self.last_update = 0
        self.delay = delay
        self.last_elapsed_time = 0

        pass


    @cython.ccall
    @cython.locals(
        curr_ticks=cython.int
    )
    def reset(self):
        curr_ticks = pygame.time.get_ticks()
        # Update last elapsed time
        self.last_elapsed_time = curr_ticks - self.last_update
        if self.last_elapsed_time > self.delay:
            # Don't let last elapsed be too huge
            self.last_elapsed_time = self.delay
        self.last_update = curr_ticks
        #print(self.timer_name + " - reset: " + str(self.last_update))

    @cython.locals(
        curr_ticks=cython.int,
        ret=cython.bint,
    )
    @cython.returns(cython.bint)
    @property
    def expired(self):
        ret = False

        curr_ticks = pygame.time.get_ticks()
        if (curr_ticks - self.last_update) > self.delay:
            ret = True
        
        if ret == True:
            # reset timer
            curr_ticks = pygame.time.get_ticks()
            self.last_elapsed_time = curr_ticks - self.last_update
            self.last_update = curr_ticks

        return ret

    @cython.ccall
    @cython.returns(cython.bint)
    @cython.locals(
        ret=cython.bint,
        curr_ticks=cython.int,
        auto_reset=cython.bint,
    )
    def is_expired(self, auto_reset=True):
        ret = False
        curr_ticks = pygame.time.get_ticks()
        #print(self.timer_name + " " + str(curr_ticks) + " - " + str(self.last_update) + " -- " + str(curr_ticks - self.last_update)  + " " + str(self.delay))
        if (curr_ticks - self.last_update) > self.delay:
            # Expired
            ret = True
        
        if auto_reset == True and ret == True:
            # print(self.timer_name + ' resetting')
            #print(self.timer_name + " " + str(curr_ticks) + " - " + str(self.last_update) + " -- " + str(curr_ticks - self.last_update)  + " " + str(self.delay))
            self.reset()
        else:
            #print(self.timer_name + " not resetting")
            #print(self.timer_name + " " + str(curr_ticks) + " - " + str(self.last_update) + " -- " + str(curr_ticks - self.last_update)  + " " + str(self.delay))
            pass
        return ret

_anim_cache = cython.declare("AnimCache", None)

@cython.cclass
class AnimCache():
    """
    A shared cache for images and objects
    """
    # A simple dict of image_name -> Surface - helps with not re-loading multiple copies each time
    shared_images = cython.declare(dict)

    # A dict of class types and a list of those object types - helps to keep track of active bullets, players, etc...
    active_objects = cython.declare(dict)


    @cython.cfunc
    @cython.returns("AnimCache")
    @staticmethod
    def get_instance():
        global _anim_cache

        if _anim_cache is None:
            _anim_cache = AnimCache()
        return _anim_cache
    
    def __init__(self):

        self.shared_images = dict()
        self.active_objects = dict()
    
    @cython.cfunc
    @cython.returns(list)
    @cython.locals(
        class_type=str,
    )
    def get_active_objects(self, class_type):
        if not class_type in self.active_objects:
            self.active_objects[class_type] = list()
        
        return self.active_objects[class_type]

    @cython.cfunc
    @cython.locals(
        object_to_add=object,
        active_objects=list
    )
    def add_active_object(self, object_to_add):
        object_type = str(type(object_to_add))
        active_objects = self.get_active_objects(object_type)
        active_objects.append(object_to_add)
        return

    @cython.cfunc
    @cython.locals(
        active_objects=object
    )
    def clean_up_inactive_objects(self, cls_type):
        # Clean out old objects
        active_objects = self.get_active_objects(cls_type)

        if len(active_objects) > 0 and \
            active_objects[0].active is not True:
            o = active_objects.pop(0)
            print("Destroying object ..." + str(cls_type))

    @cython.cfunc
    @cython.returns(object)
    @cython.locals(
        surface=object,
    )
    def get_image(self, image_file):
        surface = None

        if image_file.upper() == "<BLANK>":
            if image_file in self.shared_images:
                return self.shared_images[image_file]
            # Generate blank image
            surface = pygame.Surface((128,128)).convert() # pygame.Surface((128,128), flags=SRCALPHA, depth=32).convert_alpha()
            self.shared_images[image_file] = surface
            return surface

        if not image_file in self.shared_images:
            # Load the file and add convert it to the current color format
            # print("Loading Image File: " + str(image_file))
            surface = pygame.image.load(image_file).convert_alpha()
            # Save a copy of this in the shared_images list
            self.shared_images[image_file] = surface

        if surface is None:
            surface = self.shared_images[image_file]
        
        return surface

@cython.cclass
class AnimSprite():
    """
    Animated Sprite - used to show a group of images on a timer
    """

    # NOTE - These are defind in the PXD file
    # x = cython.declare(cython.int, visibility='public')
    # y = cython.declare(cython.int, visibility='public')
    # speed = cython.declare(cython.int, visibility='public')
    # scale = cython.declare(cython.double, visibility='public')
    # active = cython.declare(cython.bint, visibility='public')
    # direction = cython.declare(cython.int, visibility='public')
    # display_bounding_box = cython.declare(cython.bint, visibility='public')
    # frame_timer = cython.declare(AnimTimer, visibility='public')
    # update_timer = cython.declare(AnimTimer, visibility='public')
    # current_frame_index = cython.declare(cython.int, visibility='public')
    # images = cython.declare(list, visibility='public')
    # local_bounding_box = cython.declare(object, visibility='public')
    # bounding_box = cython.declare(object, visibility='public')
    # empty_image = cython.declare(object, visibility='public')
    # image = cython.declare(object, visibility='public')
    
    def __init__(self, frame_timer=200, update_timer=200):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.scale = 1.0
        self.active = True
        self.direction = 0
        self.display_bounding_box = True

        # How long to show the current frame for
        self.frame_timer = AnimTimer(timer_name="sprite_frame_timer", delay=frame_timer)
        self.update_timer = AnimTimer(timer_name="sprite_update_timer", delay=update_timer)
        
        self.current_frame_index = 0
        self.images = list()
        self.local_bounding_box = Rect(0, 0, 0, 0)
        self.bounding_box = Rect(0, 0, 0, 0)

        cache = AnimCache.get_instance()

        self.empty_image = cache.get_image("<BLANK>")
        self.empty_image.set_colorkey((0, 0, 0))
        self.image = self.empty_image
        
        # Add this object to the list of objects
        cache.add_active_object(self)
    

    @cython.ccall
    @cython.locals(
        screen=object,
    )
    def draw(self, screen):
        if screen is None:
            raise Exception("Draw requires a screen!!!")
        
        # Draw the ship at the current location with the
        # current frame
        #print("Drawing: " + str(self.x) + "/" + str(self.y))
        screen.blit(self.get_current_frame(), 
            (self.x, self.y))
        
        #pygame.draw.rect(screen, (255, 0, 0), self.local_bounding_box, 3)
        
        # Draw the bounding box
        if self.display_bounding_box is True:
            pygame.draw.rect(screen, (0, 255, 0), self.bounding_box, 1)
        #if str(type(self)) == "<class 'enemy.Enemy'>":
        #print("BOX: " + str(self.bounding_box))

        # Draw a small area for the X/Y center
        #pygame.draw.rect(screen, (255, 0, 0), Rect(self.x, self.y, 1, 1) , 2)

        # Draw small area for center of bounding box
        #pygame.draw.rect(screen, (200, 200, 0), 
        #    Rect(self.bounding_box.centerx, self.bounding_box.centery, 1, 1),
        #    2)
        
    @cython.ccall
    @cython.locals(
        time_elapsed_seconds=cython.double,
        radians=cython.double,
        curr_speed=cython.double,
        new_x = cython.int,
        new_y = cython.int
    )
    def move_step(self, time_elapsed_seconds):
        # Trig to move along a line given direction and speed

        # Get elapsed seconds from timer
        time_elapsed_seconds = self.update_timer.last_elapsed_time
        
        # Need radians - not degrees
        radians = (self.direction * math.pi) / 180
        
        # How far did we move this frame?
        if time_elapsed_seconds == 0:
            # prevent divide by 0 error
            time_elapsed_seconds = 0.0000000001
        curr_speed = self.speed * time_elapsed_seconds
        
        # Calculate new X,Y
        new_x = self.x + math.cos(radians) * curr_speed
        new_y = self.y + math.sin(radians) * curr_speed
        
        return new_x, new_y
        
    @cython.ccall
    @cython.locals(
        time_elapsed_seconds=cython.double,
    )
    def update(self, time_elapsed_seconds):
        if self.frame_timer.expired:
            # Go to next frame
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.images):
                self.current_frame_index = 0

        # Update frame if update timer has past
        if self.update_timer.expired:        
            # Set the current bounding box
            self.bounding_box = self.local_bounding_box.move(self.x, self.y)
    
    @cython.ccall
    @cython.locals(
        x = cython.int,
        y = cython.int,
        x_diff = cython.int,
        y_diff = cython.int
    )
    def center_on_point(self, x=0, y=0):
        # Center the surface here!
        # Due to the x/y of this being in the upper left corner, the image will be drawn
        # below and off to the right of the normal X/Y, so make sure our "center" is here.

        # NOTE - bounding_box is NOT the same as the surface dimensions
        x_diff = self.local_bounding_box.centerx - self.x
        y_diff = self.local_bounding_box.centery - self.y

        self.x = x - x_diff
        self.y = y - y_diff

    @cython.ccall
    @cython.locals(
        surface = object,
        img_w = cython.int,
        img_h = cython.int,
        max_x = cython.int,
        max_y = cython.int,
        min_x = cython.int,
        min_y = cython.int,
        key_pixel = object,
        x = cython.int,
        y = cython.int,
        pixel = object,

    )
    def calculate_bounding_box(self):
        # Look at all the pixels, make the smallest possible
        # box around lit pixels so we have an accurate bounding
        # box
        surface = self.get_current_frame()
        img_w = surface.get_width()
        img_h = surface.get_height()
        
        max_x = 0
        min_x = img_w
        max_y = 0
        min_y = img_h
        
        key_pixel = (0, 0, 0, 0)
        # Grab upper left corner pixel
        key_pixel = surface.get_at((0, 0))
        # print("Using Key Pixel: " + str(key_pixel))
        
        for x in range(0, img_w):
            # Loop through X and keep the max x and least x for
            # non transparent pixels
            for y in range(0, img_h):
                pixel = surface.get_at((x, y))
                if pixel != key_pixel:
                    # Not transparent, see if this is the farthest
                    # extreme where a pixel is located and record it
                    # to auto detect our bounding_box
                    if x > max_x:
                        max_x = x
                    if x < min_x:
                        min_x = x
                    if y > max_y:
                        max_y = y
                    if y < min_y:
                        min_y = y
        
        # Should have a bounding box now
        self.local_bounding_box = Rect(min_x, min_y,
            max_x-min_x, max_y-min_y)
        print("Calculated Bounding Box: " + str(self.local_bounding_box) + " - " + str(type(self)))
    
    @cython.ccall
    @cython.locals(
        image_file = str,
        surface = object,
        cache = "AnimCache",
    )
    def add_image(self, image_file):
        surface = None

        cache = AnimCache.get_instance()
        surface = cache.get_image(image_file)

        if surface is None:
            # Unable to find/load the surface
            print("ERROR finding or loading surface!")
            return
        
        # print("Shared Image Count: " + str(len(type(self).shared_images)))
        # Add this surface to the local copy
        self.images.append(surface)
        
        # Make sure to calculate the bounding box
        if self.local_bounding_box == Rect(0, 0, 0, 0):
            self.calculate_bounding_box()
    
    @cython.ccall
    @cython.locals(
        image_files = list,
        s = str
    )
    def add_images(self, image_files):
        # Add each surface
        for s in image_files:
            self.add_image(s)
    
    @cython.ccall
    @cython.returns(cython.int)
    def get_current_frame_index(self):
        # Figure out the current frame for this animation
        
        if len(self.images) < 1:
            # No images at all? Return -1 for error
            return -1
        
        # Make sure it isn't too low or too high
        if self.current_frame_index < 0:
            self.current_frame_index = 0
        if self.current_frame_index >= len(self.images):
            # If too high, wrap around back to 0
            self.current_frame_index = 0
        return self.current_frame_index
    
    @cython.ccall
    @cython.locals(
        frame_index = cython.int,
    )
    @cython.returns(object)
    def get_current_frame(self):
        frame_index = self.get_current_frame_index()
        # If we are < 0 then send back an empty surface so things don't
        # blow up
        if len(self.images) == 0:
            return self.image

        if frame_index >= 0:
            # Set the current image
            self.image = self.images[frame_index]
            
        # Return the current frame
        return self.image
    
    @cython.ccall
    def destroy(self):
        # Set to inactive and it will get cleaned up by update
        self.active = False
    
    @cython.ccall
    @cython.locals(
        cache = "AnimCache",
        o = object,
        screen = object,
    )
    @classmethod
    def draw_all(cls, screen):
        cache = AnimCache.get_instance()

        # Tell objects to draw themselves
        # print(str(cls) + " len " + str(len(cls.active_objects)) + str(cls.__name__))
        for o in cache.get_active_objects(cls):
            o.draw(screen)
    
    @cython.ccall
    @cython.locals(
        time_elapsed_seconds = cython.double,
        o = object,
        cache = "AnimCache"
    )
    @classmethod
    def update_all(cls, time_elapsed_seconds):
        cache = AnimCache.get_instance()

        # Tell each object to update
        for o in cache.get_active_objects(cls):
            o.update(time_elapsed_seconds)
        
        cache.clean_up_inactive_objects(cls)
    
    
