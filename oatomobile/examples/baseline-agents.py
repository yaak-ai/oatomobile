import argparse

import gym
import torch
import oatomobile
import oatomobile.baselines.rulebased

from oatomobile.baselines.torch import BehaviouralModel, CILAgent, \
    ImitativeModel, RIPAgent

AGENT_LIST = {'dim': CILAgent, 'rip': RIPAgent, 'cil': ImitativeModel}


def run_agent(agent, town, save_path=None, interactive=False):
  # Initializes a CARLA environment.
  env = oatomobile.envs.CARLAEnv(town=town)
  if save_path is not None:
    env = oatomobile.MonitorWrapper(env, output_fname=save_path)

  # Makes an initial observation.
  obs = env.reset()
  done = False

  models = [oatomobile.baselines.torch.ImitativeModel() for _ in range(4)]

  agent = AGENT_LIST[agent](environment=env, models=models, algorithm="WCM")

  while not done:
    # Selects a random action.
    action = agent.act(obs)
    obs, reward, done, info = env.step(action)

    # Renders interactive display.
    if interactive:
      env.render(mode="human")

  # Book-keeping: closes
  env.close()


if __name__ == '__main__':

  parser = argparse.ArgumentParser("Remote render and saving script")
  parser.add_argument('-a', '--agent', help='Type of Agent',
                      choices=['dim', 'rip', 'cil'], default='dim')
  parser.add_argument('-v', '--vid', help='Path where to save the videos')
  parser.add_argument('-t', '--town', help='Town Name')
  parser.add_argument('-i', '--interactive', action='store_true', default=False,
                      help='Interactive visualization')

  args = parser.parse_args()

  run_agent(args.agent, args.town, args.vid, args.interactive)
