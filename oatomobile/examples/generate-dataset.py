import random
import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset
from oatomobile.simulators.carla import defaults


def generate_dataset(
    town, num_pedestrians, num_vehicles, num_steps, destination, port, tm_port
):

    dataset = CARLADataset(id="raw")

    if town is None:
        town = random.sample(defaults.AVAILABLE_CARLA_TOWNS, 1)[0]

    print("Generating dataset for {}".format(town))

    SENSORS = [
        "rss",
        "lidar",
        "obstacle",
        "collision",
        "lane_invasion",
        "red_light_invasion",
        "is_at_traffic_light",
        "traffic_light_state",
        "actors_tracker",
        "front_camera_rgb",
        "right_camera_rgb",
        "left_camera_rgb",
        "rear_camera_rgb",
        "bird_view_camera_rgb",
        "control",
        "velocity",
        "acceleration",
        "location",
    ]

    dataset.collect(
        town,
        destination.as_posix(),
        num_vehicles,
        num_pedestrians,
        num_steps,
        sensors=SENSORS,
        port=port,
        tm_port=tm_port,
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
    parser.add_argument(
        "-w", "--walkers", help="Number of pedestrians", type=int, default=100
    )
    parser.add_argument(
        "-v", "--vehicles", help="Number of vehicles", type=int, default=100
    )
    parser.add_argument(
        "-s", "--steps", help="Number of simulatiom steps", type=int, default=1000
    )
    parser.add_argument("-d", "--destination", help="Save path", type=Path)
    parser.add_argument("-p", "--port", help="Carla Port", type=int, default=2000)
    parser.add_argument(
        "-m", "--tm_port", help="Carla Traffic Manager Port", type=int, default=8000
    )

    args = parser.parse_args()

    generate_dataset(
        args.town,
        args.walkers,
        args.vehicles,
        args.steps,
        args.destination,
        args.port,
        args.tm_port,
    )
