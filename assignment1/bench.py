import subprocess
import os
import sys
import re
import ctypes

def run(numThreads, matrixSize, iterations):
    prog = "./single" if numThreads == 0 else "./openmp"

    bench_env = os.environ.copy()

    bench_env["OMP_NUM_THREADS"] = str(numThreads)

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
        raise Exception("relax time not found in output")
    
    relaxTime = float(m.group(1))

    if (m := re.search(totalTimeRe, out)) == None:
        raise Exception("Time spend total not found in output")
    
    totalTime = float(m.group(1))

    if (m := re.search(gflopsRe, out)) == None:
        raise Exception("Gflop not found in output")
    
    gflops = float(m.group(1))
    
    return relaxTime, totalTime, gflops

if __name__ == "__main__":
    INIT_THREADS = 0
    MAX_THREADS = 4
    STEP_THREAD = 1

    INIT_MATRIX = 100
    MAX_MATRIX = 1000
    STEP_MATRIX = 100

    INIT_ITERATIONS = 500
    MAX_ITERATIONS = 1500
    STEP_ITERATIONS = 500

    REPEAT = 5

    dataPoints = []

    for numThreads in range(INIT_THREADS, MAX_THREADS + 1, STEP_THREAD):
        for matrixSize in range(INIT_MATRIX, MAX_MATRIX + 1, STEP_MATRIX):
            for iterations in range(INIT_ITERATIONS, MAX_ITERATIONS + 1, STEP_ITERATIONS):
                dataPoint = {
                    "relaxTime": [],
                    "totalTime": [],
                    "gflop/s": [],
                    "matrixSize": matrixSize,
                    "iterations": iterations,
                    "numCores": numThreads,
                    "size": (float(matrixSize)**2 * ctypes.sizeof(ctypes.c_double)) / (1024**2)
                }

                for i in range(REPEAT):
                    print(f"{i}/{REPEAT}, threads: {numThreads}/{MAX_THREADS}, matrixSize: {matrixSize}/{MAX_MATRIX}, iterations: {iterations}/{MAX_ITERATIONS}")

                    relaxTime, totalTime, gflops = run(numThreads, matrixSize, iterations)

                    dataPoint["relaxTime"].append(relaxTime)
                    dataPoint["totalTime"].append(totalTime)
                    dataPoint["gflop/s"].append(gflops)

                dataPoints.append(dataPoint)

    # generate graphs
    # generateGraphs(dataPoints)