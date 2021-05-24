import gym
import numpy as np
from gym_neutreeko.envs import NeutreekoEasyEnv


class Agent:
    @staticmethod
    def choice_random(env):
        player = env.game.current_player
        possible_moves = env.game.get_possible_moves(player, only_valid=True)

        i_random = np.random.randint(len(possible_moves))
        return possible_moves[i_random]


env = NeutreekoEasyEnv(render_mode='terminal')
print(env.action_space)  # Discrete(24)
print(env.observation_space)  # Box(0, 2, (5, 5), int8)

NB_EPISODES = 10
for episode in range(1, NB_EPISODES + 1):
    env.reset()
    done = False
    while not done:
        action = Agent.choice_random(env)
        obs, reward, done, info = env.step(action)
        print(f"{info['turn']: <4} | {str(info['direction']): >10} | reward={reward: >3} ")
        env.render()
    print(f"Episode {info['turn']: <4} finished after {env.game.turns_count} turns \n")
env.close()

# For use with complete game
# NB_EPISODES = 5
# for episode in range(1, NB_EPISODES + 1):
#     env.reset()
#     done = False
#     while not done:
#         action = Agent.choice_random(env)
#         obs, reward, done, info = env.step(action)
#         print(f"{info['turn']: <4} | {info['player_name']} | {str(info['direction']): >10} | reward={reward: >3} ")
#         env.render()
#     print(f"Episode {info['turn']: <4} finished after {env.game.turns_count} turns \n")
# env.close()
