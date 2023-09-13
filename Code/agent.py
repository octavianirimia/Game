import math
import os
import pygame
import random
import sys
import torch

from neural_memory import DQN, Memory



class Agent():
    def __init__(self, number_of_observation, number_of_actions):

        # Constante
        self.batch_size = 256
        self.gamma = 0.99
        self.tau = 0.005
        self.exploration_rate_start = 1
        self.exploration_rate_stop = 0.05
        self.exploration_rate_decay = 1000
        self.learning_rate = 1e-4
        self.target_net_update_frequency = 1e3
        self.memory_capacity = 100000
        self.steps_done = 0

        self.episode = 0

        # Variabile joc
        self.record = 0
        self.player_previous_position = 200
        self.obstacle_passed = False
        self.obstacles = {
            "Spikes": 1, 
            "Fire": 2,
            "Bat": 3,
            "Fat_bird": 4,
            "Snail": 5,
            "Rino": 6
        }

        self.number_of_actions = number_of_actions

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.online_net = DQN(number_of_observation, number_of_actions).to(self.device)
        self.target_net = DQN(number_of_observation, number_of_actions).to(self.device)
        self.target_net.load_state_dict(self.online_net.state_dict())
        self.target_net.eval()

        self.optimizer = torch.optim.AdamW(self.online_net.parameters(), lr = self.learning_rate, amsgrad = True)
        
        self.loss_function = torch.nn.SmoothL1Loss().to(device = self.device)

        self.loss = None
        
        self.memory = Memory(self.memory_capacity)


    def get_state(self, player, offset, groups):

        idle = player.status == "Idle"
        left_direction = player.direction.x == -1
        right_direction = player.direction.x == 1
        jump = player.status == "Jump"

        state = [
            # Mișcare
            idle,
            left_direction,
            right_direction,
            jump,

            # Jucătorul
            player.rect.left,
            player.rect.top,
            player.rect.right,
            player.rect.bottom,

            # Limita
            offset, # Offset atins

            # Tipul pericolului
            self.obstacles[type(groups[0].sprites()[0]).__name__],
            self.obstacles[type(groups[0].sprites()[1]).__name__],

            # Primul pericol
            groups[0].sprites()[0].rect.left,
            groups[0].sprites()[0].rect.top,
            groups[0].sprites()[0].rect.right,
            groups[0].sprites()[0].rect.bottom,
            
            # Al doilea pericol
            groups[0].sprites()[1].rect.left,
            groups[0].sprites()[1].rect.top,
            groups[0].sprites()[1].rect.right,
            groups[0].sprites()[1].rect.bottom,

            # Viteza pericolelor
            groups[0].sprites()[0].speed if hasattr(groups[0].sprites()[0], "self.speed") else 0,
            groups[0].sprites()[1].speed if hasattr(groups[0].sprites()[1], "self.speed") else 0,
            
            # Recompensă
            groups[2].sprites()[0].rect.left,
            groups[2].sprites()[0].rect.top,
            groups[2].sprites()[0].rect.right,
            groups[2].sprites()[0].rect.bottom
            ]

        return torch.tensor([state], dtype = torch.float32, device = self.device)
    

    def select_action(self, state, train):

        if train is not None:# and self.steps_done <= self.maximum_steps:
            exploration_rate = self.exploration_rate_stop+ (self.exploration_rate_start - self.exploration_rate_stop) * \
                math.exp(-1. * self.steps_done / self.exploration_rate_decay)
            
            self.steps_done += 1

            if random.random() > exploration_rate:
                with torch.no_grad():
                    action = self.online_net(state).max(1)[1].view(1, 1)
            else:
                action = torch.tensor([[random.randint(0, self.number_of_actions - 1)]], dtype = torch.long, device = self.device)
        
        else:
            with torch.no_grad():
                action = self.online_net(state).max(1)[1].view(1, 1)

        return action


    def step(self, player, action, offset, groups):

        done = False

        # Acțiunile pe care le poate executa jucătorul

        if action == 0:
            player.direction.x = 0

        elif action == 1:
            player.status_direction = "left"

            if player.rect.left - offset > 0:
                player.direction.x = -1

        elif action == 2:
            player.status_direction = "right"
            player.direction.x = 1

        elif action == 3 and player.on_ground:
            player.direction.y = -1.6
        

        # Funcția recompensă

        if player.dead or player.rect.left < offset:
            reward = -100
            self.episode += 1
            done = True

        elif player.rect.centerx >= 14500:
            reward = 100
        
        elif player.picked_coin:
            reward = 20
            player.picked_coin = False
        
        elif player.rect.centerx > self.player_previous_position:
            reward = 1
        
        elif player.rect.centerx == self.player_previous_position:
            reward = -30
        
        elif player.rect.centerx < self.player_previous_position:
            reward = -50

        self.player_previous_position = player.rect.centerx


        reward = torch.tensor([reward], dtype = torch.long, device = self.device)

        return None if done else self.get_state(player, offset, groups), reward, done


    def cache(self, state, action, reward, next_state, done):

        done = torch.tensor([done], dtype = torch.long, device = self.device)

        self.memory.add(state, action, reward, next_state, done)
    

    def learn(self):
        
        if self.memory.get_size() >= self.batch_size:

            # Eșantion din memorie
            state_batch, action_batch, reward_batch, next_state_batch, done_batch = self.recall()

            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, next_state_batch)), dtype = torch.bool, device = self.device)
            non_final_next_states = torch.cat([s for s in next_state_batch if s is not None]).to(device = self.device)

            state_action_values = self.online_net(state_batch).gather(1, action_batch).to(device = self.device)

            next_state_values = torch.zeros(self.batch_size, device = self.device)

            with torch.no_grad():
                next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0]
            
            expected_state_action_values = (1 - done_batch) * self.gamma * next_state_values + reward_batch

            self.loss = self.loss_function(state_action_values, expected_state_action_values.unsqueeze(1)).to(device = self.device)
            self.optimizer.zero_grad()
            self.loss.backward()
            torch.nn.utils.clip_grad.clip_grad_value_(self.online_net.parameters(), 100)
            self.optimizer.step()
        
        # Actualizarea rețelei țintă
        if self.steps_done % self.target_net_update_frequency == 0:
            self.update_target_net()
    

    def recall(self): # din memorie

        state_batch, action_batch, reward_batch, next_state_batch, done_batch = self.memory.sample(self.batch_size)


        state_batch = torch.cat(state_batch).to(device = self.device)
        action_batch = torch.cat(action_batch).to(device = self.device)
        reward_batch = torch.cat(reward_batch).to(device = self.device)
        done_batch = torch.cat(done_batch).to(device = self.device)

        return state_batch, action_batch, reward_batch, next_state_batch, done_batch
    

    def update_target_net(self):
        
        online_net_state_dict = self.online_net.state_dict()
        target_net_state_dict = self.target_net.state_dict()

        for key in online_net_state_dict:
            target_net_state_dict[key] = online_net_state_dict[key] * self.tau + target_net_state_dict[key] * (1 - self.tau)
        
        self.target_net.load_state_dict(target_net_state_dict)
    

    def save(self, player, train):

        if player.rect.centerx > self.record:
            file = open(os.path.join("Python", "Game", "AI model", f"Data {train.lower()}.txt"), "w")
            file.write(f"Distance: {player.rect.centerx}\nReward: {player.reward}\nCoins: {player.coins}")
            file.close()

            torch.save({
                "Online net": self.online_net.state_dict(),
                "Target net": self.target_net.state_dict(),
                "Optimizer": self.optimizer.state_dict(),
                "Loss": self.loss
            }, os.path.join("Python", "Game", "AI model", f"Model {train.lower()}.pth"))

            self.record = player.rect.centerx

            if self.record >= 14500:
                print("Training complete")
                pygame.quit()
                sys.exit()
    

    def load(self, train):

        model = torch.load(os.path.join("Python", "Game", "AI model", f"Model {train.lower()}.pth"))

        self.online_net.load_state_dict(model["Online net"])
        self.target_net.load_state_dict(model["Target net"])
        self.optimizer.load_state_dict(model["Optimizer"])
        self.loss = model["Loss"]

        self.online_net.eval().to(device = self.device)
        self.target_net.eval().to(device = self.device)