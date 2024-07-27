import os
import re
from datetime import datetime
from collections import defaultdict
import pandas as pd

BENCHMARKS = [
    "600.perlbench_s",
    "602.gcc_s",
    "605.mcf_s",
    "620.omnetpp_s",
    "623.xalancbmk_s",
    "625.x264_s",
    "631.deepsjeng_s",
    "641.leela_s",
    "648.exchange2_s",
    "657.xz_s",
]


def read_files_in_directory(directory):
    file_contents = {}
    for subdir, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            with open(file_path, "r") as f:
                file_contents[file_path] = f.read()
    return file_contents


def parse_benchmark_data(contents, pattern, cpu_pattern):
    results = {
        benchmark: {
            "returnvalue": None,
            "walltime": 0,
            "cputime": 0,
            "memory": 0,
            "blkio-read": 0,
            "blkio_write": 0,
        }
        for benchmark in BENCHMARKS
    }
    iter = 1
    for data in contents.values():
        for match in pattern.finditer(data):
            benchmark = match.group("benchmark")
            walltime = float(match.group("walltime"))
            cputime = float(match.group("cputime"))
            memory = int(match.group("memory"))
            blkio_read = int(match.group("blkio_read"))
            blkio_write = int(match.group("blkio_write"))

            results[benchmark]["walltime"] = (
                results[benchmark]["walltime"] + walltime
            ) / iter
            results[benchmark]["cputime"] = (
                results[benchmark]["cputime"] + cputime
            ) / iter
            results[benchmark]["memory"] = (
                results[benchmark]["memory"] + memory
            ) / iter
            results[benchmark]["blkio-read"] = (
                results[benchmark]["blkio-read"] + blkio_read
            ) / iter
            results[benchmark]["blkio_write"] = (
                results[benchmark]["blkio_write"] + blkio_write
            ) / iter
        iter += 1
    return results


if "__main__" == __name__:
    pattern = re.compile(
        r"(?P<benchmark>[\d\.a-z_]+)\n"
        r"starttime=(?P<starttime>[^\n]+)\n"
        r"returnvalue=(?P<returnvalue>\d+)\n"
        r"walltime=(?P<walltime>[\d\.]+)s\n"
        r"cputime=(?P<cputime>[\d\.]+)s\n"
        r"(?P<cpu_times>(?:cputime-cpu\d+=\d+\.\d+s\n)+)"
        r"memory=(?P<memory>\d+)B\n"
        r"blkio-read=(?P<blkio_read>\d+)B\n"
        r"blkio-write=(?P<blkio_write>\d+)B\n"
    )

    cpu_pattern = re.compile(r"cputime-cpu(?P<cpu>\d+)=(?P<time>[\d\.]+)s")

    base_contents = read_files_in_directory("./base")
    base_results = parse_benchmark_data(base_contents, pattern, cpu_pattern)

    fuse_contents = read_files_in_directory("./fuse")
    fuse_results = parse_benchmark_data(fuse_contents, pattern, cpu_pattern)

    # Convert results to DataFrame
    base_df = pd.DataFrame.from_dict(base_results, orient="index")
    fuse_df = pd.DataFrame.from_dict(fuse_results, orient="index")

    # Save DataFrames to CSV
    base_df.to_csv("base_results.csv")
    fuse_df.to_csv("fuse_results.csv")
