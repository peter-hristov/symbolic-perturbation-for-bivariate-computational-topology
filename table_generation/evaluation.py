from sympy import sign

def evaluateTable(pExpressions, pl, pi, pv, pj, pu, pk, pl_r, pi_r, pv_r, pj_r, pu_r, pk_r):

    subs_dict = {
        pl[0]: pl_r[0], pl[1]: pl_r[1],
        pi[0]: pi_r[0], pi[1]: pi_r[1],
        pv[0]: pv_r[0], pv[1]: pv_r[1],
        pj[0]: pj_r[0], pj[1]: pj_r[1],
        pu[0]: pu_r[0], pu[1]: pu_r[1],
        pk[0]: pk_r[0], pk[1]: pk_r[1],
    }

    for i, pExpression in enumerate(pExpressions):
        expressionSign = sign(pExpression.subs(subs_dict).evalf())

        # print(f"The expression is {pExpression.subs(subs_dict).evalf()}")
        # print(sign)
        # print(type(sign))
        # print(expressionSign)

        expr = pExpression.subs(subs_dict)
        expr_eval = expr.evalf()

        if (expressionSign != 0):
            return expressionSign, i

    raise ValueError("Table could not be evaluated") 
