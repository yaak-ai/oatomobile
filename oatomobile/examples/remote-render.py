import gym
import argparse


def run_rendrer(env_name, save_path, interactive):

  # Initializes a 'Breakout-v0' environment.
  env = gym.make(env_name)
  env = gym.wrappers.Monitor(env, save_path)

  # Makes an initial observation.
  obs = env.reset()
  done = False

  while not done:
    # Selects a random action.
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)

    # Renders interactive display.
    if interactive:
      env.render(mode="rgb_array")

  # Book-keeping: closes
  env.close()


if __name__ == '__main__':

  parser = argparse.ArgumentParser("Remote render and saving script")
  parser.add_argument('-v', '--vid', help='Path where to save the videos')
  parser.add_argument('-e', '--env', help='Environment Name')
  parser.add_argument('-i', '--interactive', action='store_true', default=False,
                      help='Interactive visualization')

  args = parser.parse_args()

  run_rendrer(args.env, args.vid, args.interactive)
