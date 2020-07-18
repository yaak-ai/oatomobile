import argparse

import gym
import oatomobile


def run_rendrer(town, save_path, interactive):
  # Initializes a CARLA environment.
  env = oatomobile.envs.CARLAEnv(town=town)
  env = gym.wrappers.Monitor(env, save_path)

  # Makes an initial observation.
  obs = env.reset()
  done = False

  while not done:
    # Selects a random action.
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)

    # Renders interactive display.
    if interactive:
      env.render(mode="human")

  # Book-keeping: closes
  env.close()


if __name__ == '__main__':

  parser = argparse.ArgumentParser("Remote render and saving script")
  parser.add_argument('-v', '--vid', help='Path where to save the videos')
  parser.add_argument('-t', '--town', help='Town Name')
  parser.add_argument('-i', '--interactive', action='store_true', default=False,
                      help='Interactive visualization')

  args = parser.parse_args()

  run_rendrer(args.town, args.vid, args.interactive)
