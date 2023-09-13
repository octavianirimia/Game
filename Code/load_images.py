import os
import pygame



def flip(images):
    return [pygame.transform.flip(image, True, False) for image in images]


def load_animations(path, width, direction = False):
    image_names = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))] # Se încarcă fiecare nume al pozelor

    animation_list_for_every_state = {} # inițializarea unei variabile de tip dicționar

    # Iterarea prin fiecare nume de poză
    for image_name in image_names:
        image = pygame.image.load(os.path.join(path, image_name)).convert_alpha() # Încărcarea pozei și modificarea fundalului în fundal transparent
        
        animation_list = []

        height = image.get_height()

        # Iterarea prin fiecare imagine din fiecare poză
        for i in range(image.get_width() // width):
            temporary_image = image.subsurface(i * width, 0, width, height)
            animation_list.append(pygame.transform.scale2x(temporary_image))


        # Se adaugă în dicționar fiecare nume de imagine și se întoarce imaginea în caz că nu e în direcția potrivită
        if direction:
            animation_list_for_every_state[image_name.replace(".png", "") + "_right"] = flip(animation_list)
            animation_list_for_every_state[image_name.replace(".png", "") + "_left"] = animation_list

        else:
            animation_list_for_every_state[image_name.replace(".png", "")] = animation_list

    return animation_list_for_every_state


def load_images():
    # Imagini
    ground_block_image = pygame.image.load(os.path.join("Python", "Game", "Graphics", "Terain", "Ground block.png")).convert_alpha()
    stone_block_image = pygame.image.load(os.path.join("Python", "Game", "Graphics", "Terain", "Stone block.png")).convert_alpha()
    background_image = pygame.image.load(os.path.join("Python", "Game", "Graphics", "Background", "Landscape.jpg"))
    spikes_trap_image = pygame.transform.scale2x(
                        pygame.image.load(os.path.join("Python", "Game", "Graphics", "Traps", "Spikes", "Spikes.png")).convert_alpha())
    mute_image = pygame.image.load(os.path.join("Python", "Game", "Graphics", "Sound", "Mute.png")).convert_alpha()
    unmute_image = pygame.image.load(os.path.join("Python", "Game", "Graphics", "Sound", "Unmute.png")).convert_alpha()
    
    # Imagini animate
    fire_trap_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Traps", "Fire"), 16)
    bat_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Enemies", "Bat"), 46, True)
    fat_bird_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Enemies", "Fat bird"), 40)
    rino_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Enemies", "Rino"), 52)
    snail_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Enemies", "Snail"), 38, True)
    player_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Characters", "Bunny"), 34, True)
    ghost_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Characters"), 34)
    coin_animations = load_animations(os.path.join("Python", "Game", "Graphics", "Rewards", "Coin"), 16)

    player_animations.update(ghost_animations)
    
    images = {
        "Ground": ground_block_image,
        "Stone": stone_block_image,
        "Background": background_image,
        "Spikes": spikes_trap_image,
        "Fire": fire_trap_animations,
        "Bat": bat_animations,
        "Fat bird": fat_bird_animations,
        "Rino": rino_animations,
        "Snail": snail_animations,
        "Player": player_animations,
        "Coin": coin_animations,
        "Sound": {"Mute": mute_image, "Unmute": unmute_image}
    }

    return images