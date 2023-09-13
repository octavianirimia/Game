import pygame

from custom_timer import Timer



class Bat(pygame.sprite.Sprite):
    def __init__(self, animations, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Setări generale
        self.status = "Flying"
        self.status_direction = "left"
        self.frame_index = 0
        self.animations = animations
        self.image = self.animations[f"{self.status}_{self.status_direction}"][self.frame_index]
        self.rect = self.image.get_rect(center = position)

        # Setări de mișcare
        self.direction = -1
        self.position = self.rect.centerx
        self.initial_position = self.position
        self.speed_factor = 200
        self.speed = 0
    

    def move(self, dt):
        
        self.speed = self.direction * self.speed_factor * dt
        self.position += self.speed
        position = round(self.position)
        self.rect.centerx = position

        if abs(position - self.initial_position) >= 200:
            self.direction *= -1
            if self.direction == -1:
                self.status_direction = "left"    
            else:
                self.status_direction = "right"


    def animate(self, dt):

        self.frame_index += 20 * dt

        if self.frame_index >= len(self.animations[f"{self.status}_{self.status_direction}"]):
            self.frame_index = 0

        self.image = self.animations[f"{self.status}_{self.status_direction}"][int(self.frame_index)]
    

    def kill_object(self, offset):

        if offset - self.rect.right > 0:
            self.kill()
    

    def update(self, dt, window_dimensions, offset, block_size):

        self.move(dt)
        self.animate(dt)
        self.kill_object(offset)



class Fat_bird(pygame.sprite.Sprite):
    def __init__(self, animations, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Setări generale
        self.frame_index = 0
        self.animations = animations
        self.image = self.animations["Fall"][self.frame_index]
        self.rect = self.image.get_rect(center = position)

        # Setări de mișcare
        self.direction = 0
        self.position = self.rect.centery
        self.initial_position = self.position
        self.gravitational_acceleration = 10
        self.on_ground = False
        self.speed = 0

        # Timer pentru timpul petrecut pe pământ
        self.animation_reset_timer = Timer(3000)

    
    def gravity(self, dt):

        if not self.on_ground:
            self.speed = self.gravitational_acceleration * dt
            self.direction += self.speed
            self.position += self.direction
            self.rect.centery = round(self.position)
            

    def collsion(self, ground_top):

        if self.rect.bottom > ground_top:
            self.direction = 0
            self.rect.bottom = ground_top + 10
            self.on_ground = True
        
        else:
            self.on_ground = False

    
    def animate(self, window_height):

        if self.animation_reset_timer.done:
            self.rect.centery = self.initial_position
            self.position = self.initial_position
            self.animation_reset_timer.done = False

        if not self.on_ground:
            if self.rect.bottom < window_height - 96 - 40:
                self.frame_index = 0

            elif self.rect.bottom >= window_height -96- 40 and self.rect.bottom < window_height -96- 30:
                self.frame_index = 3

            elif self.rect.bottom >= window_height - 96-30 and self.rect.bottom < window_height - 96-20:
                self.frame_index = 2

            elif self.rect.bottom >= window_height - 96-20:
                self.frame_index = 1
            
            self.image = self.animations["Fall"][self.frame_index]
        
        else:
            if not self.animation_reset_timer.active and not self.animation_reset_timer.done:
                self.animation_reset_timer.activate()
        

    def kill_object(self, offset):
        if offset - self.rect.right > 0:

            self.kill()

    
    def update(self, dt, window_dimensions, offset, block_size): # arguments = (window_dimensions, menu_display, offset, block_size, [obstacles_group, stone_group])

        self.gravity(dt)
        self.collsion(window_dimensions[1] - block_size)
        self.animate(window_dimensions[1])

        if self.animation_reset_timer.active:
            self.animation_reset_timer.update()
        
        self.kill_object(offset)

        

class Rino(pygame.sprite.Sprite):
    def __init__(self, animations, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Setări generale
        self.status = "Run"
        self.frame_index = 0
        self.animations = animations
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(midbottom = position)

        # Setări de mișcare
        self.position = self.rect.centerx
        self.speed_factor = 180
        self.speed = 0


    def move(self, dt, window_width, offset):

        if offset > self.rect.left - window_width:
            self.speed = self.speed_factor * dt
            self.position -= self.speed
            self.rect.centerx = round(self.position)
    

    def animate(self, dt):

        self.frame_index += 20 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
    

    def kill_object(self, offset):
        if offset - self.rect.right > 0:

            self.kill()
    

    def update(self, dt, window_dimensions, offset, block_size):# arguments = (window_dimensions, menu_display, offset, block_size, [obstacles_group, stone_group])

        self.move(dt, window_dimensions[0], offset)
        self.animate(dt)
        self.kill_object(offset)



class Snail(pygame.sprite.Sprite):
    def __init__(self, animations, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Setări generale
        self.status = "Walk"
        self.status_direction = "left"
        self.frame_index = 0
        self.animations = animations
        self.image = self.animations[f"{self.status}_{self.status_direction}"][self.frame_index]
        self.rect = self.image.get_rect(midbottom = position)

        # Setări de mișcare
        self.direction = -1
        self.position = self.rect.centerx
        self.initial_position = self.position
        self.speed_factor = 50
        self.speed = 0
    

    def move(self, dt):

        self.speed = self.direction * self.speed_factor * dt
        self.position += self.speed
        position = round(self.position)
        self.rect.centerx = position

        if abs(position - self.initial_position) >= 200:
            self.direction *= -1
            if self.direction == -1:
                self.status_direction = "left"    
            else:
                self.status_direction = "right"


    def animate(self, dt):

        self.frame_index += 20 * dt

        if self.frame_index >= len(self.animations[f"{self.status}_{self.status_direction}"]):
            self.frame_index = 0

        self.image = self.animations[f"{self.status}_{self.status_direction}"][int(self.frame_index)]
    

    def kill_object(self, offset):
        
        if offset - self.rect.right > 0:

            self.kill()
    

    def update(self, dt, window_dimensions, offset, block_size): # arguments = (window_dimensions, menu_display, offset, block_size, [obstacles_group, stone_group])

        self.move(dt)
        self.animate(dt)
        self.kill_object(offset)