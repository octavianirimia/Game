import os
import pygame



def load_sounds():
    
    Sounds = {
        "Run": pygame.mixer.Sound(os.path.join("Python", "Game", "Audio", "Run.wav")),
        "Jump": pygame.mixer.Sound(os.path.join("Python", "Game", "Audio", "Jump.wav")),
        "Game over": pygame.mixer.Sound(os.path.join("Python", "Game", "Audio", "Game over.wav")),
        "Ground hit": pygame.mixer.Sound(os.path.join("Python", "Game", "Audio", "Ground hit.wav")),
        "Coin picking": pygame.mixer.Sound(os.path.join("Python", "Game", "Audio", "Coin picking.mp3"))
    }

    return Sounds