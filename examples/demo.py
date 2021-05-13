import gym

from gym_neutreeko.envs import NeutreekoEnv

class Agent:
    @staticmethod
    def choice_random(env):
        pass


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
