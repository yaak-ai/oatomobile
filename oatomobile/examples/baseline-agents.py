import argparse

import gym
import torch
import oatomobile
import oatomobile.baselines.rulebased

from oatomobile.baselines.torch import CILAgent, DIMAgent, RIPAgent
from oatomobile.baselines.torch import BehaviouralModel, ImitativeModel, RIPAgent

AGENT_LIST = {'dim': DIMAgent, 'rip': RIPAgent, 'cil': CILAgent}


def run_agent(agent, ckpt, town, num_vehicles, num_pedestrians,
              save_path=None, interactive=False):
  # Initializes a CARLA environment.
  env = oatomobile.envs.CARLAEnv(town=town, num_vehicles=num_vehicles,
                                 num_pedestrians=num_pedestrians)
  if save_path is not None:
    env = oatomobile.MonitorWrapper(env, output_fname=save_path)

  # Makes an initial observation.
  obs = env.reset()
  done = False

  model = ImitativeModel()
  model.load_state_dict(torch.load(ckpt))

  agent = AGENT_LIST[agent](environment=env, model=model)

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
  parser.add_argument('-w', '--weights', help='Model weights files')
  parser.add_argument('-v', '--vid', help='Path where to save the videos')
  parser.add_argument('-t', '--town', help='Town Name')
  parser.add_argument('-i', '--interactive', action='store_true', default=False,
                      help='Interactive visualization')
  parser.add_argument('-nv', '--num-vehicles', dest='n_vehicles',
                      help='Number of vehicles', default=100, type=int)
  parser.add_argument('-np', '--num-pedestrians', dest='n_pedestrians',
                      help='Number of pedestrians', default=100, type=int)

  args = parser.parse_args()

  run_agent(args.agent, args.weights, args.town, args.n_vehicles,
            args.n_pedestrians, args.vid, args.interactive)
