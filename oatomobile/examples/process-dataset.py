import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset


def process_dataset(source, destination, is_video, nj):

    dataset = CARLADataset(id="raw")

    fn = dataset.process_video if is_video else dataset.process

    fn(source.as_posix(), destination.as_posix(), num_jobs=nj)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Remote render and saving script")
    parser.add_argument("-s", "--source", help="Source Directory", type=Path)
    parser.add_argument("-d", "--destination", help="Destination Directory", type=Path)
    parser.add_argument(
        "-v",
        "--video",
        action="store_true",
        default=False,
        help="Its a video dataset",
    )
    parser.add_argument(
        "-n",
        "--nj",
        dest="nj",
        type=int,
        help="Number of concurrent jobs to run",
        default=1,
    )

    args = parser.parse_args()

    process_dataset(args.source, args.destination, args.video, args.nj)
