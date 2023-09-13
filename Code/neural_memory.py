import random
import torch



class Memory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.experience = {"State": [], "Action": [], "Reward": [], "Next state": [], "Done": []}
    

    def get_size(self):

        return len(self.experience["State"])
    

    def add(self, state, action, reward, next_state, done):

        # Ștergerea unei experiențe mai vechi dacă memoria e plină
        if len(self.experience["State"]) >= self.capacity:
            del self.experience["State"][0]
            del self.experience["Action"][0]
            del self.experience["Reward"][0]
            del self.experience["Next state"][0]
            del self.experience["Done"][0]

        # Adăugarea unei noi experiențe
        self.experience["State"].append(state)
        self.experience["Action"].append(action)
        self.experience["Reward"].append(reward)
        self.experience["Next state"].append(next_state)
        self.experience["Done"].append(done)

    
    def sample(self, batch_size):

        index = random.sample(range(self.get_size()), batch_size)

        state = [self.experience["State"][i] for i in index]
        action = [self.experience["Action"][i] for i in index]
        reward = [self.experience["Reward"][i] for i in index]
        next_state = [self.experience["Next state"][i] for i in index]
        done = [self.experience["Done"][i] for i in index]

        return state, action, reward, next_state, done



class DQN(torch.nn.Module):

    def __init__(self, number_of_observations, number_of_actions):
        torch.nn.Module.__init__(self)
        self.layer1 = torch.nn.Linear(number_of_observations, 256)
        self.layer2 = torch.nn.Linear(256, 128)
        self.layer3 = torch.nn.Linear(128, number_of_actions)

    def forward(self, x):
        
        x = torch.nn.functional.relu(self.layer1(x))
        x = torch.nn.functional.relu(self.layer2(x))
        return self.layer3(x)