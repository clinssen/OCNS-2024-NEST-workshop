import matplotlib.pyplot as pl
import matplotlib.patches as patches
import numpy as np
import nest

class ParameterSet(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def is_integer(x):
    """
    Check if value is (close to) integer.

    :param x:
    :return:
    """
    return np.isclose(x, np.rint(x))


def no_overlap(rho, n_stim, map_size, n_src):
    """
    Determine whether a modular connectivity matrix can be created without overlap between the maps.

    :param rho:
    :param n_stim:
    :param map_size:
    :param n_src:
    :return:
    """

    return rho <= 1. / n_stim and map_size * n_stim <= n_src


def get_map_size(rho, n):
    """

    :param rho:
    :param n:
    :return:
    """
    size_f = rho * n  # float
    assert np.isclose(size_f, np.rint(size_f)), "Value of delta (step size) leads to inconsistent map sizes! " \
                                                "Make sure the resulting map sizes are integers!"

    return np.rint(size_f).astype(int)


def get_overlap_size(map_size, map_idx, n, n_stim):
    """

    :param map_size:
    :param map_idx:
    :param n:
    :param n_stim:
    :return:
    """
    excess = abs(n - (map_size * n_stim))
    overlap = float(excess) / (n_stim - 1)

    # TODO this is a workaround to find the correct placement of the last cluster in the case when the
    # TODO overlap is not an integer..
    # if map_idx == n_stim - 1 and overlap > 1. and not is_integer(overlap):
    #     overlap = excess - (n_stim - 2) * np.floor(overlap)
    # print('\nWARNING: overlap in target layer is not an integer, applying compensation for last cluster')

    # return np.floor(overlap).astype(int)
    return np.ceil(overlap).astype(int)


def get_source_clusters(n_src, n_stim, rho_src=None):
    """
    Returns a list of clusters (lists) for each stimulus, ensuring that each one contains an equal number of neurons.
    For this, overlapping must be handled properly.

    :param n_src:
    :param n_stim:
    :param rho_src:
    :return:
    """
    if rho_src is None:
        rho_src = 1./n_stim

    # compute size of map
    map_size = get_map_size(rho_src, n_src)

    clusters = []

    if no_overlap(rho_src, n_stim, map_size, n_src):
        return [np.arange(map_size * n, map_size * (n + 1), 1) for n in range(n_stim)]
    else:
        start_idx = 0
        stop_idx = map_size

        for map_idx in range(n_stim):
            overlap = get_overlap_size(map_size, map_idx, n_src, n_stim)

            if map_idx > 0:
                start_idx = stop_idx - overlap
                stop_idx = start_idx + map_size
            clusters.append(np.arange(start_idx, stop_idx))

    return clusters

def get_all_clusters(n_layers, n_stim, N, NE, NI, rho_src=None):
    """
    :return:
    """
    if rho_src is None:
        rho_src = 1./n_stim

    map_size_e = get_map_size(rho_src, NE)
    map_size_i = get_map_size(rho_src, NI)

    clusters = {'E': [], 'I': []}

    for l in range(n_layers):
        c = [np.arange(map_size_e * n + l*N, map_size_e * (n + 1) + l*N, 1) + 1 for n in range(n_stim)]  # +1 for NEST gid
        clusters['E'].append([nest.NodeCollection(x) for x in c])

        c = [np.arange(map_size_i * n + l*N + NE, map_size_i * (n + 1) + l*N + NE, 1) + 1 for n in range(n_stim)]
        clusters['I'].append([nest.NodeCollection(x) for x in c])

    return clusters



def compute_density_matrix(A):
    return np.count_nonzero(A) / float(A.shape[0] * A.shape[1])


def compute_density_theory(map_src, map_tgt, n_src, n_tgt, p_0, p_c, n_stim):
    """
    Computes the theoretical density.

    :param map_src:
    :param map_tgt:
    :param n_src:
    :param n_tgt:
    :param p_0:
    :param p_c:
    :param n_stim:
    :return:
    """
    if n_stim * map_src < n_src:
        C_0 = int(n_src * n_tgt - n_stim * map_src * map_tgt)
        C_c = int(n_stim * map_src * map_tgt)
    else:
        C_c = int(n_tgt * n_src - float(n_stim) / (n_stim - 1) * ((n_tgt - map_tgt) * (n_src - map_src)))
        C_0 = int(float(n_stim) / (n_stim - 1) * ((n_tgt - map_tgt) * (n_src - map_src)))

    return (p_0 * C_0 + p_c * C_c) / (n_src * n_tgt)


def get_topographic_probabilities(sigma, m, n_stim, n_src, n_tgt, map_size_src, map_size_tgt, debug=False):
    """
    Calculate the inter/intra-cluster probabilities depending on the density (sigma) and modularity, as well as the
    computed map sizes in the source and target clusters.

    :param sigma: target density of connection matrix
    :param m: modularity
    :param n_stim: number of stimuli
    :param n_src: neurons in source population
    :param n_tgt: neurons in target population
    :param map_size_src:
    :param map_size_tgt:
    :return: p_c, p_0
    """
    if n_stim * map_size_src <= n_src:
        C_c = n_stim * map_size_src * map_size_tgt
        C_0 = n_src * n_tgt - C_c
    else:
        C_0 = float(n_stim) / (n_stim - 1) * (n_src - map_size_src) * (n_tgt - map_size_tgt)
        C_c = n_src * n_tgt - C_0

    assert np.isclose(C_0, np.rint(C_0)), "C_0 is inconsistent (float)!"
    assert np.isclose(C_c, np.rint(C_c)), "C_c is inconsistent (float)!"

    coefficients = np.array([[C_c, C_0], [m - 1, 1]])
    results = np.array([sigma * n_src * n_tgt, 0])
    x = np.linalg.solve(coefficients, results)
    assert x[0] <= 1., "Map size too small for density = {} and modularity = {}, as p_c = {} is impossible!". \
        format(sigma, m, x[0])
    assert x[1] <= 1., "Something went wrong, p_0 = {}?!".format(x[1])

    return x[0], x[1]


def generate_modular_connections(n_src, n_tgt, mod_pars, src_layer=0, tgt_layer=1, plot=False, debug=False):
    """
    Generates a structured feed-forward connection matrix.

    :param n_src: number of source neurons (e.g., generators / channels)
    :param n_tgt: number of neurons in target populations
    :param src_layer: index of the source layer
    :param tgt_layer: index of the target layer (usually src_layer + 1)
    :param plot:
    :param debug:
    :return: numpy array of weights [n_src x n_targets]
    """
    # if not hasattr(mod_pars, 'rho'):
    rho_src = mod_pars.rho0 + src_layer * mod_pars.delta  # i-1
    rho_tgt = mod_pars.rho0 + tgt_layer * mod_pars.delta  # i
    # else:
    #     rho_src = mod_pars.rho0 if src_layer == 0 else mod_pars.rho
    #     rho_tgt = mod_pars.rho
    src_clusters = get_source_clusters(n_src=n_src, n_stim=mod_pars.n_stim, rho_src=rho_src)

    # compute size of map (#neurons) in target layer
    map_size_tgt = get_map_size(rho_tgt, n_tgt)
    map_size_src = len(src_clusters[0])

    p_c, p_0 = get_topographic_probabilities(mod_pars.sigma, mod_pars.m, mod_pars.n_stim, n_src, n_tgt,
                                             map_size_src, map_size_tgt, debug)

    A = np.zeros((n_src, n_tgt))

    start_idx = 0
    stop_idx = map_size_tgt

    # overlap between the modules among the target neurons (will change later - horizontal in the FF conn matrix)
    h_overlap = 0
    # overlap between the modules in the source population (vertical in the FF connection matrix; same for all clusters)
    v_overlap = len(set(src_clusters[0]).intersection(src_clusters[1]))

    stimulus_segments = list()

    # deal with stimulus specific clusters
    for map_idx, src_pop in enumerate(src_clusters):
        # if we can create entirely segregated clusters, without any overlap, and we actually want it
        if rho_tgt <= 1./mod_pars.n_stim and map_size_tgt * mod_pars.n_stim <= n_tgt:
            start_idx = map_idx * map_size_tgt
            stop_idx = int((map_idx + 1) * map_size_tgt)

        # handle overlap
        else:
            h_overlap = get_overlap_size(map_size_tgt, map_idx, n_tgt, mod_pars.n_stim)

            if map_idx > 0:
                start_idx = stop_idx - h_overlap
                stop_idx = start_idx + map_size_tgt

        if debug:
            print('src cluster for layer {2}: [{0}-{1}]\t->\t[{3} - {4}]'.format(min(src_pop), max(src_pop), tgt_layer,
                                                                                 start_idx, stop_idx - 1))

        # putative target neuron ids
        putative_intra_tgts = np.arange(start_idx, stop_idx)
        putative_inter_tgts = np.concatenate((np.arange(start_idx), np.arange(stop_idx, n_tgt)))  # before and after

        # number of total intra-/inter-cluster connections for this stimulus
        k_c = int(p_c * map_size_src * map_size_tgt)
        k_0 = int(p_0 * map_size_src * (n_tgt - map_size_tgt))

        #############################################################
        # draw the connections and mark them in the connection matrix

        # randomly sample items from a flattened connectivity matrix, the drawn connection items will be expanded later
        if k_c:
            flattened_ids_intra = np.random.choice(np.arange(map_size_src * map_size_tgt), k_c, replace=False)
        else:
            flattened_ids_intra = 0
        # only if there are new inter-cluster connections
        if k_0:
            flattened_ids_inter = np.random.choice(np.arange(map_size_src * (n_tgt - map_size_tgt)), k_0, replace=False)
        else:
            flattened_ids_inter = 0

        # expand the flattened connection ids computed above and store source-target pairs for intra- and inter
        src_neurons_intra = (flattened_ids_intra / map_size_tgt).astype(int)
        tgt_neurons_intra = (flattened_ids_intra % map_size_tgt).astype(int)

        src_neurons_inter = (flattened_ids_inter / (n_tgt - map_size_tgt)).astype(int)
        tgt_neurons_inter = (flattened_ids_inter % (n_tgt - map_size_tgt)).astype(int)

        # avoid duplicating connections by removing some new ones but also some existing ones
        if v_overlap and map_idx:
            # remove would-be within-cluster duplicates
            if k_c:
                to_delete = np.intersect1d(np.where(src_neurons_intra < v_overlap), np.where(tgt_neurons_intra < h_overlap))
                src_neurons_intra = np.delete(src_neurons_intra, to_delete)
                tgt_neurons_intra = np.delete(tgt_neurons_intra, to_delete)

            # remove would-be inter-cluster duplicates, only if there are new inter-cluster connections
            if k_0:
                to_delete = np.where(src_neurons_inter < v_overlap)
                src_neurons_inter = np.delete(src_neurons_inter, to_delete)
                tgt_neurons_inter = np.delete(tgt_neurons_inter, to_delete)

            #
            A[np.ix_(src_pop[:v_overlap], putative_intra_tgts[h_overlap:])] = 0

        # update binary connectivity matrix using correct indices from the putative arrays
        if k_c:
            A[src_pop[src_neurons_intra], putative_intra_tgts[tgt_neurons_intra]] = 1

        if k_0:
            A[src_pop[src_neurons_inter], putative_inter_tgts[tgt_neurons_inter]] = 1

        if plot:
            stimulus_segments.append(((min(src_pop), max(src_pop)), (start_idx, stop_idx - 1)))

    ########
    # ensure that neurons not in a topographic map - free neurons, if there are any, still project randomly with p_0
    putative_tgts = np.arange(n_tgt)
    for src_neuron in range(max(src_clusters[-1]) + 1, n_src):
        targets = np.random.choice(putative_tgts, int(n_tgt * p_0), replace=False).astype(int)
        A[src_neuron, targets] = 1

    density_text = None

    if debug:
        density = compute_density_matrix(A)
        density_theory = compute_density_theory(map_size_src, map_size_tgt, n_src, n_tgt,
                                                p_0, p_c, mod_pars.n_stim)

        print('\nLayer {} -> {}\n\tComputed density: {}\n\tTheoretical density: {}\n\tDiscrepancy: {}'.format(
            src_layer, tgt_layer, density, density_theory, abs(density_theory - density)))

        density_text = 'Layer {} -> {}\nComputed density: {}\nTheoretical density: {}\nDiscrepancy: {}\np_c: {}, ' \
                       'p_0: {}'.format(src_layer, tgt_layer, density, density_theory,
                                        abs(density_theory - density), p_c, p_0)

        assert abs(density_theory - density) < 0.01, "Large discrepancy"

    # return connection matrix augmented with appropriate weights for E and I connections
    # and list of stimulus target segments
    return A * mod_pars.wE, stimulus_segments, density_text


def print_weight_matrix(W, label=None, ax=None, cmap='Greys', save=False):
    """
    E/D
    This is version 1 as per the documentation. In this case we have no real control over p_u
    at population level, rather only at single neuron level within a stimulus-specific sub-population.
    :return:
    """
    if ax is None:
        fig = pl.figure()
        ax = fig.add_subplot(111)
    if label is not None:
        ax.set_title(label)

    plot = ax.imshow(W, cmap=cmap, interpolation="none", aspect='auto')

    if cmap != 'Greys':
        cbar = pl.colorbar(plot, ax=ax)

    ax.grid(False)
    ax.tick_params(labelsize=12)
    if save:
        fig.tight_layout()
        fig.savefig('{}.pdf'.format(save))


def plot_connection_matrices(W, stim_segments, n_stim, title, save):
    """

    :param W:
    :param stim_segments:
    :param n_stim:
    :param save:
    :return:
    """
    fig = pl.figure(figsize=(6, 6))
    ax = pl.subplot2grid((1, 1), (0, 0))
    print_weight_matrix(W, ax=ax)
    seg_colors = ['g', 'r', 'b', 'm', 'y']

    for seg_idx, seg in enumerate(stim_segments):
        src_start = seg[0][0]
        src_end = seg[0][1]
        tgt_start = seg[1][0]
        tgt_end = seg[1][1]
        rect = patches.Rectangle((tgt_start, src_start), tgt_end - tgt_start, src_end - src_start,
                                 linewidth=1.5, edgecolor=seg_colors[seg_idx], facecolor='none')
        ax.add_patch(rect)

    if title:
        ax.set_title(title, fontsize=10)

    ax.tick_params(axis='both', which='major', labelsize=10)

    fig.tight_layout()
    if save:
        fig.savefig(save)


def modular_matrix(layer, N, src_neurons, tgt_neurons, n_clusters, density, modularity, rho0=None):
    """
    Generate a modular adjacency matrix.

    :param src_neurons: number of pre- and post-synaptic neurons (assumes equal)
    :param n_clusters: number of clusters
    :param density: connection density (total)
    :param modularity: degree of modularity (0 for homogeneous, 1 for perfectly modular)
    :param rho0: relation between intra and inter-cluster density (if None, keep equal to density)
    """
    if rho0 is None:
        rho0 = 1./n_clusters
    mod_pars = ParameterSet({
        'rho0': rho0,
        'm': modularity,
        'sigma': density,
        'n_stim': n_clusters,
        'wE': 1.0,
        'N': src_neurons,
        'delta': 0.
    })

    # leave layer_tgt = 1 and src_layer = 0 to generate 1 matrix..
    adjacency, clusters, text = generate_modular_connections(n_src=src_neurons, n_tgt=tgt_neurons,
                                                                      src_layer=0, tgt_layer=1,
                                                                      mod_pars=mod_pars, plot=True, debug=False)
    # clusters = [nest.NodeCollection(np.arange(ct[1][0] + (layer + 1) * N + 1, ct[1][1] + (layer + 1) * N + 1))
    # clusters = [np.arange(ct[1][0] + (layer + 1) * N + 1, ct[1][1] + (layer + 1) * N + 1)
    #             for ct in clusters]
    return adjacency
