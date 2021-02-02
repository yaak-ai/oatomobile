import argparse
from pathlib import Path
from oatomobile.datasets.carla import CARLADataset


def plot_datum(source, destination):

  dataset = CARLADataset(id='processed')

  dataset.plot_datum(source.as_posix(), destination.as_posix())


if __name__ == '__main__':

  parser = argparse.ArgumentParser("Plot all datum in the file")
  parser.add_argument('-s', '--source', help='Source File', type=Path)
  parser.add_argument('-d', '--destination', help='Destination File', type=Path)

  args = parser.parse_args()

  plot_datum(args.source, args.destination)
