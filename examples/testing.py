from gym_neutreeko.envs import NeutreekoEasyEnv
from gym_neutreeko.game.engine.gamelogic import NeutreekoEasyGame

env = NeutreekoEasyEnv()
env.reset()

print(env.game.board)
print(env.process(10))
