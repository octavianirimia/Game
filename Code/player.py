import pygame
import sys

from custom_timer import Timer



class Player(pygame.sprite.Sprite):
    def __init__(self, animations, position, sounds, group):
        pygame.sprite.Sprite.__init__(self, group)

        # Variabile de lucru
        self.status = "Idle"
        self.status_direction = "right"
        self.frame_index = 0
        self.reseted_environment = True
        self.dead = False
        self.game_over = False
        self.coins = 0
        self.picked_coin = False

        # Setări generale
        self.sounds = sounds
        self.animations = animations
        self.image = self.animations[f"{self.status}_{self.status_direction}"][self.frame_index]
        self.rect = self.image.get_rect(center = position)

        # Setări de mișcare
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 300
        self.gravitational_acceleration = 4
        self.on_ground = False

        # Timer
        self.dead_animation_timer = Timer(2500)
        self.sound_is_playing = False
        self.previous_status = "Run"

        # AI
        self.state = None
        self.reward = 0
        self.passed_obstacles = 0


    def get_input(self, menu_display, offset):
       
        if not menu_display and not self.dead:
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_a] and self.rect.left - offset > 0:
                self.direction.x = -1
                self.status_direction = "left"

            elif pressed_keys[pygame.K_d]:
                self.direction.x = 1
                self.status_direction = "right"
                
            else:
                self.direction.x = 0
            
            if pressed_keys[pygame.K_SPACE] and self.on_ground:
                self.direction.y = -1.6
    
        
    def move(self, dt, ground_top, stone_group):

        # Mișcare pe orizontală
        self.position.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.position.x)
        self.collision(ground_top, stone_group, "horizontal")

        # Mișcare pe verticală / săritură
        self.position.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.position.y)
        self.collision(ground_top, stone_group, "vertical")


    def gravity(self, dt):

        if not self.on_ground and not self.dead:
            self.direction.y += self.gravitational_acceleration * dt
            self.position.y += self.direction.y
            self.rect.centery = round(self.position.y)

    
    def obstacles_collision(self, self_play, obstacles_group):

        if pygame.sprite.spritecollideany(self, obstacles_group):
            if pygame.sprite.spritecollide(self, obstacles_group, False, pygame.sprite.collide_mask):
                if not self.dead_animation_timer.active and not self.dead_animation_timer.done:
                    self.direction.x, self.direction.y = 0, -1
                    self.dead = True

                    if not self_play:
                        self.dead_animation_timer.activate()
    

    def collision(self, ground_top, stone_group, direction):

        collided_block = pygame.sprite.spritecollideany(self, stone_group)

        if collided_block:
            if direction == "horizontal": # Coliziune orizontală
                if self.direction.x > 0:
                    self.rect.right = collided_block.rect.left

                elif self.direction.x < 0:
                    self.rect.left = collided_block.rect.right

                self.position.x = self.rect.centerx

            else: # Coiliziune verticală
                if self.direction.y >= 0:
                    self.rect.bottom = collided_block.rect.top
                    self.on_ground = True

                elif self.direction.y < 0:
                    self.rect.top = collided_block.rect.bottom

                self.direction.y = 0

        else:
            if self.rect.bottom > ground_top:
                self.direction.y = 0
                self.rect.bottom = ground_top
                self.on_ground = True
            
            else:
                self.on_ground = False
    

    def coin_pick(self, coins_group):

        if pygame.sprite.spritecollideany(self, coins_group):
            if pygame.sprite.spritecollide(self, coins_group, True, pygame.sprite.collide_mask):
                self.coins += 1
                self.picked_coin = True


    def get_status(self):

        if self.dead:
            self.status = "Ghost"
        elif self.direction.y < 0:
            self.status = "Jump"
        elif self.direction.y > 0:
            self.status = "Fall"
        elif self.direction.x != 0:
            self.status = "Run"
        else:
            self.status = "Idle"


    def animate(self, dt):

        self.frame_index += 20 * dt
        frame_index = round(self.frame_index)

        animation = self.status + "_" + self.status_direction if not self.dead else self.status

        if frame_index >= len(self.animations[animation]):
            frame_index = 0
            self.frame_index = 0

        self.image = self.animations[animation][frame_index]


    def play_sounds(self):
        
        if (self.status != self.previous_status or self.picked_coin) and self.previous_status in self.sounds.keys():
            self.sound_is_playing = False
            self.sounds[self.previous_status].stop()

        if not self.sound_is_playing:
            self.previous_status = self.status

            if self.picked_coin:
                self.picked_coin = False
                self.sounds["Coin picking"].play()
        
            elif self.status == "Ghost":
                self.sound_is_playing = True
                self.sounds["Game over"].play()
            
            elif self.status == "Jump":
                self.sound_is_playing = True
                self.sounds[self.status].play(-1)
            
            elif self.status == "Run":
                self.sound_is_playing = True
                self.sounds[self.status].play(-1)


    def train_ai(self, agent, train, offset, groups):

        # Starea anterioarară
        if self.reseted_environment:
            self.reseted_environment = False
            self.state = agent.get_state(self, offset, groups)

        # Găsirea următoarei mișcări
        action = agent.select_action(self.state, train)

        next_state, reward, done = agent.step(self, action.item(), offset, groups)

        agent.cache(self.state, action, reward, next_state, done)

        agent.learn()

        self.state = next_state

        self.reward += reward.item()

        if done:
            agent.save(self, train)
            self.game_over = True
            print(f"Episode: {agent.episode}\nDistance: {self.rect.centerx}\nReward: {self.reward}\nCoins: {self.coins}\n\n")

            if agent.episode >= 1000:
                pygame.quit()
                sys.exit()
    

    def test_ai(self, agent, train, offset, groups):

        if self.reseted_environment:
            self.reseted_environment = False
            self.state = agent.get_state(self, offset, groups)

        action = agent.select_action(self.state, train)

        next_state, reward, done = agent.step(self, action.item(), offset, groups)

        self.reward += reward.item()

        self.state = next_state

        if done:
            self.game_over = True
            print(f"Distance: {self.rect.centerx}\nReward: {self.reward}\nCoins: {self.coins}\n\n")


    def run(self, dt, window_dimensions, menu_display, train, self_play, offset, block_size, sound, agent,
            obstacles_group, stone_group, coins_group):
        
        if train is not None:
            self.train_ai(agent, train, offset, [obstacles_group, stone_group, coins_group])
        
        elif self_play is not None:
            self.test_ai(agent, train, offset, [obstacles_group, stone_group, coins_group])
        
        else:
            self.get_input(menu_display, offset)

            if self.dead_animation_timer.active:
                self.dead_animation_timer.update()
        
            else:
                if self.dead_animation_timer.done:
                    self.game_over = True

        if not self.game_over:
            self.move(dt, window_dimensions[1] - block_size, stone_group)
            self.gravity(dt)
            self.obstacles_collision(self_play, obstacles_group)
        
        if not self.game_over:
            self.coin_pick(coins_group)
            self.get_status()
            self.animate(dt)
        
        if sound == "Unmute":
            self.play_sounds()