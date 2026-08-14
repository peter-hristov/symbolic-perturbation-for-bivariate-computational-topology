import random
from sympy import symbols, Rational, simplify

def generateRandomRationalCirclePoint(randomRange):
    # Define symbols
    x_sym, y_sym, t = symbols("x y t")

    # Parametrize x and y
    x_expr = (1 - t**2) / (1 + t**2)
    y_expr = (2 * t) / (1 + t**2)

    a = random.randint(randomRange[0], randomRange[1])
    b = random.randint(randomRange[0], randomRange[1])

    # Define a rational value of t
    t_val = Rational(a, b)  # This is t = 3/4

    # Evaluate x and y at t = 3/4
    x_val = simplify(x_expr.subs(t, t_val))
    y_val = simplify(y_expr.subs(t, t_val))

    # Print results
    assert x_val**2 + y_val**2 == 1

    return [x_val, y_val]


# Make sure we generate a valid rational (not division by zero)
def safe_rand_scale(randomRange):
    while True:
        num = random.randint(*randomRange)
        denom = random.randint(*randomRange)
        if denom != 0:
            return Rational(num, denom)

# Scale and offset each point
def transform_point(p, offsetX, offsetY, randomRange):
    scale = safe_rand_scale(randomRange)
    return [p[0]*scale + offsetX, p[1]*scale + offsetY]
    # return [p[0]*scale, p[1]*scale]
    # return [p[0], p[1]]

def generateSegments(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    pv = generateRandomRationalCirclePoint(randomRange)
    pj = [-pv[0], -pv[1]]

    pu = generateRandomRationalCirclePoint(randomRange)
    pk = [-pu[0], -pu[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)
    pv = transform_point(pv, centerOffsetX, centerOffsetY, randomRange)
    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)
    pu = transform_point(pu, centerOffsetX, centerOffsetY, randomRange)
    pk = transform_point(pk, centerOffsetX, centerOffsetY, randomRange)

    return pl, pi, pv, pj, pu, pk

def generateColinearPoints(randomRange):
    # Generate original points as lists
    pi = generateRandomRationalCirclePoint(randomRange)
    pj = [0, 0]
    pk = [-pi[0], -pi[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)
    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)
    pk = transform_point(pk, centerOffsetX, centerOffsetY, randomRange)

    return pi, pj, pk

def evaluateExpression(expression, p, variables, indexSubstitution, p1, p2, p3, p4, p5, p6):
    i, j, k, l, u, v = variables

    expression_index_subs = expression.subs(indexSubstitution)

    valueSubs = {
            p[indexSubstitution[i], 1]: p1[0], p[indexSubstitution[i], 2]: p1[1],
            p[indexSubstitution[j], 1]: p2[0], p[indexSubstitution[j], 2]: p2[1],
            p[indexSubstitution[k], 1]: p3[0], p[indexSubstitution[k], 2]: p3[1],
            p[indexSubstitution[l], 1]: p4[0], p[indexSubstitution[l], 2]: p4[1],
            p[indexSubstitution[u], 1]: p5[0], p[indexSubstitution[u], 2]: p5[1],
            p[indexSubstitution[v], 1]: p6[0], p[indexSubstitution[v], 2]: p6[1],
            }

    expression_value_subs = expression_index_subs.subs(valueSubs)

    return expression_value_subs


# Generic Case 1.
# Three segments with generic intersections

def generateSegmentsNewCase1(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0] + Rational(0.00001), -pl[1]]


    while (pv := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass
    pj = [-pv[0], -pv[1]]

    while (pu := generateRandomRationalCirclePoint(randomRange)) in (pl, pi, pv, pj):
        pass
    pk = [-pu[0], -pu[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)
    pv = transform_point(pv, centerOffsetX, centerOffsetY, randomRange)
    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)
    pu = transform_point(pu, centerOffsetX, centerOffsetY, randomRange)
    pk = transform_point(pk, centerOffsetX, centerOffsetY, randomRange)

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # print(type(pv[0]))
    # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # print(type(pu[0]))
    # print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    # print("\n\n")

    return pl, pi, pv, pj, pu, pk


# Degenerate Case 2.
# Three segments intersecting in an point in their interiors

def generateSegmentsNewCase2(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pv := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass
    pj = [-pv[0], -pv[1]]

    while (pu := generateRandomRationalCirclePoint(randomRange)) in (pl, pi, pv, pj):
        pass
    pk = [-pu[0], -pu[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)
    pv = transform_point(pv, centerOffsetX, centerOffsetY, randomRange)
    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)
    pu = transform_point(pu, centerOffsetX, centerOffsetY, randomRange)
    pk = transform_point(pk, centerOffsetX, centerOffsetY, randomRange)

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # print(type(pv[0]))
    # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # print(type(pu[0]))
    # print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    # print("\n\n")

    return pl, pi, pv, pj, pu, pk


# Case 3
# 2 overlapping segments, 1 free segment
#
def generateSegmentsNewCase3(randomRange):

    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pu := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass
    pk = [-pu[0], -pu[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    pu = transform_point(pu, centerOffsetX, centerOffsetY, randomRange)
    pk = transform_point(pk, centerOffsetX, centerOffsetY, randomRange)

    print("What are the types we need?2")
    print(type(pl[0]))
    print(type(pl[1]))
    print(type(pi[0]))
    print(type(pi[1]))
    # print(type(pv[0]))
    # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    print(type(pu[0]))
    print(type(pu[1]))
    print(type(pk[0]))
    print(type(pk[1]))
    print("\n\n")



    return pl, pi, pl, pi, pu, pk



# Three overlapping
#

def generateSegmentsNewCase4(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)
    print("What are the types we need?2")
    print(type(pl[0]))
    print(type(pl[1]))
    print(type(pi[0]))
    print(type(pi[1]))
    # print(type(pv[0]))
    # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # print(type(pu[0]))
    # print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    print("\n\n")



    return pl, pi, pl, pi, pl, pi



# two crossing, one point non-overlapping
#
def generateSegmentsNewCase5(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pv := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass
    pj = [-pv[0], -pv[1]]


    while (pu := generateRandomRationalCirclePoint(randomRange)) in (pl, pi, pv, pj):
        pass

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    pv = transform_point(pv, centerOffsetX, centerOffsetY, randomRange)
    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)

    pu = transform_point(pu, centerOffsetX, centerOffsetY, randomRange)

    print("What are the types we need?2")
    print(type(pl[0]))
    print(type(pl[1]))
    print(type(pi[0]))
    print(type(pi[1]))
    print(type(pv[0]))
    print(type(pv[1]))
    print(type(pj[0]))
    print(type(pj[1]))
    print(type(pu[0]))
    print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    print("\n\n")

    return pl, pi, pv, pj, pu, pu


# two crossing, one point overlapping one segment
#

def generateSegmentsNewCase6(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pv := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass

    pj = [-pv[0], -pv[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)
    pv = transform_point(pv, centerOffsetX, centerOffsetY, randomRange)
    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)


    t1 = Rational(random.uniform(0.01, 0.49))

    pu = [
        (1 - t1) * pl[0] + t1 * pi[0],
        (1 - t1) * pl[1] + t1 * pi[1],
    ]

    return pl, pi, pv, pj, pu, pu



# two crossing, one point at the point of intersection
#

def generateSegmentsNewCase7(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pv := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass

    pj = [-pv[0], -pv[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)
    pv = transform_point(pv, centerOffsetX, centerOffsetY, randomRange)
    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)

    pu = [centerOffsetX, centerOffsetY]

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # print(type(pv[0]))
    # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # print(type(pu[0]))
    # print(type(pu[1]))
    # # print(type(pk[0]))
    # # print(type(pk[1]))
    # print("\n\n")


    return pl, pi, pv, pj, pu, pu


# Two overlapping segments, one point
#

def generateSegmentsNewCase8(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pv := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    centerOffsetX2 = safe_rand_scale(randomRange)
    centerOffsetY2 = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    pv = transform_point(pv, centerOffsetX, centerOffsetY, randomRange)


    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # print(type(pv[0]))
    # print(type(pv[1]))
    # # print(type(pj[0]))
    # # print(type(pj[1]))
    # # print(type(pu[0]))
    # # print(type(pu[1]))
    # # print(type(pk[0]))
    # # print(type(pk[1]))
    # print("\n\n")

    return pl, pi, pl, pi, pv, pv



# two overlapping segments, one point overlapping them
#

def generateSegmentsNewCase9(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)


    t1 = Rational(random.uniform(0.1, 0.4))

    pu = [
        (1 - t1) * pl[0] + t1 * pi[0],
        (1 - t1) * pl[1] + t1 * pi[1],
    ]

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # # print(type(pv[0]))
    # # print(type(pv[1]))
    # # print(type(pj[0]))
    # # print(type(pj[1]))
    # print(type(pu[0]))
    # print(type(pu[1]))
    # # print(type(pk[0]))
    # # print(type(pk[1]))
    # print("\n\n")

    return pl, pi, pl, pi, pu, pu


# One segment, two free points
#

def generateSegmentsNewCase10(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pj := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass

    while (pk := generateRandomRationalCirclePoint(randomRange)) in (pl, pi, pj):
        pass

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # centerOffsetX2 = safe_rand_scale(randomRange)
    # centerOffsetY2 = safe_rand_scale(randomRange)

    # centerOffsetX3 = safe_rand_scale(randomRange)
    # centerOffsetY3 = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)
    pk = transform_point(pk, centerOffsetX, centerOffsetY, randomRange)

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # # print(type(pv[0]))
    # # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # # print(type(pu[0]))
    # # print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    # print("\n\n")



    return pl, pi, pj, pj, pk, pk




# One segment, one point overlapping the segment, one free point
#

def generateSegmentsNewCase11(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pj := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass


    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # centerOffsetX2 = safe_rand_scale(randomRange)
    # centerOffsetY2 = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)

    t1 = Rational(random.uniform(0.01, 0.49))
    pk = [
        (1 - t1) * pl[0] + t1 * pi[0],
        (1 - t1) * pl[1] + t1 * pi[1],
    ]

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # # print(type(pv[0]))
    # # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # # print(type(pu[0]))
    # # print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    # print("\n\n")


    return pl, pi, pj, pj, pk, pk



# One segment, two distinct points overlapping the segment
#
def generateSegmentsNewCase12(randomRange):
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    t1 = Rational(random.uniform(0.1, 0.9))
    pj = [
        (1 - t1) * pl[0] + t1 * pi[0],
        (1 - t1) * pl[1] + t1 * pi[1],
    ]

    while (t2 := Rational(random.uniform(0.1, 0.9))) == t1:
        pass

    pk = [
        (1 - t2) * pl[0] + t2 * pi[0],
        (1 - t2) * pl[1] + t2 * pi[1],
    ]

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # # print(type(pv[0]))
    # # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # # print(type(pu[0]))
    # # print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    # print("\n\n")

    return pl, pi, pj, pj, pk, pk



# One segment, two overlapping points free
#
def generateSegmentsNewCase13(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    while (pj := generateRandomRationalCirclePoint(randomRange)) in (pl, pi):
        pass

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # centerOffsetX2 = safe_rand_scale(randomRange)
    # centerOffsetY2 = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    pj = transform_point(pj, centerOffsetX, centerOffsetY, randomRange)

    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # # print(type(pv[0]))
    # # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # # print(type(pu[0]))
    # # print(type(pu[1]))
    # # print(type(pk[0]))
    # # print(type(pk[1]))
    # print("\n\n")

    return pl, pi, pj, pj, pj, pj


# One segment, two overlapping points, overlapping segment
#
def generateSegmentsNewCase14(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    # t1 = Rational(random.uniform(0.1, 0.9))
    # pj = [
        # (1 - t1) * pl[0] + t1 * pi[0],
        # (1 - t1) * pl[1] + t1 * pi[1],
    # ]

    pj = pl


    # print("What are the types we need?2")
    # print(type(pl[0]))
    # print(type(pl[1]))
    # print(type(pi[0]))
    # print(type(pi[1]))
    # # print(type(pv[0]))
    # # print(type(pv[1]))
    # print(type(pj[0]))
    # print(type(pj[1]))
    # # print(type(pu[0]))
    # # print(type(pu[1]))
    # # print(type(pk[0]))
    # # print(type(pk[1]))
    # print("\n\n")

    return pl, pi, pj, pj, pj, pj


#
# Three points, general position
#

def generateSegmentsNewCase15(randomRange):
    while True:
        # Generate original points
        pl = generateRandomRationalCirclePoint(randomRange)
        pi = generateRandomRationalCirclePoint(randomRange)
        pj = generateRandomRationalCirclePoint(randomRange)

        # Offset centers
        centerOffsetX = safe_rand_scale(randomRange)
        centerOffsetY = safe_rand_scale(randomRange)

        centerOffsetX2 = safe_rand_scale(randomRange)
        centerOffsetY2 = safe_rand_scale(randomRange)

        centerOffsetX3 = safe_rand_scale(randomRange)
        centerOffsetY3 = safe_rand_scale(randomRange)

        # Transform points
        pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
        pi = transform_point(pi, centerOffsetX2, centerOffsetY2, randomRange)
        pj = transform_point(pj, centerOffsetX3, centerOffsetY3, randomRange)

        # Pairwise distinct and non-collinear
        if pl == pi or pl == pj or pi == pj:
            continue

        det = (
            (pi[0] - pl[0]) * (pj[1] - pl[1])
            - (pi[1] - pl[1]) * (pj[0] - pl[0])
        )

        if det == 0:
            continue

        break

    print("What are the types we need?2")
    print(type(pl[0]))
    print(type(pl[1]))
    print(type(pi[0]))
    print(type(pi[1]))
    # print(type(pv[0]))
    # print(type(pv[1]))
    print(type(pj[0]))
    print(type(pj[1]))
    # print(type(pu[0]))
    # print(type(pu[1]))
    # print(type(pk[0]))
    # print(type(pk[1]))
    print("\n\n")

    return pl, pl, pi, pi, pj, pj

# Three colinear points
#
def generateSegmentsNewCase16(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)
    pi = [-pl[0], -pl[1]]

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX, centerOffsetY, randomRange)

    t1 = Rational(random.random())

    pj = [
        (1 - t1) * pl[0] + t1 * pi[0],
        (1 - t1) * pl[1] + t1 * pi[1],
    ]

    return pl, pl, pi, pi, pj, pj


#
# two duplicate point, one free
#
def generateSegmentsNewCase17(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)

    while (pi := generateRandomRationalCirclePoint(randomRange)) == pl:
        pass

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    centerOffsetX2 = safe_rand_scale(randomRange)
    centerOffsetY2 = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)
    pi = transform_point(pi, centerOffsetX2, centerOffsetY2, randomRange)

    return pl, pl, pl, pl, pi, pi



# three duplicate
#
def generateSegmentsNewCase18(randomRange):
    # Generate original points as lists
    pl = generateRandomRationalCirclePoint(randomRange)

    # Offset center
    centerOffsetX = safe_rand_scale(randomRange)
    centerOffsetY = safe_rand_scale(randomRange)

    # Transform all points
    pl = transform_point(pl, centerOffsetX, centerOffsetY, randomRange)


    return pl, pl, pl, pl, pl, pl


