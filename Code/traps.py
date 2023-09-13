import pygame



class Spikes(pygame.sprite.Sprite):
    def __init__(self, image, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Setări generale
        self.image = image
        self.rect = self.image.get_rect(midbottom = position)
    

    def kill_object(self, offset):
        
        if offset - self.rect.right > 0:
            self.kill()
    

    def update(self, dt, window_dimensions, offset, block_size):# arguments = (window_dimensions, menu_display, offset, block_size, [obstacles_group, stone_group])

        self.kill_object(offset)



class Fire(pygame.sprite.Sprite):
    def __init__(self, animations, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Setări generale
        self.animations = animations
        self.status = "On"
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(midbottom = position)
    

    def animate(self, dt):

        self.frame_index += 20 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
    

    def kill_object(self, offset):

        if offset - self.rect.right > 0:
            self.kill()


    def update(self, dt, window_dimensions, offset, block_size): # arguments = (window_dimensions, menu_display, offset, block_size, [obstacles_group, stone_group])

        self.animate(dt)
        self.kill_object(offset)