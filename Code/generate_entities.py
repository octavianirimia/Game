import random

from block import Lava, generate_stone_construction
from coin import Coin
from enemy import Bat, Fat_bird, Rino, Snail
from traps import Fire, Spikes



def random_generate_entities(window_dimensions, images, position, block_size, groups):
    generated_obstacles = set()

    for obstacle in groups[1]:
        generated_obstacles.add(type(obstacle).__name__)
    
    while len(generated_obstacles) < 4:

        generated_obstacles = set()

        for obstacle in groups[1]:
            generated_obstacles.add(type(obstacle).__name__)
    
    
        position += 1000

        obstacles = ["Spikes", "Fire", "Bat", "Fat bird", "Snail", "Rino"]
        obstacle = random.choice(obstacles)

        if obstacle == "Lava":
            Lava(images[obstacle], (position, window_dimensions[1]), groups[:2])

        elif obstacle == "Stone construction":
            generate_stone_construction(window_dimensions, images["Stone"], position, block_size, groups[:3])
        
        elif obstacle == "Spikes":
            Spikes(images[obstacle], (position, window_dimensions[1] - block_size), groups[:2])

        elif obstacle == "Fire":
            Fire(images[obstacle], (position, window_dimensions[1] - block_size), groups[:2])

        elif obstacle == "Bat":
            Bat(images[obstacle], (position, 500), groups[:2])

        elif obstacle == "Fat bird":
            Fat_bird(images[obstacle], (position, 200), groups[:2])

        elif obstacle == "Rino":
            Rino(images[obstacle], (position, window_dimensions[1] - block_size), groups[:2])

        else:
            Snail(images[obstacle], (position, window_dimensions[1] - block_size), groups[:2])
        
        Coin(images["Coin"], (position - 150, window_dimensions[1] - block_size - 20), groups[::3])

    return position



def generate_entities(window_dimensions, images, block_size, groups):

    obstacles = ["Spikes", "Bat", "Fire", "Fat bird", "Snail", "Rino", "Bat", "Snail", "Spikes", "Rino", "Fire", "Fat bird", "Bat", "Fire"]

    position = 1000

    for i in range(len(obstacles)):
        
        if obstacles[i] == "Spikes":
            Spikes(images[obstacles[i]], (position, window_dimensions[1] - block_size), groups[:2])

        elif obstacles[i] == "Fire":
            Fire(images[obstacles[i]], (position, window_dimensions[1] - block_size), groups[:2])

        elif obstacles[i] == "Bat":
            Bat(images[obstacles[i]], (position, 500), groups[:2])

        elif obstacles[i] == "Fat bird":
            Fat_bird(images[obstacles[i]], (position, 200), groups[:2])

        elif obstacles[i] == "Rino":
            Rino(images[obstacles[i]], (position, window_dimensions[1] - block_size), groups[:2])

        else:
            Snail(images[obstacles[i]], (position, window_dimensions[1] - block_size), groups[:2])
        
        Coin(images["Coin"], (position - 150, window_dimensions[1] - block_size - 20), groups[::3])

        position += 1000