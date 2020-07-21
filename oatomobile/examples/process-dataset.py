import random
import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset
from oatomobile.simulators.carla import defaults


def process_dataset(source, destination):

  dataset = CARLADataset(id='raw')

  dataset.process(source.as_posix(), destination.as_posix())


if __name__ == '__main__':

  parser = argparse.ArgumentParser("Remote render and saving script")
  parser.add_argument('-s', '--source', help='Source Directory', type=Path)
  parser.add_argument('-d', '--destination', help='Destination Directory', type=Path)

  args = parser.parse_args()

  process_dataset(args.source, args.destination)
