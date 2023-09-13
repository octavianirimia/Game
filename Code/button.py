class Text_button():
    def __init__(self, position, text, font, color, hover_color):

        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.button_text = font.render(self.text, True, self.color)
        self.rect = self.button_text.get_rect(center = position)
    

    def input(self, mouse_position):

        if mouse_position[0] in range(self.rect.left, self.rect.right) and \
            mouse_position[1] in range(self.rect.top, self.rect.bottom):
            return True


    def hover(self, mouse_position):

        if mouse_position[0] in range(self.rect.left, self.rect.right) and \
            mouse_position[1] in range(self.rect.top, self.rect.bottom):
            self.button_text = self.font.render(self.text, True, self.hover_color)
        else:
            self.button_text = self.font.render(self.text, True, self.color)
    
    
    def draw(self, window):

        window.blit(self.button_text, self.rect)



class Image_button():
    def __init__(self, images, position):
        
        self.images = images
        self.position = position
        self.sound = "Unmute"
        
        self.update()
    

    def input(self, mouse_position):

        if mouse_position[0] in range(self.rect.left, self.rect.right) and \
            mouse_position[1] in range(self.rect.top, self.rect.bottom):
            if self.sound == "Unmute":
                self.sound = "Mute"
            else:
                self.sound = "Unmute"

            self.update()
        
        return self.sound
        

    def update(self):
        
        self.image = self.images[self.sound]
        self.rect = self.image.get_rect(center = self.position)


    def draw(self, window):

        window.blit(self.image, self.rect)