import pygame
import sys
import time

from environment import Environment



def main(fps, window_dimensions, window):

    # Crearea unui obiect ce ajută la monitorizarea timpului
    clock = pygame.time.Clock()

    # Mediul
    environment = Environment(window_dimensions, window)

    run = True
    previous_time = time.time()

    # Bucla jocului
    while run:
        dt = time.time() - previous_time
        previous_time = time.time()

        mouse_position = (0, 0)

        # Gestionarea evenimentelor
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
            
        environment.run(dt, mouse_position)

        pygame.display.update()

        # Limitarea rulării buclei la fps ori pe secundă/rularea jocului la fps cadre pe secundă
        clock.tick(fps)


    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    # Inițializare pygame
    pygame.init()

    # Proprietățile ferestrei
    window_dimensions = (1280, 720) # dimensiule inițiale ale ferestrei

    # Inițializarea ferestrei de lucru
    window = pygame.display.set_mode(window_dimensions, pygame.RESIZABLE)

    # Numele ferestrei
    pygame.display.set_caption("Joc") # Numele ferestrei

    fps = 60

    main(fps, window_dimensions, window)