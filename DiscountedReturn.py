''' 
problem statement
Goal: maximize the return (rewards)
Number of states: 5
type of states: intial normal terminal
agent possible actions: left or right
additional rule: garbage collector coming in 3 min, it takes 1 min to move between states
'''

import random

class RecylingEnv:
    def __init__(self):
        self.current_state = 1

        self.time_left = 3

        self.rewards = [2, 0, 0, 1, 10]

        self.terminal_states = [0, 4]
        
        self.has_wrapper = False
    
    def reset(self):
        self.current_state = 1
        self.time_left = 3
        self.has_wrapper = False
        return self.current_state
    
    def step(self, action):
        intended_state = self.current_state
        if action == 'left' and self.current_state >0:
            intended_state -= 1
        elif action == 'right' and self.current_state < 4:
            intended_state += 1
        
        if intended_state in self.terminal_states and not self.has_wrapper:
            pass
        else:
            self.current_state = intended_state

        if self.current_state == 3:
            self.has_wrapper = True

        self.time_left -= 1

        reward = self.rewards[self.current_state]

        done = False
        if self.time_left == 0 or self.current_state in self.terminal_states:
            done = True

        return self.current_state, reward, done


env = RecylingEnv()
state = env.reset()
done = False

t = 0
discounted_return = 0

print(f"Starting in the state {state}")

while not done:
    action = random.choice(['left', 'right'])

    state, reward, done = env.step(action)
    discounted_reward = (0.9 ** t) * reward
    discounted_return += discounted_reward
    t += 1
    print(f"Action: {action:5} | New State: {state} | Reward: {reward}")

print("Episode finished!")
print("-" * 35)
print(f"Total Discounted Return (R) = {discounted_return:.4f}")