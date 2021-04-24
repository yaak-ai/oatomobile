import argparse
import logging
import json

import numpy as np

from tqdm import tqdm
from pathlib import Path
from prettytable import PrettyTable

import itertools
import subprocess as sp
import multiprocessing as mp

from oatomobile.utils.log import get_logger

logger = get_logger(__name__)


def generate_stats(json_path, show):

    bookmarks = {
        "": None,
        "obstacle": 0,
        "collision": 1,
        "red_light_invasion": 2,
        "rss": 3,
        "clean": 4,
        "lane_invasion": 5,
    }

    mat = np.zeros([6, 6]).astype(int)
    print(mat.shape)

    table = PrettyTable()
    table.field_names = bookmarks
    table.align = "l"

    with json_path.open() as pfile:
        data = json.load(pfile)

    ep_stats = data["episodes"]
    global_stats = data["stats"]

    mat[4, 4] = global_stats["clean"]

    for ep_name, incidents in ep_stats.items():
        all_incidents = list([(k, v) for k, v in incidents.items() if v == 1])
        for (k, v) in all_incidents:
            mat[bookmarks[k], bookmarks[k]] += v
        if len(all_incidents) == 1:
            continue
        for p1, p2 in itertools.permutations(all_incidents, 2):
            mat[bookmarks[p1[0]], bookmarks[p2[0]]] += p2[1]

    for name, idx in bookmarks.items():
        if idx is None:
            continue
        logger.info(f"{mat[idx]}")
        mat[idx, idx] -= sum(mat[idx]) - mat[idx, idx]
        table.add_row([name] + list(mat[idx]))

    if show:
        print(table)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Generate Confusion matrix stats for Carla")
    parser.add_argument(
        "-j",
        "--json",
        dest="json_path",
        type=Path,
        help="JSON with data statistics",
        default=None,
    )
    parser.add_argument(
        "-s",
        "--show",
        dest="show",
        help="Show stats in table",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()

    generate_stats(args.json_path, args.show)
