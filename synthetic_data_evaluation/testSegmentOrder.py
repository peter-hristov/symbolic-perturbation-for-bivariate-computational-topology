import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

from sympy import symbols, count_ops

# Local imports
from . import geometry, stats
from table_generation import schemes, io, evaluation

def evaluate_iteration(iteration):
    # print(f"---------------------------------------------------------- At iteration {iteration}")
    # start = time.time()

    pl_r, pi_r, pv_r, pj_r, pu_r, pk_r = geometry.generateSegmentsNewCase18((1, 10000))

    signYapL, depthYapL = evaluation.evaluateTable(pExpressionsYapLex, pl, pi, pv, pj, pu, pk, pl_r, pi_r, pv_r, pj_r, pu_r, pk_r)
    signYapT, depthYapT = evaluation.evaluateTable(pExpressionsYapTotal, pl, pi, pv, pj, pu, pk, pl_r, pi_r, pv_r, pj_r, pu_r, pk_r)
    signSoS, depthSoS = evaluation.evaluateTable(pExpressionsSoS, pl, pi, pv, pj, pu, pk, pl_r, pi_r, pv_r, pj_r, pu_r, pk_r)

    # end = time.time()
    # print(f"Time for expression sign evaluation : {end - start:.6f} seconds")

    return {
        "signYapL": signYapL,
        "depthYapL": depthYapL,
        "signYapT": signYapT,
        "depthYapT": depthYapT,
        "signSoS": signSoS,
        "depthSoS": depthSoS
    }

if len(sys.argv) != 2:
    print("Usage: python your_script.py <num_iterations>")
    sys.exit(1)

try:
    n = int(sys.argv[1])
except ValueError:
    print("Invalid input: must be an integer")
    sys.exit(1)


# Set up symbols for the evaluation tables
pl = symbols("pl1, pl2")
pi = symbols("pi1, pi2")
pv = symbols("pv1, pv2")
pj = symbols("pj1, pj2")
pu = symbols("pu1, pu2")
pk = symbols("pk1, pk2")

# Compute the evaluation tables for each scheme
# print("Computing tables for Yap Lex...")
# pExpressionsYapLex, eExpressionsYapLex = schemes.getEvaluationTableSegmentOrderYap(pl, pi, pv, pj, pu, pk, "lex")

# print("Computing tables for Yap Total...")
# pExpressionsYapTotal, eExpressionsYapTotal = schemes.getEvaluationTableSegmentOrderYap(pl, pi, pv, pj, pu, pk, "total")

# print("Computing tables for SoS...")
# pExpressionsSoS, eExpressionsSoS = schemes.getEvaluationTableSegmentOrderSoS(pl, pi, pv, pj, pu, pk)

pExpressionsYapLex, eExpressionsYapLex = io.load_or_compute(
    "segment_order_yap_lex",
    lambda: schemes.getEvaluationTableSegmentOrderYap(
        pl, pi, pv, pj, pu, pk, "lex"
    ),
)

pExpressionsYapTotal, eExpressionsYapTotal = io.load_or_compute(
    "segment_order_yap_total",
    lambda: schemes.getEvaluationTableSegmentOrderYap(
        pl, pi, pv, pj, pu, pk, "total"
    ),
)

pExpressionsSoS, eExpressionsSoS = io.load_or_compute(
    "segment_order_sos",
    lambda: schemes.getEvaluationTableSegmentOrderSoS(
        pl, pi, pv, pj, pu, pk
    ),
)

# Compute number of arithemtic operations for each row of the evaluation table for each scheme
operationCountYapLex = [count_ops(p) for p in pExpressionsYapLex]
operationCountYapTotal = [count_ops(p) for p in pExpressionsYapTotal]
operationCountSoS = [count_ops(p) for p in pExpressionsSoS]

# Set up arrays to hold the results for each test
signsYapL = []
depthsYapL = []
operationsYapL = []
depthsHistogramYapL = defaultdict(int)

signsYapT = []
depthsYapT = []
operationsYapT = []
depthsHistogramYapT = defaultdict(int)

signsSoS = []
depthsSoS = []
operationsSoS = []
depthsHistogramSoS = defaultdict(int)


start = time.time()

# Run all tests in paralle
with ProcessPoolExecutor() as executor:
    results = list(executor.map(evaluate_iteration, range(n)))

for r in results:
    signsYapL.append(r["signYapL"])
    depthsYapL.append(r["depthYapL"])
    operationsYapL.append(sum(operationCountYapLex[:r["depthYapL"]+1]))
    depthsHistogramYapL[r["depthYapL"]] += 1

    signsYapT.append(r["signYapT"])
    depthsYapT.append(r["depthYapT"])
    operationsYapT.append(sum(operationCountYapTotal[:r["depthYapT"]+1]))
    depthsHistogramYapT[r["depthYapT"]] += 1

    signsSoS.append(r["signSoS"])
    depthsSoS.append(r["depthSoS"])
    operationsSoS.append(sum(operationCountSoS[:r["depthSoS"]+1]))
    depthsHistogramSoS[r["depthSoS"]] += 1

end = time.time()
print(f"Time for expression sign evaluation : {end - start:.6f} seconds")

# Output stats over all tests
print("\n\n------------------------------------------------------------------- Yap Lex")
print("Here are the depth stats for Yap Lex")
stats.printStats(depthsYapL)
print("\nHere are the operations stats for Yap Lex")
stats.printStats(operationsYapL)
print(f"\nHere's the histogram:")
for key, value in depthsHistogramYapL.items():
    print(f"Depth: {key}, count: {value}")

print("\n\n------------------------------------------------------------------- Yap Total")
print("Here are the depth stats for Yap Total")
stats.printStats(depthsYapT)
print("\nHere are the operations stats for Yap Total")
stats.printStats(operationsYapT)
print(f"\nHere's the histogram:")
for key, value in depthsHistogramYapT.items():
    print(f"Depth: {key}, count: {value}")

print("\n\n------------------------------------------------------------------- Sos")
print("Here are the depth stats for SoS")
stats.printStats(depthsSoS)
print("\nHere are the operations stats for SoS")
stats.printStats(operationsSoS)
print(f"\nHere's the histogram:")
for key, value in depthsHistogramSoS.items():
    print(f"Depth: {key}, count: {value}")



print("\n\n")
stats.printTableRow(depthsYapL, depthsYapT, depthsSoS, operationsYapL, operationsYapT, operationsSoS)
print("\n")
stats.printFigCase(depthsYapL, depthsYapT, depthsSoS, operationsYapL, operationsYapT, operationsSoS)
