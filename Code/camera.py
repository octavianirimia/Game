import pygame


class Camera_group(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        
        self.offset = 0
    

    def draw(self, window, window_width, player):
        
        if player.rect.centerx -self.offset > window_width / 2 and player.direction.x:
            self.offset = player.rect.centerx - window_width / 2

        for object in self:
            offset_rect = object.rect.copy()
            offset_rect.centerx -= self.offset
            window.blit(object.image, offset_rect)