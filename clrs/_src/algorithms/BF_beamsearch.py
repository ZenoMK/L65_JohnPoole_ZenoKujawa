import numpy as np
import clrs._src.dfs_sampling as dfs_sampling

def beamsearch(A, s, probMatrix, beamwidth=3):
    """
    nicely decomposed. calls path_to_i for each node. returns parent tree.
    LeastCost path parent tree is sufficient for all leastCost paths,  since if leastCost path s->pi[t]->t didn't use leastCost path s->pi[t], there would be a lowerCost path s->t using s->pi[t]
    """
    vertices = range(len(probMatrix))
    pi = np.zeros(len(vertices))
    pi[s] = s
    for t in vertices:
        if t != s:
            least_cost_path = beamsearch_least_cost_path(A, s, t, probMatrix, beamwidth)
            pi[t] = least_cost_path[1] # paths in reverse order [a,b,c] means [c->b->a]. Path ends at t: [t,parent,...]
    return pi

def beamsearch_least_cost_path(A, s, t, probMatrix, beamwidth):
    '''compute path s->t. Note we go backwards, reconstructing path t->s'''
    # paths terminate in t
    path_guesses = [[i] for i in range(beamwidth)]  # paths in reverse order. [a,b,c] indicates [c->b->a]
    path_costs = [np.inf for i in range(beamwidth)]
    best_path_cost = np.inf
    best_path_from_s = None

    for k in range(1, len(probMatrix)):  # try paths of length up-to |V|, number of vertices
        longer_paths = []  # list of paths, each path in reverse order
        longer_path_costs = []  # list of path costs for new longer candidate paths

        # get paths length k
        longer_paths, longer_path_costs = add_beamsearch_parent_of_source_to_paths(A, probMatrix, beamwidth, path_guesses, path_costs)

        best_path_from_s = select_best_path_from_s(s, best_pathlonger_paths)# If any path begins with source node s, and has lower cost than current best path from s,
        # save it. (remember, paths in target->source order, so path[-1] is starting node)
        for path_ix in range(len(longer_paths)):
            path = longer_paths[path_ix]
            if path[-1] == s:
                path_cost = longer_path_costs[path_ix]
                if path_cost < best_path_cost:
                    best_path_from_s = path

        # filter for next iteration

    return parent_of_t

def add_parent_of_source_to_paths(A, probMatrix, beamwidth, path_guesses, path_costs):
    # Explore beam-many parents for each of the beam-many candidates
    longer_paths = []  # list of paths, each path in reverse order
    longer_path_costs = []  # list of path costs for new longer candidate paths

    for path_ix in range(len(path_guesses)):
        #print('ci', candidate_ix)
        path = path_guesses[path_ix]
        path_cost = path_costs[path_ix]
        #print('cp-1', candidate_path)
        highest_node = path[-1]  # most recent node added, conceptually the progenitor of path
        parent_probs = probMatrix[highest_node]

        new_path, new_path_cost = grow_path_by_parent_probs(path, path_cost, parent_probs)

    return

        # Extend candidate path by new parent, calculate cost
        # Store new path grown from this candidate, and its associated cost
        for new_path_num in range(beamwidth):
            new_parent = dfs_sampling.chooseUniformly(parent_probs)

            # extend & store path
            new_path = np.append(candidate_path,
                                 candidate_parent)  # concatenate parent to h, conceptually, adding a parent to path progenitor
            longer_paths.append(new_path)
            # calculate & store cost
            cost_of_new_edge = A[candidate_parent, highest_node]
            if cost_of_new_edge == 0:  # edge not in OG graph
                cost_of_new_edge = np.inf
            prev_cost = candidates_cost[candidate_ix]
            new_cost = prev_cost + cost_of_new_edge
            longer_path_costs.append(new_cost)


def BF_beamsearch(A, s, probMatrix, beamwidth=3):
    """
    Beamsearch sampler given a probmatrix returned by Bellman-Ford
    :param A: adjacency matrix
    :param s: source node
    :param probMatrix: model output
    :param beamwidth: the number of candidate solutions at any point
    :return: sampled parent tree
    """
    # optimizations possible, keep low-cost shorter paths over extending to bad parents
    # flip-coin for tie-breaking equal-cost kept-parents
    # tune-beam
    # sample without replacement
    try:
        pi = np.zeros(len(probMatrix))

        # make source its own parent
        pi[s] = s

        # assign parent to every node
        for i in range(len(probMatrix)):
            # compute path to i
            if i != s:

                # paths terminate in i
                candidates_rev = [[i] for i in range(beamwidth)] # paths in reverse order. [a,b,c] indicates [c->b->a]
                candidates_cost = [0 for i in range(beamwidth)]
                best_path_cost = np.inf
                best_path_stemming_from_s = None

                for k in range(len(probMatrix)): # try paths of length up-to |V|, number of vertices
                    longer_paths = [] # list of paths, each path in reverse order
                    longer_path_costs = [] # list of path costs for new longer candidate paths

                    # Explore beam-many parents for each of the beam-many candidates
                    for candidate_ix in range(len(candidates_rev)):
                        print('ci', candidate_ix)
                        candidate_path = candidates_rev[candidate_ix]
                        print('cp-1', candidate_path)
                        highest_node = candidate_path[-1] # most recent node added, conceptually the progenitor of path
                        parent_probs = probMatrix[highest_node]

                        # Extend candidate path by new parent, calculate cost
                        # Store new path grown from this candidate, and its associated cost
                        for new_path_num in range(beamwidth):
                            candidate_parent = dfs_sampling.chooseUniformly(parent_probs)
                            # extend & store path
                            new_path = np.append(candidate_path, candidate_parent) # concatenate parent to h, conceptually, adding a parent to path progenitor
                            longer_paths.append(new_path)
                            # calculate & store cost
                            cost_of_new_edge = A[candidate_parent, highest_node]
                            if cost_of_new_edge == 0: # edge not in OG graph
                                cost_of_new_edge = np.inf
                            prev_cost = candidates_cost[candidate_ix]
                            new_cost = prev_cost + cost_of_new_edge
                            longer_path_costs.append(new_cost)

                    # If any path begins with source node s, and has lower cost than current best path from s,
                    # save it. (remember, paths in target->source order, so path[-1] is starting node)
                    for path_ix in range(len(longer_paths)):
                        path = longer_paths[path_ix]
                        if path[-1] == s:
                            path_cost = longer_path_costs[path_ix]
                            if path_cost < best_path_cost:
                                best_path_stemming_from_s = path

                    # Select the (beam width)-many best paths (lowest weight in original graph); explored further next loop.
                    path_ixs_by_lowest_cost = np.argsort(longer_path_costs)
                    best_3_ixs = path_ixs_by_lowest_cost[:beamwidth]
                    candidates_rev = np.array(longer_paths)[best_3_ixs] # select paths for next-round according to best beam-many cost-minimizing indices

            if best_path_stemming_from_s is not None:
                pi[i] = best_path_stemming_from_s[1] # node before i on best_path_found
            else:
                print('no good path')
                breakpoint() #oops! no good path
    except:
        print('other error')
        breakpoint()

    return pi




def BF_beamsearch_OLD(A, s, probMatrix, beamwidth=3):
    """
    Beamsearch sampler given a probmatrix returned by Bellman-Ford
    :param A: adjacency matrix
    :param s: source node
    :param probMatrix: model output
    :param beamwidth: the number of candidate solutions at any point
    :return: sampled parent tree
    """
    # TODO: simplify, since we don't use the fact that newpaths are grown by candidates (unnecessary list of lists)
    # optimizations possible, keep low-cost shorter paths over extending to bad parents
    # flip-coin for tie-breaking equal-cost kept-parents

    pi = np.zeros(len(probMatrix))

    # make source its own parent
    pi[s] = s

    # assign parent to every node
    for i in range(len(probMatrix)):
        # compute path to i
        if i != s:

            # paths terminate in i
            candidates_rev = [[i] for i in range(beamwidth)] # paths in reverse order. [a,b,c] indicates [c->b->a]
            candidates_cost = [0 for i in range(beamwidth)]
            best_path_stemming_from_s = None
            best_path_cost = np.inf

            for k in range(len(probMatrix)): # try paths of length up-to |V|, number of vertices
                longer_paths_by_candidate = [] # list of lists: each inner list contains paths grown by 1 parent from candidate
                longer_path_costs = [] # list of lists: each inner list contains path costs for new longer candidate paths

                # Explore beam-many parents for each of the beam-many candidates
                for candidate_ix in range(len(candidates_rev)):
                    candidate_path = candidates_rev[candidate_ix]
                    highest_node = candidate_path[-1] # most recent node added, conceptually the progenitor of path
                    parent_probs = probMatrix[highest_node]
                    my_new_paths = []
                    my_new_costs = []

                    # Extend candidate path by new parent, calculate cost
                    for new_path_num in range(beamwidth):
                        candidate_parent = dfs_sampling.chooseUniformly(parent_probs)
                        # extend path
                        new_path = candidate_path + [candidate_parent] # concatenate parent to h, conceptually, adding a parent to path progenitor
                        my_new_paths.append(new_path)
                        # calculate cost
                        cost_of_new_edge = A[candidate_parent, highest_node]
                        if cost_of_new_edge == 0: # edge not in OG graph
                            cost_of_new_edge = np.inf
                        prev_cost = candidates_cost[candidate_ix]
                        new_cost = prev_cost + cost_of_new_edge
                        my_new_costs.append(new_cost)

                    # Store new paths grown from this candidate, and their associated costs
                    longer_paths_by_candidate.append(my_new_paths)
                    longer_path_costs.append(my_new_costs)

                # Select the (beam width)-many best paths (lowest weight in original graph); explored further next loop.
                longer_paths = np.ravel(longer_paths_by_candidate) # flatten
                longer_path_costs = np.ravel(longer_path_costs)
                #
                best_paths = [None for i in range(beamwidth)]
                best_path_costs = [np.inf for i in range(beamwidth)]
                for cand_path_ix in range(len(longer_paths_by_candidate)):
                    cand_paths = longer_paths_by_candidate[cand_path_ix]
                    for path_ix in range(len(cand_paths)):
                        path = cand_paths[path_ix]
                        cost = longer_path_costs[cand_path_ix][path_ix]

                        # If any path begins with source node s, and has lower cost than current best path from s,
                        # save it. (remember, paths in target->source order, so path[-1] is starting node)
                        if path[-1] == s:
                            if cost < best_path_cost:
                                best_path_stemming_from_s = path

            #best_path_stemming_from_s

    return best_paths




if __name__ == '__main__':
    #testexample
    pM = np.array([[6.7942673e-03, 1.8254748e-06, 5.3676311e-04, 5.6340452e-04,
            9.9210370e-01],
           [8.2969433e-04, 9.4034225e-01, 5.7718944e-02, 2.6801512e-05,
            1.0822865e-03],
           [1.4186887e-01, 2.8001370e-02, 8.2659137e-01, 5.6764267e-05,
            3.4815797e-03],
           [8.1846189e-01, 3.9187955e-05, 9.7058117e-05, 1.7738120e-01,
            4.0207091e-03],
           [3.3088622e-03, 1.5012523e-07, 3.4113563e-07, 2.7682628e-07,
            9.9669027e-01]])

    A = np.array([[1., 0., 1., 1., 1.],
                 [0., 0., 1., 0., 0.],
                 [1., 1., 0., 0., 0.],
                 [1., 0., 0., 1., 0.],
                 [1., 0., 0., 0., 1.]])

    s = 3

    result = BF_beamsearch(A,s,pM)
