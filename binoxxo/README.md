# BinOXXO

## The Game

Binoxxo is a binary puzzle played on a 10 by 10 grid that is prefilled with o and x. The goal is to complete the grid following these rules:

- even number of o and x per row and column
- no two identical rows or columns
- not more than 2 adjacent o or x

## The Solution

Two solutions are shown:

- a classic brute force approach, with some heuristics.
- a formulation of the problem solved by CP-SAT from [OR-Tools](https://developers.google.com/).
- an identical formulation of the problem solved by the [Z3 Theorem Prover](https://github.com/Z3Prover/z3).