import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset


def download_carla_dataset(id, destination):

  dataset = CARLADataset(id=id)

  dataset.download_and_prepare(destination.as_posix())


if __name__ == '__main__':

  parser = argparse.ArgumentParser("Remote render and saving script")
  parser.add_argument('-i', '--id', help='Id or Type', default='processed',
                      choices=['raw', 'examples', 'processed'])
  parser.add_argument('-d', '--destination', help='Save path', type=Path)

  args = parser.parse_args()

  download_carla_dataset(args.id, args.destination)
