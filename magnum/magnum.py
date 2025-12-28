#! env python

"""
Magnum Popsiscle Calculator
"""

import math

classic = 41.5
almond = 44.3
white = 41.3

weights = [classic, almond, white]

pkg_weight = 336.8
nb_pops = 8

# Variant 1: we brute force over all triplets, knowing that some
# are not valid.

c = 0
for i in range(1, nb_pops - 1):
    for j in range(1, nb_pops - 1):
        for k in range(1, nb_pops - 1):
            c += 1
            counts = [i, j, k]
            # Max number of popsicles must match.
            if sum(counts) == nb_pops:
                computed_weights = sum(x * y for x, y in zip(counts, weights))
                res = ""
                if math.isclose(computed_weights, pkg_weight):
                    res = " --! bingo !--"

                print(
                    f"classic, almond, white = {i} {j} {k} {computed_weights:5.1f}"
                    f" {computed_weights-pkg_weight:5.2f} {res}"
                )
print(f"total = {c}")

# Variant 2: we compute only valid triplets by changing
# the limits of the second range and computing the third quantity
# to match the total. We only need to check the weight.

c = 0
for i in range(1, nb_pops - 1):
    for j in range(1, nb_pops - i):
        c += 1
        counts = [i, j, nb_pops - i - j]
        computed_weights = sum(x * y for x, y in zip(counts, weights))
        res = ""
        if math.isclose(computed_weights, pkg_weight):
            res = " --! bingo !--"
        print(
            f"classic, almond, white = {i} {j} {nb_pops-i-j} {computed_weights:5.1f}"
            f" {computed_weights-pkg_weight:5.2f} {res}"
        )
print(f"total = {c}")
