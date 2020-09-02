import argparse

import gym
import torch
import oatomobile
import oatomobile.baselines.rulebased

from oatomobile.baselines.torch import CILAgent, DIMAgent, RIPAgent
from oatomobile.baselines.torch import BehaviouralModel, ImitativeModel, RIPAgent

AGENT_LIST = {'dim': DIMAgent, 'rip': RIPAgent, 'cil': CILAgent}


def run_agent(agent, ckpts, algorithm, town, num_vehicles, num_pedestrians,
              save_path=None, interactive=False):

  # Initializes a CARLA environment.
  env = oatomobile.envs.CARLAEnv(town=town, num_vehicles=num_vehicles,
                                 num_pedestrians=num_pedestrians)
  if save_path is not None:
    env = oatomobile.MonitorWrapper(env, output_fname=save_path)

  # Makes an initial observation.
  obs = env.reset()
  done = False
  

  if agent=='cil':
    model = BehaviouralModel()
  else:
    model = ImitativeModel()

  models = [model for _ in range(len(ckpts))]
  for model, ckpt in zip(models, ckpts):
    model.load_state_dict(torch.load(ckpt))
    model.eval()

  if agent=='rip':
    agent = AGENT_LIST[agent](
        environment=env,
        models=models,
        algorithm=algorithm,)
  else:
    agent = AGENT_LIST[agent](environment=env, model=models[0])


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
  parser.add_argument('-w', '--weights', nargs='+',
                      help='Model weights files. Example: -w model1 model2')
  parser.add_argument('-g', '--algorithm', help='RIP varient algorihtm',
                      choices=['WCM', 'MA', 'BCM'], default='MA')
  parser.add_argument('-v', '--vid', help='Path where to save the videos')
  parser.add_argument('-t', '--town', help='Town Name')
  parser.add_argument('-i', '--interactive', action='store_true', default=False,
                      help='Interactive visualization')
  parser.add_argument('-nv', '--num-vehicles', dest='n_vehicles',
                      help='Number of vehicles', default=100, type=int)
  parser.add_argument('-np', '--num-pedestrians', dest='n_pedestrians',
                      help='Number of pedestrians', default=100, type=int)

  args = parser.parse_args()
  run_agent(args.agent, args.weights, args.algorithm, args.town, args.n_vehicles,
            args.n_pedestrians, args.vid, args.interactive)


