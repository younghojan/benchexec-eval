import os
import re
import pandas as pd

BENCHMARKS = [
    "600.perlbench_s",
    "602.gcc_s",
    "620.omnetpp_s",
    "623.xalancbmk_s",
    "631.deepsjeng_s",
    "641.leela_s",
    "648.exchange2_s",
    "998.specrand_is",
]


def read_files_in_directory(directory):
    file_contents = {}
    for subdir, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            with open(file_path, "r") as f:
                file_contents[file_path] = f.read()
    return file_contents


def parse_benchmark_data(contents, pattern):
    results = {
        benchmark: {
            "walltime": 0.0,
            "cputime": 0.0,
            "memory": 0.0,
            "blkio-read": 0.0,
            "blkio_write": 0.0,
            "pressure-cpu-some": 0.0,
            "pressure-io-some": 0.0,
            "pressure-memory-some": 0.0,
        }
        for benchmark in BENCHMARKS
    }
    iter = 1
    for data in contents.values():
        for match in pattern.finditer(data):
            benchmark = match.group("benchmark")
            walltime = float(match.group("walltime"))
            cputime = float(match.group("cputime"))
            memory = float(match.group("memory"))
            blkio_read = float(match.group("blkio_read"))
            blkio_write = float(match.group("blkio_write"))
            pressure_cpu_some = float(match.group("pressure_cpu_some"))
            pressure_io_some = float(match.group("pressure_io_some"))
            pressure_memory_some = float(match.group("pressure_memory_some"))

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
            results[benchmark]["pressure-cpu-some"] = (
                results[benchmark]["pressure-cpu-some"] + pressure_cpu_some
            ) / iter
            results[benchmark]["pressure-io-some"] = (
                results[benchmark]["pressure-io-some"] + pressure_io_some
            ) / iter
            results[benchmark]["pressure-memory-some"] = (
                results[benchmark]["pressure-memory-some"] + pressure_memory_some
            ) / iter
        iter += 1
    return results


def parse_benchmark_data2(contents, pattern):
    results = {
        benchmark: {
            "walltime": [],
            "cputime": [],
            "memory": [],
            "blkio-read": [],
            "blkio_write": [],
            "pressure-cpu-some": [],
            "pressure-io-some": [],
            "pressure-memory-some": [],
        }
        for benchmark in BENCHMARKS
    }
    for data in contents.values():
        for match in pattern.finditer(data):
            benchmark = match.group("benchmark")
            walltime = float(match.group("walltime"))
            cputime = float(match.group("cputime"))
            memory = float(match.group("memory"))
            blkio_read = float(match.group("blkio_read"))
            blkio_write = float(match.group("blkio_write"))
            pressure_cpu_some = float(match.group("pressure_cpu_some"))
            pressure_io_some = float(match.group("pressure_io_some"))
            pressure_memory_some = float(match.group("pressure_memory_some"))

            results[benchmark]["walltime"].append(walltime)
            results[benchmark]["cputime"].append(cputime)
            results[benchmark]["memory"].append(memory)
            results[benchmark]["blkio-read"].append(blkio_read)
            results[benchmark]["blkio_write"].append(blkio_write)
            results[benchmark]["pressure-cpu-some"].append(pressure_cpu_some)
            results[benchmark]["pressure-io-some"].append(pressure_io_some)
            results[benchmark]["pressure-memory-some"].append(pressure_memory_some)
    return results


def convert_to_dataframe(results):
    rows = []
    for benchmark, metrics in results.items():
        for i in range(len(metrics["walltime"])):
            row = {
                "benchmark": benchmark,
                "walltime": metrics["walltime"][i],
                "cputime": metrics["cputime"][i],
                "memory": metrics["memory"][i],
                "blkio-read": metrics["blkio-read"][i],
                "blkio_write": metrics["blkio_write"][i],
                "pressure-cpu-some": metrics["pressure-cpu-some"][i],
                "pressure-io-some": metrics["pressure-io-some"][i],
                "pressure-memory-some": metrics["pressure-memory-some"][i],
            }
            rows.append(row)
    df = pd.DataFrame(rows)
    return df


if "__main__" == __name__:
    pattern = re.compile(
        r"(?P<benchmark>[\d\.a-z_]+)\n"
        r"starttime=(?P<starttime>[^\n]+)\n"
        r"returnvalue=(?P<returnvalue>\d+)\n"
        r"walltime=(?P<walltime>[\d\.]+)s\n"
        r"cputime=(?P<cputime>[\d\.]+)s\n"
        r"memory=(?P<memory>\d+)B\n"
        r"blkio-read=(?P<blkio_read>\d+)B\n"
        r"blkio-write=(?P<blkio_write>\d+)B\n"
        r"pressure-cpu-some=(?P<pressure_cpu_some>[\d\.]+)s\n"
        r"pressure-io-some=(?P<pressure_io_some>[\d\.]+)s\n"
        r"pressure-memory-some=(?P<pressure_memory_some>[\d\.]+)s\n"
    )

    base_contents = read_files_in_directory("./base")
    # base_results = parse_benchmark_data(base_contents, pattern)
    base_results = parse_benchmark_data2(base_contents, pattern)

    fuse_contents = read_files_in_directory("./fuse")
    # fuse_results = parse_benchmark_data(fuse_contents, pattern)
    fuse_results = parse_benchmark_data2(fuse_contents, pattern)

    # base_df = pd.DataFrame.from_dict(base_results, orient="index")
    # fuse_df = pd.DataFrame.from_dict(fuse_results, orient="index")

    # base_df.to_csv("base_results.csv")
    # fuse_df.to_csv("fuse_results.csv")

    # Convert results to DataFrame
    base_df = convert_to_dataframe(base_results)
    fuse_df = convert_to_dataframe(fuse_results)

    # Save DataFrames to CSV
    base_df.to_csv("base_results.csv", index=False)
    fuse_df.to_csv("fuse_results.csv", index=False)
