import gym
import numpy as np
import matplotlib.pyplot as plt

from examples.QAgent import QAgent
from examples.RandomAgent import RandomAgent
from gym_neutreeko.envs import NeutreekoEasyEnv

env = NeutreekoEasyEnv(render_mode='terminal')
agent = QAgent()
print(env.action_space)  # Discrete(24)
print(env.observation_space)  # Box(0, 2, (5, 5), int8)

# Creating lists to keep track of reward and epsilon values
training_rewards = []
epsilons = []

NB_EPISODES = 15000
for episode in range(1, NB_EPISODES + 1):
    # Resetting the environment each time as per requirement
    env.reset()
    # Starting the tracker for the rewards
    total_training_rewards = 0

    done = False
    while not done:
        action = agent.choice(env)
        obs, reward, done, info = env.step(action)
        total_training_rewards += reward
        # print(f"{info['turn']: <4} | {str(info['direction']): >10} | reward={reward: >3} ")
        # env.render()
        agent.update(obs, reward, done, info)
    print(f"Episode {episode: <4} finished after {env.game.turns_count} turns")

    # Cutting down on exploration by reducing the epsilon
    agent.epsilon = agent.min_epsilon + (agent.max_epsilon - agent.min_epsilon)*np.exp(-agent.decay*episode)

    # Adding the total reward and reduced epsilon values
    training_rewards.append(total_training_rewards)
    epsilons.append(agent.epsilon)
print(f'Highest board id -> {agent.lastID}')
env.close()

# Visualizing results and total reward over all episodes
x = range(NB_EPISODES)
plt.plot(x, training_rewards)
plt.xlabel('Episode')
plt.ylabel('Training total reward')
plt.title('Total rewards over all episodes in training')
plt.show()

# Visualizing the epsilons over all episodes
plt.plot(epsilons)
plt.xlabel('Episode')
plt.ylabel('Epsilon')
plt.title("Epsilon for episode")
plt.show()
# For use with complete game
# NB_EPISODES = 5
# for episode in range(1, NB_EPISODES + 1):
#     env.reset()
#     done = False
#     while not done:
#         action = agent.choice_random(env)
#         obs, reward, done, info = env.step(action)
#         print(f"{info['turn']: <4} | {info['player_name']} | {str(info['direction']): >10} | reward={reward: >3} ")
#         env.render()
#     print(f"Episode {info['turn']: <4} finished after {env.game.turns_count} turns \n")
# env.close()
