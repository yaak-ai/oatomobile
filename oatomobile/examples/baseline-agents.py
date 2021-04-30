import argparse

import gym
import torch
import oatomobile
import oatomobile.baselines.rulebased

from oatomobile.baselines.torch import CILAgent, DIMAgent, RIPAgent
from oatomobile.baselines.torch import BehaviouralModel, ImitativeModel, RIPAgent

AGENT_LIST = {"dim": DIMAgent, "rip": RIPAgent, "cil": CILAgent}


def run_agent(
    agent,
    ckpt,
    town,
    num_vehicles,
    num_pedestrians,
    length,
    down_sampling,
    save_path=None,
    interactive=False,
    port=2000,
    tm_port=8000,
    in_channels=2,
):
    # Initializes a CARLA environment.
    CARLA_SENSORS = (
        "goal",
        "lidar",
        "bird_view_camera_rgb",
        "bird_view_camera_cityscapes",
        "control",
        "location",
        "rotation",
        "velocity",
        "is_at_traffic_light",
        "traffic_light_state",
    )
    env = oatomobile.envs.CARLAEnv(
        town=town,
        num_vehicles=num_vehicles,
        num_pedestrians=num_pedestrians,
        port=port,
        tm_port=tm_port,
        sensors=CARLA_SENSORS,
    )
    if save_path is not None:
        env = oatomobile.MonitorWrapper(env, output_fname=save_path)

    # Makes an initial observation.
    # obs is in RGB space if using 2 channels use first two
    obs = env.reset()
    done = False

    model = ImitativeModel(output_shape=[down_sampling, 2], in_channels=in_channels)
    model.load_state_dict(torch.load(ckpt))
    model.eval()

    # agent = AGENT_LIST[agent](environment=env, model=model, length=length)
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Remote render and saving script")
    parser.add_argument(
        "-a",
        "--agent",
        help="Type of Agent",
        choices=["dim", "rip", "cil"],
        default="dim",
    )
    parser.add_argument("-w", "--weights", help="Model weights files")
    parser.add_argument(
        "-s",
        "--sampling",
        dest="sampling",
        type=int,
        default=4,
        help="Downsampling for trajactory",
    )
    parser.add_argument(
        "-l",
        "--length",
        dest="length",
        type=int,
        default=80,
        help="Length of generated trajactory",
    )
    parser.add_argument("-v", "--vid", help="Path where to save the videos")
    parser.add_argument("-t", "--town", help="Town Name")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        default=False,
        help="Interactive visualization",
    )
    parser.add_argument(
        "-nv",
        "--num-vehicles",
        dest="n_vehicles",
        help="Number of vehicles",
        default=100,
        type=int,
    )
    parser.add_argument(
        "-np",
        "--num-pedestrians",
        dest="n_pedestrians",
        help="Number of pedestrians",
        default=100,
        type=int,
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        help="Port for Carla",
        default=2000,
        type=int,
    )
    parser.add_argument(
        "-m",
        "--tm_port",
        dest="tm_port",
        help="Port for Carla Traffic Manager",
        default=8000,
        type=int,
    )
    parser.add_argument(
        "-c",
        "--in_channels",
        dest="in_channels",
        help="Input channels in sensor data",
        default=2,
        type=int,
    )

    args = parser.parse_args()

    run_agent(
        args.agent,
        args.weights,
        args.town,
        args.n_vehicles,
        args.n_pedestrians,
        args.length,
        args.sampling,
        args.vid,
        args.interactive,
        args.port,
        args.tm_port,
        args.in_channels,
    )
