# cgmlst-clustering

cgmlst-clustering takes the output of the [kma-cgmlst](https://github.com/BCCDC-PHL/kma-cgmlst) pipeline, combine all allele call profiles for all samples, calculate distance and perform dendrogram and clustering.


The distance is calculated by [cgmlst-dists](https://github.com/tseemann/cgmlst-dists).


## Input
| Arguments      | Usage      | 
|----------------|:----------:|
|kma_folder  | folder path for kma_cgmlst sample output folders |
|threshold   | threshold for AgglomerativeClustering, can be a list of numbers in a quotation, e.g. '5 10 15' |
|outdir      | output directory |
|runClustering| a single argument that specify if clustering should be run |
|linkage_type | linkage type for AgglomerativeClustering, possible choice is 'single', 'average', 'complete'|


## Usage

For initial run without clustering:
```
nextflow run BCCDC-PHL/cgmlst-clustering --kma_folder cgmlst --outdir output
```

This will produce a dendrogram for examining.

For rerunning with clustering after determining the thresholds from looking at the dendrogram, add all arguments for clusterings and `-resume` to continue the nextflow pipeline from cache:

```
nextflow run BCCDC-PHL/cgmlst-clustering \
  --kma_folder cgmlst \
  --runClustering \
  --threshold '25 50 75 100 125 150 200 250 300 350 400' \
  --linkage_type 'single' \
  --outdir output \ 
  -resume
```
