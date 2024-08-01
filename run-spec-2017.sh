#!/bin/bash

SPEC2017=/home/haoranyang/SPEC2017
BENCHMARKS=("600.perlbench_s" "602.gcc_s" "620.omnetpp_s" "623.xalancbmk_s" "631.deepsjeng_s" "641.leela_s" "648.exchange2_s" "998.specrand_is")
RESULT_DIR=/home/haoranyang/benchexec-eval/benchexec-results

cd $SPEC2017

source ../benchexec-venv/bin/activate
source shrc

for i in {0..4}; do
    for BENCHMARK in "${BENCHMARKS[@]}"; do
        echo ${BENCHMARK} >> ${RESULT_DIR}/base/iter_${i}
        sudo /home/haoranyang/benchexec-eval/clean_cache.sh
        runexec --overlay-dir /home --read-only-dir / --full-access-dir /home/haoranyang/SPEC2017/result -- runcpu --config /home/haoranyang/SPEC2017/config/benchexec-gcc-linux-x86.cfg --flags /home/haoranyang/SPEC2017/config/flags/benchexec.xml --size ref --tune base --iterations 1 $BENCHMARK >>${RESULT_DIR}/base/iter_${i}
    done
done

cp /home/haoranyang/container.py /home/haoranyang/benchexec/benchexec/container.py

cd /home/haoranyang/benchexec/

pip install -e .

cd $SPEC2017

sleep 10

for i in {0..4}; do
    for BENCHMARK in "${BENCHMARKS[@]}"; do
        echo $BENCHMARK >> ${RESULT_DIR}/fuse/iter_${i}
        sudo /home/haoranyang/benchexec-eval/clean_cache.sh
        runexec --overlay-dir /home --read-only-dir / --full-access-dir /home/haoranyang/SPEC2017/result -- runcpu --config /home/haoranyang/SPEC2017/config/benchexec-gcc-linux-x86.cfg --flags /home/haoranyang/SPEC2017/config/flags/benchexec.xml --size ref --tune base --iterations 1 $BENCHMARK >>${RESULT_DIR}/fuse/iter_${i}
    done
done
