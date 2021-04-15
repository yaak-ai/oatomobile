import argparse
import logging
import json

import numpy as np

from tqdm import tqdm
from pathlib import Path
from prettytable import PrettyTable

import subprocess as sp
import multiprocessing as mp

from oatomobile.utils.log import get_logger

logger = get_logger(__name__)


def merge_stats(return_dict, nj):

    stats = {
        "obstacle": 0,
        "collision": 0,
        "red_light_invasion": 0,
        "rss": 0,
        "clean": 0,
    }
    ep_stats = {}

    bookmarks = [return_dict[idx]["stats"] for idx in range(nj)]
    episode_bookmarks = [return_dict[idx]["epsisode_stats"] for idx in range(nj)]

    for ep in bookmarks:
        for k, v in ep.items():
            stats[k] += v

    for b in episode_bookmarks:
        ep_stats.update(b)

    return stats, ep_stats


def parse_episodes(args):

    (
        episodes,
        chunk_size,
        return_dict,
        group_number,
    ) = args

    stats = return_dict[group_number]["stats"]
    epsisode_stats = return_dict[group_number]["epsisode_stats"]

    episodes_p = episodes[group_number * chunk_size : (group_number + 1) * chunk_size]
    pbar = tqdm(episodes_p, position=group_number + 1, leave=False, ascii=True)

    for episode in pbar:

        if not episode.joinpath("metadata").is_file():
            continue

        with episode.joinpath("metadata").open() as pfile:
            metadata = pfile.readlines()
            metadata = [m.strip() for m in metadata]

        # pbar_metadata = tqdm(
        #     metadata, position=2 * group_number + 1, ascii=True, leave=False
        # )

        obstacle, collision, red_light_invasion, rss = [], [], [], []

        for fname in metadata:
            npz_file = episode.joinpath(fname + ".npz")
            annotations = np.load(npz_file)
            obstacle.append(annotations["obstacle"])
            collision.append(annotations["collision"])
            red_light_invasion.append(annotations["red_light_invasion"])
            rss.append(annotations["rss"])

        epsisode_stats[episode.name] = {
            "obstacle": int(np.any(obstacle)),
            "collision": int(np.any(collision)),
            "red_light_invasion": int(np.any(red_light_invasion)),
            "rss": int(np.any(rss)),
        }

        stats["obstacle"] += epsisode_stats[episode.name]["obstacle"]
        stats["collision"] += epsisode_stats[episode.name]["collision"]
        stats["red_light_invasion"] += epsisode_stats[episode.name][
            "red_light_invasion"
        ]
        stats["rss"] += epsisode_stats[episode.name]["rss"]

        stats["clean"] += int(
            np.all(
                [
                    epsisode_stats[episode.name]["obstacle"] == 0,
                    epsisode_stats[episode.name]["collision"] == 0,
                    epsisode_stats[episode.name]["red_light_invasion"] == 0,
                    epsisode_stats[episode.name]["rss"] == 0,
                ]
            )
        )

        pbar.set_description(f"[#{group_number}] {episode.name}: {stats}")


def generate_stats(location, json_path, nj, show):

    episodes = list(location.iterdir())

    logger.info(f"Found {len(episodes)} episodes at {location}")

    table = PrettyTable()
    table.field_names = ["bookmark", "count"]
    table.align = "l"

    chunk_size = len(episodes) // nj

    logger.info(f"Parsing {len(episodes)} episodes on {nj} chunks")

    p = mp.Pool(int(nj))
    m = mp.Manager()
    return_dict = m.dict()

    for n in range(nj):
        ep = m.dict()
        ep["obstacle"] = 0
        ep["collision"] = 0
        ep["red_light_invasion"] = 0
        ep["rss"] = 0
        ep["clean"] = 0
        return_dict[n] = {"stats": ep, "epsisode_stats": m.dict()}

    args = [
        (
            episodes,
            chunk_size,
            return_dict,
            idx,
        )
        for idx in range(nj)
    ]

    p.map(parse_episodes, args)

    stats, epsisode_stats = merge_stats(return_dict, nj)

    for bookmark_type, count in stats.items():
        table.add_row([bookmark_type, count])

    if show:
        print(table)

    if json_path:
        with json_path.open("w") as pfile:
            json.dump({"episodes": epsisode_stats, "stats": stats}, pfile)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Generate dataset stats for Carla")
    parser.add_argument(
        "-l",
        "--location",
        dest="location",
        type=Path,
        help="Root path to data colection",
    )
    parser.add_argument(
        "-j",
        "--json",
        dest="json_path",
        type=Path,
        help="JSON with data statistics",
        default=None,
    )
    parser.add_argument(
        "-n",
        "--nj",
        dest="nj",
        type=int,
        help="Number of concurrent jobs to run",
        default=1,
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

    generate_stats(args.location, args.json_path, args.nj, args.show)
