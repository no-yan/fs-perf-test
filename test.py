#!/usr/bin/env python
# Source: https://gist.github.com/indygreg/a50e187f5372807cdcab5ac12bc2feea
# See also: https://gregoryszorc.com/blog/2018/10/29/global-kernel-locks-in-apfs/

import argparse
import multiprocessing
import os
import time


def walk(path):
    for entry in os.listdir(path):
        full = os.path.join(path, entry)

        if os.path.isdir(full):
            walk(full)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j",
        "--jobs",
        default=multiprocessing.cpu_count(),
        type=int,
        help="Number of parallel processes",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=100,
        type=int,
        help="Number of recursive walks to perform",
    )
    parser.add_argument("path", help="Directory to walk")

    args = parser.parse_args()

    pool = multiprocessing.Pool(processes=args.jobs)

    t_start = time.time()
    for _ in range(args.limit):
        pool.apply_async(walk, (args.path,))

    pool.close()
    pool.join()
    t_end = time.time()
    duration = t_end - t_start

    print(
        "ran %d walks across %d processes in %.3fs" % (args.limit, args.jobs, duration)
    )


if __name__ == "__main__":
    main()
