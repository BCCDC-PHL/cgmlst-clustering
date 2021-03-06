#!/usr/bin/env python3

import argparse
import csv

import numpy as np

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering


def parse_distance_matrix(distance_matrix_path):
    labels = []
    distance_matrix = []
    with open(distance_matrix_path, 'r') as f:
        next(f) # skip header
        for line in f:
            line_split = line.strip().split(args.delimiter)
            label = line_split[0]
            distances = list(map(int, line_split[1:]))
            labels.append(label)
            distance_matrix.append(distances)

    distance_matrix = np.asmatrix(distance_matrix)
    
    return labels, distance_matrix

def plot_dendrogram(model, labels, **kwargs):
    """
    Create linkage matrix and then plot the dendrogram
    Adapted from:
    https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html
    """
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    print(counts)
    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)
    print(linkage_matrix)
    # Plot the corresponding dendrogram
    #truncate labels if they are longer than 20 characters
    leaf_label_func= lambda x: (labels[x][:6] + '...' + labels[x][-6:]) if len(labels[x]) > 20 else labels[x]
    dendrogram(linkage_matrix, leaf_label_func=leaf_label_func,leaf_rotation = 90, **kwargs)


def main(args):
    labels, distance_matrix = parse_distance_matrix(args.distance_matrix)
    
    clustering = AgglomerativeClustering(
        n_clusters=None,
        linkage='complete',
        compute_full_tree=True,
        distance_threshold=0,
        affinity='precomputed'
    )
    
    clusters = clustering.fit(np.asarray(distance_matrix))

    plt.title(args.title)
    plt.gcf().set_size_inches(8.5, 11)
    plot_dendrogram(clusters, labels)
    plt.savefig(args.output,bbox_inches='tight')
    
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('distance_matrix')
    parser.add_argument('-d', '--delimiter', default=',')
    parser.add_argument('-t', '--title', default='Hierarchical Clustering Dendrogram')
    parser.add_argument('-o', '--output', default='dendrogram.pdf')
    args = parser.parse_args()
    main(args)
