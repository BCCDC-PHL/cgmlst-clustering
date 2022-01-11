#!/usr/bin/env python3

import argparse
import csv

import numpy as np

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

def main(args):
    labels, distance_matrix = parse_distance_matrix(args.distance_matrix)
    
    clustering = AgglomerativeClustering(
        n_clusters=None,
        linkage='single',
        compute_full_tree=True,
        distance_threshold=args.threshold,
        affinity='precomputed'
    )

    cluster_ids = clustering.fit_predict(np.asarray(distance_matrix))

    clusters = {}
    for i in range(len(labels)):
        if cluster_ids[i] in clusters:
            clusters[cluster_ids[i]].append(labels[i])
        else:
            clusters[cluster_ids[i]] = [labels[i]]

    for cluster_id in sorted(clusters):
        for sample_id in sorted(clusters[cluster_id]):
            print(','.join([sample_id, str(cluster_id)]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('distance_matrix')
    parser.add_argument('-d', '--delimiter', default=',')
    parser.add_argument('-t', '--threshold', type=int, default=10)
    args = parser.parse_args()
    main(args)
