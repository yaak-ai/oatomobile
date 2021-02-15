import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset


def build_fron_cam_video(source, destination, type):

    dataset = CARLADataset(id="processed")

    dataset.build_front_cam_video(source.as_posix(), destination.as_posix(), args.type)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Make video from front_camera_rgb")
    parser.add_argument("-s", "--source", help="Source Directory", type=Path)
    parser.add_argument(
        "-t",
        "--type",
        help="Data type to use",
        default="front_camera_rgb",
        choices=["lidar", "front_camera_rgb"],
    )
    parser.add_argument("-d", "--destination", help="Destination Videl file", type=Path)

    args = parser.parse_args()

    build_fron_cam_video(args.source, args.destination, args.type)
