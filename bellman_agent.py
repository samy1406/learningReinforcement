import random

class RecylingEnv:
    def __init__(self):
        self.current_state = 1
        self.time_left = 3
        self.rewards = [2,0,0,1,10]
        self.terminal_states = [0, 4]
        self.has_wrapper = False

    
    def reset(self):
        self.current_state = 1
        self.time_left = 3
        self.has_wrapper = False
        return (self.current_state, self. has_wrapper)
    
    def step(self, action):
        intended_state = self.current_state
        if action == 'left' and self.current_state > 0:
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
        
        return (self.current_state, self.has_wrapper), reward, done

env = RecylingEnv()

q_table = {}

for s in range(5):
    for w in [False, True]:
        for a in ['left', 'right']:
            q_table[(s, w, a)] = 0.0
        
    
gamma = 0.9
epsilon = 0.2
episodes = 1000

for episode in range(episodes):
    state = env.reset()
    done = False

    while not done:
        position, has_wrapper = state

        # 1. epsilon greedy action selection
        if random.uniform(0, 1) < epsilon:
            action = random.choice(['left', 'right'])
        else:
            left_value = q_table[(position, has_wrapper, 'left')]
            right_value = q_table[(position, has_wrapper, 'right')]

            if left_value > right_value:
                action = 'left'
            elif right_value > left_value:
                action = 'right'
            else:
                action = random.choice(['left', 'right'])
            
        
        # 2. take the action
        next_state, reward, done = env.step(action)
        next_pos, next_wrap = next_state

        # 3. Bellman equation update
        next_left_val = q_table[(next_pos, next_wrap, 'left')]
        next_right_val = q_table[(next_pos, next_wrap, 'right')]
        max_next_q = max(next_left_val, next_right_val)

        # Q(s, a) = R(s, a) + gamma * max Q(s', a')
        q_table[(position, has_wrapper, action)] = reward + (gamma * max_next_q)

        state = next_state
    

print("Training finished!")
print("Value of going RIGHT from start (State 1, no wrapper):", q_table[(1, False, 'right')])
print("Value of going LEFT from start (State 1, no wrapper):", q_table[(1, False, 'left')])

print("\n--- Final Learned Q-Table ---")
print(f"{'State':<6} | {'Wrapper':<8} | {'Left Value':<12} | {'Right Value':<12}")
print("-" * 47)

for s in range(5):
    for w in [False, True]:
        left_val = q_table[(s, w, 'left')]
        right_val = q_table[(s, w, 'right')]
        
        # We format the values to 4 decimal places for clean reading
        print(f"{s:<6} | {str(w):<8} | {left_val:<12.4f} | {right_val:<12.4f}")