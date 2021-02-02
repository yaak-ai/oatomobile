import random
import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset
from oatomobile.simulators.carla import defaults


def plot_coverage(source, destination):

  dataset = CARLADataset(id='processed')

  dataset.plot_coverage(source.as_posix(), destination.as_posix())


if __name__ == '__main__':

  parser = argparse.ArgumentParser("Plot all trajactories in the dataset")
  parser.add_argument('-s', '--source', help='Source Directory', type=Path)
  parser.add_argument('-d', '--destination', help='Destination File', type=Path)

  args = parser.parse_args()

  plot_coverage(args.source, args.destination)
