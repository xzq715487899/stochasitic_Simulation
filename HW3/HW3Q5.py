import random as rd
import math
from scipy.optimize import fsolve


def sim_exp_hyper(pmf:list, expects:list, n:int, whi_seed:int=123) -> list:

    if len(pmf) != len(expects):
        raise ValueError("len(pmf) != len(expects).")
    elif sum([i < 0 for i in pmf]) > 0:
        raise ValueError(f"There are negative values in the probablity mass "
            f"function {pmf}.")

    def get_eq(u, x):
        eq = 1 - sum(pmf[i] * math.exp(- x / expects[i]) for i in range(len(pmf))) - u
        return eq

    rd.seed(whi_seed)
    us = [rd.random() for i in range(n)]
    xs = [fsolve(lambda x: get_eq(u, x), 0.1)[0] for u in us]
    return xs, us
a = [1,2,3,4]
sim_exp_hyper(a,a,1,1)