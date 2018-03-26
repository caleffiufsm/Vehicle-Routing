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

## Assumptions
Since we are considering undirected graph, distance between two nodes is same irrespective of order they are traversed. This gives us a symmetric adjacency matrix.

## Code
vrs.py - This contains all the methods from creating _MST_ to finding Hamiltonian circuit. This also contains a method called greedy_tour which finds a tour based on greedy strategy.

mwmatching.py - This script has been developed by [Joris van Rantwijk](http://jorisvr.nl/article/maximum-matching) and was available open source. It finds a maximum weight matching in a general graph and is used in our implementation of Christofides algorithm. For our purpose, we simply provide negative weights to get minimum weight matching.

## Running instructions
Create a project on google cloud console and create an api key. Follow the instruction to create a google maps distance matrix API.

Run vrs.py. Enter the starting address where the tour is supposed to start. Provide the addresses of all the nodes to be visited. Enter # before entering the address of the last node (This is not where the tour will end, the tour ends on the starting address as original problem states).

Enter the API key generated at google cloud console.

## Requirement
1. Python 2 or 3
2. [Google Maps Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/start)

## References
1. [Heuristics for Travelling Salesman Problem](https://web.tuke.sk/fei-cit/butka/hop/htsp.pdf)
2. [Christofides Algorithm](https://en.wikipedia.org/wiki/Christofides_algorithm)
3. [Maximum Weight Matching by Joris van Rantwijk](http://jorisvr.nl/article/maximum-matching)


