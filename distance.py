#!/usr/bin/env python

import argparse


def line_to_sample(line):
    line_split = line.split(args.delimiter)
    sample_id = line_split[0]
    alleles = line_split[1:-1]
    sample = (sample_id, alleles)
    return sample


def compare_two(sample1, sample2):
    distance = 0
    sample1_alleles = sample1[1]
    sample2_alleles = sample2[1]
    for i in range(len(sample1_alleles)):
        if args.ignore_missing and (sample1_alleles[i] == '-' or sample2_alleles[i] == '-'):
            continue
        elif sample1_alleles[i] != sample2_alleles[i]:
            distance += 1

    return distance


def compare_against_all(sample, cgmlst_path):
    distances = {sample[0]: {}}
    with open(cgmlst_path, 'r') as f:
        next(f) # skip the header
        for line in f:
            sample2 = line_to_sample(line.strip())
            distance = compare_two(sample, sample2)
            distances[sample[0]][sample2[0]] = distance

    return distances
    


def main(args):

    all_sample_ids = []
    with open(args.cgmlst, 'r') as f:
        next(f)
        for line in f:
            all_sample_ids.append(line.split(args.delimiter)[0])

    print(','.join([''] + all_sample_ids))

    with open(args.cgmlst, 'r') as f:
        next(f) # skip the header
        for line in f:
            sample = line_to_sample(line.strip())
            distances = compare_against_all(sample, args.cgmlst)
            output = [sample[0]]
            for s in all_sample_ids:
                output.append(str(distances[sample[0]][s]))
            print(','.join(output))
            
            
            
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cgmlst')
    parser.add_argument('-d', '--delimiter', default=',')
    parser.add_argument('-i', '--ignore-missing', action='store_true')
    args = parser.parse_args()
    main(args)
