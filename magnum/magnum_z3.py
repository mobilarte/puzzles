#! env python

"""
Solving the Magnum Problem with z3.
"""

from z3 import Int, Solver, sat

# Weight of each popsicle.
classic = 41.5
almond = 44.3
white = 41.3

# Weight of package.
pkg_weight = 336.8

# Nb of popsicles per package.
nb_pop = 8

nb_classic = Int("nb_classic")
nb_almond = Int("nb_almond")
nb_white = Int("nb_white")

solver = Solver()

# Constraints to enforce at least one of each.
solver.add(nb_classic > 0)
solver.add(nb_almond > 0)
solver.add(nb_white > 0)

# Constraint for the total number of popsicles.
solver.add(nb_classic + nb_almond + nb_white == nb_pop)

# Constraints for the total weight.
solver.add(classic * nb_classic + almond * nb_almond + white * nb_white == pkg_weight)

# Solve and get the first solution.
if solver.check() == sat:
    
    model = solver.model()
    
    # stats = solver.statistics()

    print(f"classic, almond, white = "
          f"{model.eval(nb_classic)}, "
          f"{model.eval(nb_almond)}, "
          f"{model.eval(nb_white)}")
