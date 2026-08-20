# import matplotlib.pyplot as plt

def printStats(depths):

    # After the loop
    n = len(depths)
    minD = min(depths)
    maxD = max(depths)
    mean = sum(depths) / n
    variance = sum((d - mean) ** 2 for d in depths) / (n - 1)  # sample stddev
    stddev = variance ** 0.5


    print(f"{float(minD):.0f}, {float(maxD):.0f}, {float(mean):.0f}, {float(stddev):.0f}")

    # plt.hist(depths, bins=100, edgecolor='black')
    # plt.xlabel('Count')
    # plt.ylabel('Frequency')
    # plt.title('Histogram of Counts')
    # plt.grid(True)
    # plt.show()

    # print(f"Min: {float(minD):.3f}")
    # print(f"Max: {float(maxD):.3f}")
    # print(f"Average: {float(mean):.3f}")
    # print(f"Standard deviation: {float(stddev):.3f}")

def getStatsString(values):
    n = len(values)

    minD = min(values)
    maxD = max(values)
    mean = sum(values) / n
    variance = sum((d - mean) ** 2 for d in values) / (n - 1)
    stddev = variance ** 0.5

    return f"{minD:.0f}, {maxD:.0f}, {mean:.0f}, {stddev:.0f}"

def getAverage(values):
    return f"{sum(values) / len(values):.0f}"

def printTableRow(depthsYL, depthsYT, depthsSoS,
                  operationsYL, operationsYT, operationsSoS):

    print(
        f"{getStatsString(depthsYL)} & "
        f"{getStatsString(depthsYT)} & "
        f"{getStatsString(depthsSoS)} & "
        f"{getStatsString(operationsYL)} & "
        f"{getStatsString(operationsYT)} & "
        f"{getStatsString(operationsSoS)} \\\\"
    )


def printFigCase(depthsYL, depthsYT, depthsSoS,
                  operationsYL, operationsYT, operationsSoS):

    print(
        f"{getAverage(depthsYL)}, "
        f"{getAverage(depthsYT)}, "
        f"{getAverage(depthsSoS)}\n"
        f"{getAverage(operationsYL)}, "
        f"{getAverage(operationsYT)}, "
        f"{getAverage(operationsSoS)}"
    )
