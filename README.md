# Vehicle-Routing
Python implementation of Christofides heuristic for travelling salesman problem.

## Problem Statement
Travelling Salesman Problem is one of the computationally challenging combinatorial optimization problem that arise very often in industry.
The problem basically is to find best tour (minimum cost) in a complete graph such that all the nodes are visited exactly once (except starting node) and tour ends at the starting node.
For convenience, the graph is assumed undirected.

The problem is NP-hard. Although several exact and heuristic algorithms are available, Professor Nicos Christofides provided a heuristic that guarantees worst-case cost of 1.5 times the optimal cost while most heuristics have worst-case cost of twice the optimal cost.

More information to be added. 

One of the files mwmatching.py developed by [Joris van Rantwijk](http://jorisvr.nl/article/maximum-matching) was available open source. It finds a maximum weight matching in a general graph and is used in our implementation of Christofides algorithm.
