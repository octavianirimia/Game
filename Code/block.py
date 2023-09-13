import os
import pygame
import random



class Ground(pygame.sprite.Sprite):
    def __init__(self, image, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        self.image = image
        self.rect = self.image.get_rect(bottomleft = position)
        self.ground_type = "Ground"

        self.ground_group = groups[1]
        self.i = 0
        self.j = len(self.ground_group) - 1


    def update(self, dt, window_dimensions, offset, block_size): # arguments = (window_dimensions, menu_display, offset, block_size, [obstacles_group, stone_group])
        if self.i > len(self.ground_group) - 1:
                self.i = 0
                self.j = len(self.ground_group) - 1
            
        else:
            self.j = self.i - 1

        if offset - self.ground_group.sprites()[self.i].rect.right > block_size:
            self.ground_group.sprites()[self.i].rect.left = self.ground_group.sprites()[self.j].rect.right
            self.i += 1



class Lava(Ground):
    def __init__(self, image, position, groups):
        Ground.__init__(self, image, position , groups)



class Stone(pygame.sprite.Sprite):
    def __init__(self, image, position, groups):
        pygame.sprite.Sprite.__init__(self, groups)

        # Setări generale
        self.image = image
        self.rect = self.image.get_rect(midbottom = position)
    

    def kill_object(self, offset):
         
        if offset - self.rect.right > 0:
            self.kill()


    def update(self, dt, window_dimensions, offset, block_size): # arguments = (window_dimensions, menu_display, offset, block_size, [obstacles_group, stone_group])
        
        self.kill_object(offset)



def generate_ground(window_dimensions, image, groups):
    image = pygame.image.load(os.path.join("Python", "Game", "Graphics", "Terain", "Ground block.png")).convert_alpha()
    block_size = image.get_height()

    for i in range(0, (2 * window_dimensions[0]) // block_size):
        Ground(image, (i * block_size, window_dimensions[1]), groups)
    
    return block_size



def generate_stone_construction(windows_dimensions, image, position, block_size, groups):

    stone_construction_width_height = random.randrange(1, 5)

    for i in range(0, stone_construction_width_height):
        for j in range (i, stone_construction_width_height):
            Stone(image, (position + j * block_size, windows_dimensions[1] - (i + 1) * block_size), groups)