# Vehicle-Routing
Python implementation of Christofides heuristic for travelling salesman problem.

## Problem Statement
Travelling Salesman Problem is one of the computationally challenging combinatorial optimization problem that arise very often in industry.
The problem basically is to find best tour (minimum cost) in a complete graph such that all the nodes are visited exactly once (except starting node) and tour ends at the starting node.
For convenience, the graph is assumed undirected.

The problem is NP-hard. Although several exact and heuristic algorithms are available, Professor Nicos Christofides provided a heuristic that guarantees worst-case cost of 1.5 times the optimal cost while most heuristics have worst-case cost of twice the optimal cost.

## Algorithm
1. Given a complete undirected graph _G_, create a minimum spanning tree _MST_.
2. Find the set of vertices _O_ in _MST_ with odd degrees.
3. Form a subgraph of _G_ using vertices from _O_.
4. Create a perfect-matching subgraph _M_ on subgraph obtained in step 3.
5. Take union of _M_ and _MST_.
6. Find a Euler tour on the union.
7. Find Hamiltonian circuit on the Euler tour bypassing repeated vertices.

## Code
vrs.py - This contains all the functions from creating _MST_ to finding Hamiltonian circuit.

mwmatching.py - This script has been developed by [Joris van Rantwijk](http://jorisvr.nl/article/maximum-matching) and was available open source. It finds a maximum weight matching in a general graph and is used in our implementation of Christofides algorithm. For our purpose, we simply provide negative weights to get minimum weight perfect matching.

More information to be added. 

