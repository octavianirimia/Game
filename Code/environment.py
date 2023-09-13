import pygame

from agent import Agent
from audio import load_sounds
from block import generate_ground
from button import Image_button, Text_button
from camera import Camera_group
from generate_entities import generate_entities, random_generate_entities
from load_images import load_images
from player import Player



class Environment():
    def __init__(self, window_dimensions, window):
        
        # Variabile de lucru
        self.window_dimensions = window_dimensions
        self.window = window

        # AI
        self.agent = Agent(25, 4)

        # Imagini
        self.images = load_images()

        # Sunete
        self.sounds = load_sounds()

        # Grupuri
        self.group = Camera_group() # grupul tuturor obiectelor
        self.obstacles_group = pygame.sprite.Group()
        self.ground_group = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()

        # Inițializarea meniului
        font_size = 100
        font = pygame.font.SysFont("cambria", font_size)

        play_button_position = (self.window_dimensions[0] // 2, self.window_dimensions[1] // 2 - 2 * font_size)
        train_button_position = (self.window_dimensions[0] // 2, self.window_dimensions[1] // 2 - font_size)
        train_on_random_button_position = (self.window_dimensions[0] // 2, self.window_dimensions[1] // 2)
        self_play_button_position = (self.window_dimensions[0] // 2, self.window_dimensions[1] // 2 + font_size)
        self_play_on_random_position = (self.window_dimensions[0] // 2, self.window_dimensions[1] // 2 +2 * font_size)

        self.coin_image = self.images["Coin"]["Rotate"][0]

        # Butoane
        self.play_button = Text_button(play_button_position, "Play", font, "black", "red")
        self.train_button = Text_button(train_button_position, "Train", font, "black", "red")
        self.train_on_random_button = Text_button(train_on_random_button_position, "Train on radom",  font, "black", "red")
        self.self_play_button = Text_button(self_play_button_position, "Self play",  font, "black", "red")
        self.self_play_on_random_button = Text_button(self_play_on_random_position, "Self play on random", font, "black", "red")
        self.sound_button = Image_button(self.images["Sound"], (self.window_dimensions[0] - 20, 20))

        self.menu_display = True
        self.play = False
        self.train = None
        self.self_play = None

        # Inițializarea mediului
        self.background = self.images["Background"]
        self.scaled_background = pygame.transform.scale(self.background, self.window_dimensions)

        self.block_size = generate_ground(window_dimensions, self.images["Ground"], [self.group, self.ground_group])

        # Crearea jucătorului
        self.player = Player(self.images["Player"], (200, 200), self.sounds, self.group)

        # Poziția obstacolelor
        self.obstacle_position = 0
    

    def run(self, dt, mouse_poisiton):
        
        new_window_dimensions = pygame.display.get_surface().get_size()
        
        self.sound = self.sound_button.input(mouse_poisiton)

        if new_window_dimensions != self.window_dimensions:
            self.resize_window(new_window_dimensions)

        if self.play or self.train == "Random" or self.self_play == "Random":
            self.obstacle_position = random_generate_entities(self.window_dimensions, self.images, self.obstacle_position, self.block_size,
                                                        [self.group, self.obstacles_group, self.stone_group, self.coins_group])
        elif (self.train == "Normal" or self.self_play == "Normal") and not self.obstacles_group:
            generate_entities(self.window_dimensions, self.images, self.block_size,
                              [self.group, self.obstacles_group, self.stone_group, self.coins_group])
        
        self.player.run(dt, self.window_dimensions, self.menu_display, self.train, self.self_play, self.group.offset, self.block_size,
                        self.sound, self.agent, self.obstacles_group, self.stone_group, self.coins_group)
        
        self.group.update(dt, self.window_dimensions, self.group.offset, self.block_size)

        self.draw()

        if self.menu_display:
            self.menu(mouse_poisiton)

        if self.player.game_over:
            self.game_over()


    def draw(self):

        self.window.blit(self.scaled_background, (0, 0))
        self.group.draw(self.window, self.window_dimensions[0], self.player)
        self.window.blit(self.coin_image, (20, 20))

        self.sound_button.draw(self.window)

        self.coin_text =  pygame.font.SysFont("cambria", 40).render(str(self.player.coins), True, "black")
        self.rect = self.coin_text.get_rect(topleft = (60, 12))
        self.window.blit(self.coin_text, self.rect)


    def menu(self, mouse_position):

        transparent_surface = pygame.Surface(self.window_dimensions)
        transparent_surface.set_alpha(150)
        transparent_surface.fill((255, 255, 255))
        self.window.blit(transparent_surface, (0, 0))

        for button in [self.play_button, self.train_button, self.train_on_random_button, self.self_play_button, self.self_play_on_random_button]:
            button.hover(pygame.mouse.get_pos())
            button.draw(self.window)
        
        if self.play_button.input(mouse_position):
            self.menu_display = False
            self.play = True
        
        elif self.train_button.input(mouse_position):
            self.menu_display = False
            self.train = "Normal"
            self.sound_button.sound = "Mute"
            self.sound_button.update()

        elif self.train_on_random_button.input(mouse_position):
            self.menu_display = False
            self.train = "Random"
            self.sound_button.sound = "Mute"
            self.sound_button.update()

        elif self.self_play_button.input(mouse_position):
            self.menu_display = False
            self.self_play = "Normal"
            self.agent.load("Normal")
            self.sound_button.sound = "Mute"
            self.sound_button.update()
        
        elif self.self_play_on_random_button.input(mouse_position):
            self.menu_display = False
            self.self_play = "Random"
            self.train = self.agent.load("Random")
            self.sound_button.sound = "Mute"
            self.sound_button.update()
    

    def resize_window(self, new_window_dimensions):
        
        self.scaled_background = pygame.transform.scale(self.background, new_window_dimensions)

        for object in self.obstacles_group:
            object.rect.bottom += new_window_dimensions[1] - self.window_dimensions[1]
        
        for object in self.ground_group:
            object.rect.bottom += new_window_dimensions[1] - self.window_dimensions[1]

        self.window_dimensions = new_window_dimensions
    

    def game_over(self):
        
        for sprite in self.group:
            sprite.kill()

        self.group.offset = 0
        self.obstacle_position = 0

        self.player = Player(self.images["Player"], (200, 200), self.sounds, self.group)

        generate_ground(self.window_dimensions, self.images["Ground"], [self.group, self.ground_group])

        if self.play or self.train == "Random" or self.self_play == "Random":
            self.obstacle_position = random_generate_entities(self.window_dimensions, self.images, self.obstacle_position,
                                                              self.block_size,
                                                              [self.group, self.obstacles_group, self.stone_group, self.coins_group])
        
        elif self.train == "Normal" or self.self_play == "Normal":
            generate_entities(self.window_dimensions, self.images, self.block_size,
                              [self.group, self.obstacles_group, self.stone_group, self.coins_group])

        if self.train is None and self.self_play is None:
            self.menu_display = True