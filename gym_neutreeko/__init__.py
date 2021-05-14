from gym.envs.registration import register

register(
    id='neutreeko-v0',
    entry_point='gym_neutreeko.envs:NeutreekoEnv',
)
