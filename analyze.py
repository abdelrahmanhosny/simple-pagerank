# Description: the most basic implementation of the PageRank algorithm
# Author: Abdelrahman Hosny
# Class: UConn, CSE 3504, Spring 2016
# Instructor: Swapna Gokhale

from __future__ import division
import numpy as np
from collections import defaultdict

websites = {}                           # a dictionary to keep track of website links and indices
graph = np.zeros(shape=(0,0))           # a matrix to represent the graph
nj = defaultdict(lambda: 0.0)           # number of outgoing link from node j

# Markov Chain variables
P = np.zeros(shape=(0,0))               # the transition matrix
p = np.zeros(shape=(0))                 # the state vector
damping_factor = 0.85

with open('hollins.dat', 'r') as data_file:
    number_of_websites, number_of_hyperlinks = map(int, data_file.readline().strip().split(' '))

    for i in range(number_of_websites):
        index, link = data_file.readline().strip().split(' ')
        websites[int(index)-1] = link                                   # save websites to 0 index

    graph = np.zeros(shape=(number_of_websites, number_of_websites))    # initialize the graph
    P = np.zeros(shape=(number_of_websites, number_of_websites))        # initialize the transition matrix
    p = np.empty(number_of_websites)                                    # initialize the state vector

    for i in range(number_of_hyperlinks):
        source_website, destination_website = map(int, data_file.readline().strip().split(' '))
        nj[source_website-1] += 1                                       # keep track of the number of outgoing links from each website
        graph[source_website-1][destination_website-1] = 1              # update the graph

    # modifying the initial state vector according to PageRank algorithm
    p.fill(1 / number_of_websites)                                      # all website have the same probability

    # modifying the transition matrix P according to PageRank formula
    # can you convert these ugly for loops to matrix computations?
    for i in range(number_of_websites):
        for j in range(number_of_websites):
            if graph[j][i] == 1:
                P[i][j] = 1 / nj[j]

    P = np.add(np.multiply(P, damping_factor), (1 - damping_factor))

    iteration = 0
    while True:
        iteration += 1
        previous = p
        p = np.dot(previous, P)
        if np.array_equal(previous, p) or np.inf in p:
            p = previous
            print len(np.argwhere(p == np.amax(p)))
            print len(np.argwhere(p == np.amin(p)))
            break