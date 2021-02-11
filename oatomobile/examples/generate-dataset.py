import random
import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset
from oatomobile.simulators.carla import defaults


def generate_dataset(town, num_pedestrians, num_vehicles, num_steps, destination):

    dataset = CARLADataset(id="raw")

    if town is None:
        town = random.sample(defaults.AVAILABLE_CARLA_TOWNS, 1)[0]

    print("Generating dataset for {}".format(town))

    SENSORS = [
        "rss",
        "lidar",
        "front_camera_rgb",
        "control",
        "velocity",
        "acceleration",
        "collision",
        "lane_invasion",
        "red_light_invasion",
        "is_at_traffic_light",
        "traffic_light_state",
        "actors_tracker",
    ]

    dataset.collect(
        town,
        destination.as_posix(),
        num_vehicles,
        num_pedestrians,
        num_steps,
        sensors=SENSORS,
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Remote render and saving script")
    parser.add_argument(
        "-t",
        "--town",
        help="Town type",
        default=None,
        choices=defaults.AVAILABLE_CARLA_TOWNS,
    )
    parser.add_argument("-p", "--pedestrians", help="Town type", type=int, default=100)
    parser.add_argument(
        "-v", "--vehicles", help="Number of vehicles", type=int, default=100
    )
    parser.add_argument(
        "-s", "--steps", help="Number of simulatiom steps", type=int, default=1000
    )
    parser.add_argument("-d", "--destination", help="Save path", type=Path)

    args = parser.parse_args()

    generate_dataset(
        args.town, args.pedestrians, args.vehicles, args.steps, args.destination
    )
