# Description: a naive implementation of Google's PageRank algorithm.
#              this file is meant for illustration purposes ONLY.
#              don't use it in production environments.
# Author: Abdelrahman Hosny
# Class: UConn, CSE 3504, Spring 2016
# Instructor: Swapna Gokhale <ssg@eng.uconn.edu>
# TA: Abdelrahman Hosny <abdelrahman@engr.uconn.edu>

from __future__ import division
import numpy as np
from collections import defaultdict

websites = {}                           # a dictionary to keep track of website links and indices
graph = np.zeros(shape=(0,0))           # a matrix to represent the graph
nj = defaultdict(lambda: 0.0)           # number of outgoing link from node j

# Markov Chain variables
P = np.zeros(shape=(0,0))               # the transition matrix
p = np.zeros(shape=(0))                 # the state vector
damping_factor = 0.85                   # the damping factor

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

    P = P * damping_factor + (1-damping_factor)

    iteration = 0
    while True:
        iteration += 1
        previous = p
        p = np.dot(previous, P)
        if np.array_equal(previous, p) or np.inf in p:
            # reaching a steady state
            p = previous
            first_rank_websites = np.argwhere(p == np.amax(p))
            last_rank_websites = np.argwhere(p == np.amin(p))
            with open('ranks_'+str(damping_factor)+'.txt', 'w') as result_file:
                result_file.write('First Ranked Website(s)\n')
                for index in first_rank_websites:
                    result_file.write(str(index[0]+1) + ' ' + websites[index[0]] + '\n')
                result_file.write('\n')
                result_file.write('Last Ranked Website(s)\n')
                for index in last_rank_websites:
                    result_file.write(str(index[0]+1) + ' ' + websites[index[0]] + '\n')
            print 'Results written to file ..'
            break  # break from the infinite loop