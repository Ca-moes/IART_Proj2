import gym
import numpy as np
from gym_neutreeko.envs import NeutreekoEnv

class Agent:
    @staticmethod
    def choice_random(env):
        player = env.game.current_player
        possible_moves = env.game.get_possible_moves(player)

        i_random = np.random.randint(len(possible_moves))
        print(possible_moves[i_random])
        return possible_moves[i_random]


env = NeutreekoEnv(render_mode='terminal')
print(env.action_space)
#> Box(0, 60, (2,), uint8)  <- Isto vai ser diferente
print(env.observation_space)
#> Box(0, 2, (5, 5), int8)

NB_EPISODES = 1
for episode in range(1, NB_EPISODES+1):
    env.reset()
    done = False
    while not done:
        action = Agent.choice_random(env)
        obs, reward, done, info = env.step(action)
        print(f"{info['turn']: <4} | {info['player_name']} | {str(info['move_type']): >16} | reward={reward: >4} ")
        env.render()
    print(f"Episode {info['turn']: <4} finished after {env.game.turns_count} turns \n")
env.close()
