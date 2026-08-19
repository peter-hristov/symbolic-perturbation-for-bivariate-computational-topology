import sys
import os
import vtk
from itertools import combinations
from tqdm import tqdm
from collections import defaultdict

from sympy import symbols, sign, count_ops, Rational

# Local imports
from synthetic_data_evaluation import stats 
from table_generation import schemes, io, evaluation

def evaluate_iteration(pl, pi, pv, pj, pu, pk, pl_f, pi_f, pv_f, pj_f, pu_f, pk_f, pExpressionsYapLex, pExpressionsYapTotal, pExpressionsSoS):

    pl_r = tuple(Rational(str(x)) for x in pl_f)
    pi_r = tuple(Rational(str(x)) for x in pi_f)
    pv_r = tuple(Rational(str(x)) for x in pv_f)
    pj_r = tuple(Rational(str(x)) for x in pj_f)
    pu_r = tuple(Rational(str(x)) for x in pu_f)
    pk_r = tuple(Rational(str(x)) for x in pk_f)

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

def read_vtk(filename):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()

    mesh = reader.GetOutput()

    point_data = mesh.GetPointData()

    f1 = point_data.GetArray(0)
    f2 = point_data.GetArray(1)

    if f1 is None or f2 is None:
        raise RuntimeError("Mesh must contain at least two point-data arrays.")

    # Map vertices to R^2
    points = []

    for i in range(mesh.GetNumberOfPoints()):
        points.append((f1.GetTuple1(i), f2.GetTuple1(i)))

    tet_edges = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    # Unique mesh edges
    edges = set()

    for cell_id in range(mesh.GetNumberOfCells()):
        cell = mesh.GetCell(cell_id)

        if cell.GetCellType() != vtk.VTK_TETRA:
            continue

        ids = [cell.GetPointId(i) for i in range(4)]

        for a, b in tet_edges:
            edges.add(tuple(sorted((ids[a], ids[b]))))

    # Convert edge vertex IDs to segments in R^2
    segments = [
        (points[u], points[v])
        for u, v in edges
    ]

    return points, segments


def generate_point_triples(points):
    return list(combinations(points, 3))


def generate_segment_triples(segments):
    return list(combinations(segments, 3))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.vtk>")
        sys.exit(1)

    points, segments = read_vtk(sys.argv[1])

    point_triples = generate_point_triples(points)
    segment_triples = generate_segment_triples(segments)

    print(f"Number of tripples of points : {len(point_triples)}")
    print(f"Number of tripples of segments : {len(segment_triples)}")


    # Set up symbols for the evaluation tables
    pl = symbols("pl1, pl2")
    pi = symbols("pi1, pi2")
    pv = symbols("pv1, pv2")
    pj = symbols("pj1, pj2")
    pu = symbols("pu1, pu2")
    pk = symbols("pk1, pk2")

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

    results = []

    for (pl_f, pi_f), (pv_f, pj_f), (pu_f, pk_f) in tqdm(
        segment_triples,
        desc="Evaluating segment triples"
    ):

        r = evaluate_iteration(pl, pi, pv, pj, pu, pk, pl_f, pi_f, pv_f, pj_f, pu_f, pk_f, pExpressionsYapLex, pExpressionsYapTotal, pExpressionsSoS)
        results.append(r)

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














    # print("\nPoint triples:")
    # for triple in point_triples:
        # print(triple)

    # print("\nSegment triples:")
    # for triple in segment_triples:
        # print(triple)

if __name__ == "__main__":
    main()
