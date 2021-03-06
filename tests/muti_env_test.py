# Simple env test.
import json
import select
import time
import logging

import gym
import matplotlib.pyplot as plt
import minerl
import numpy as np
from minerl.env.core import MineRLEnv

import coloredlogs
coloredlogs.install(logging.DEBUG)


NUM_EPISODES=10

def main():
    """
    Tests running a simple environment.
    """
    envs = [gym.make('MineRLTreechop-v0') for _ in range(3)]
    
    actions = [env.action_space.sample() for _ in range(2000)]
    xposes = []
    for _ in range(NUM_EPISODES):
        obs, info = env.reset()
        done = False
        xpos = []
        for act in actions:
            obs, reward, done, info = env.step(
                act)
            
            correct_info = json.loads(info)
            xpos.append([correct_info["XPos"], correct_info["YPos"], correct_info["ZPos"], correct_info["Yaw"]])
        xposes.append(xpos)
    

    y = np.array(xposes)
    plt.plot(y[:,:,0].T, y[:,:,2].T)
    plt.show()
    print("Demo complete.")
    
if __name__ == "__main__":
    main()