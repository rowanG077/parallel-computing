import subprocess
import os
import sys
import re
import ctypes
import json

def run(numThreads, matrixSize, iterations, sched):
    prog = "./single" if numThreads == 0 else "./openmp"

    bench_env = os.environ.copy()

    bench_env["OMP_NUM_THREADS"] = str(numThreads)
    bench_env["OMP_SCHEDULE"] = sched

    args = [prog, str(matrixSize), str(iterations)]
    p = subprocess.Popen(args, env=bench_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode()

    relaxTimeRe = r'Time spend relax: (.*) seconds'
    totalTimeRe = r'Time spend total: (.*) seconds'
    gflopsRe = r'Computation: (.*) GFLOP/s'
    
    relaxTime = 0
    totalTime = 0
    gflops = 0

    m = None
    if (m := re.search(relaxTimeRe, out)) == None:
        print(out)
        print(err)
        raise Exception("relax time not found in output")
    
    relaxTime = float(m.group(1))

    if (m := re.search(totalTimeRe, out)) == None:
        print(out)
        print(err)
        raise Exception("Time spend total not found in output")
    
    totalTime = float(m.group(1))

    if (m := re.search(gflopsRe, out)) == None:
        print(out)
        print(err)
        raise Exception("Gflop not found in output")
    
    gflops = float(m.group(1))
    
    return relaxTime, totalTime, gflops

if __name__ == "__main__":
    SCHEDULERS = ["dynamic", "guided", "static"]

    INIT_THREADS = 0
    MAX_THREADS = 8
    STEP_THREAD = 2
    ITERATIONS = 50

    MATRIX_SIZES = [800, 3200, 6400, 12800, 25600]

    REPEAT = 3

    dataPoints = []

    for numThreads in range(INIT_THREADS, MAX_THREADS + 1, STEP_THREAD):
        for matrixSize in MATRIX_SIZES:
            scheds = ["N/A"] if numThreads == 0 else SCHEDULERS
            for sched in scheds:
                dataPoint = {
                    "relaxTime": [],
                    "totalTime": [],
                    "gflop/s": [],
                    "matrixSize": matrixSize,
                    "iterations": ITERATIONS,
                    "numCores": numThreads,
                    "sched": sched,
                    "size": (float(matrixSize)**2 * ctypes.sizeof(ctypes.c_double)) / (1024**2)
                }

                for i in range(REPEAT):
                    print(f"sched: {sched}, {i}/{REPEAT}, threads: {numThreads}/{MAX_THREADS}, matrixSize: {matrixSize}, iterations: {ITERATIONS}")

                    relaxTime, totalTime, gflops = run(numThreads, matrixSize, ITERATIONS, sched)

                    dataPoint["relaxTime"].append(relaxTime)
                    dataPoint["totalTime"].append(totalTime)
                    dataPoint["gflop/s"].append(gflops)

                dataPoints.append(dataPoint)

                with open("Results.json", "w") as file:
                    json.dump(dataPoints, file)