import pygame
import random



class Coin(pygame.sprite.Sprite):
    def __init__(self, animations, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Variabile de lucru
        self.frame_index = 0

        # Setări generale
        self.animations = animations["Rotate"]
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(midbottom = position)
    

    def animate(self, dt):

        self.frame_index += 20 * dt

        if self.frame_index >= len(self.animations):
            self.frame_index = 0

        self.image = self.animations[int(self.frame_index)]
    

    def kill_object(self, offset):

        if offset - self.rect.right > 0:
            self.kill()


    def update(self, dt, window_dimensions, offset, block_size):
        
        self.animate(dt)
        self.kill_object(offset)



def generate_coins(animations, position, groups):
    
    if len(groups[1]) < 3:
        Coin(animations, (position[0] - random.randint(100, 500), position[1]), groups)