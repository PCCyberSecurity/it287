cimport cython

import cython

cdef class AnimTimer:
    cdef public str timer_name
    cdef public cython.int created_on
    cdef public cython.int last_update
    cdef public cython.int delay
    cdef public cython.int last_elapsed_time

    cpdef reset(self)
    cpdef cython.bint is_expired(self, cython.bint auto_reset=*)


cdef class AnimSprite:
    cdef public cython.int x
    cdef public cython.int y
    cdef public cython.int speed
    cdef public double scale
    cdef public bint active
    cdef public cython.int direction
    cdef public bint display_bounding_box
    cdef public AnimTimer frame_timer
    cdef public AnimTimer update_timer
    cdef public cython.int current_frame_index
    cdef public list images
    cdef public object local_bounding_box
    cdef public object bounding_box
    cdef public object empty_image
    cdef public object image
    
    #def __init__(self, frame_timer, update_timer)
          
    cpdef draw(self, object screen)
                
    cpdef move_step(self, double time_elapsed_seconds)
                
    cpdef update(self, double time_elapsed_seconds)
        
    cpdef center_on_point(self, cython.int x=*, cython.int y=*)
        
    cpdef calculate_bounding_box(self)
    
    cpdef add_image(self, str image_file)
    
    cpdef add_images(self, list image_files)
    
    cpdef cython.int get_current_frame_index(self)
    
    cpdef object get_current_frame(self)
    
    cpdef destroy(self)
    
    cpdef draw_all(cls, object screen)
    
    cpdef update_all(cls, double time_elapsed_seconds)
    

