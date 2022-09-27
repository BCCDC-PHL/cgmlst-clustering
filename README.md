# cgmlst-clustering

cgmlst-clustering takes the combined allele profile from the output of the [kma-cgmlst](https://github.com/BCCDC-PHL/kma-cgmlst) pipeline, calculate distance and perform dendrogram and clustering.


The distance is calculated by [cgmlst-dists](https://github.com/tseemann/cgmlst-dists).

You can specify pairwise comparison to count missing as differences by using ```mode``` parameter.

## Input
| Arguments      | Usage      | 
|----------------|:----------:|
|cgmlst  | a combined allele profile calls from the kma-cgmlst pipeline, in .csv format  |
|threshold   | threshold for AgglomerativeClustering, can be a list of numbers in a quotation, e.g. '5 10 15' |
|outdir      | output directory |
|runClustering| a single argument that specify if clustering should be run |
|linkage_type | linkage type for AgglomerativeClustering, possible choice is 'single', 'average', 'complete'|
|mode | if mode="count-missing" then pairwise comparison includes missing, otherwise it ignores missing |


## Usage

For initial run without clustering:
```
nextflow run BCCDC-PHL/cgmlst-clustering --cgmlst <path/to/combined_cgmlst.csv> --outdir <path/to/output_dir>
```

This will produce a dendrogram for examining.

For rerunning with clustering after determining the thresholds from looking at the dendrogram, add all arguments for clusterings and `-resume` to continue the nextflow pipeline from cache:

```
nextflow run BCCDC-PHL/cgmlst-clustering \
  --cgmlst <path/to/combined_cgmlst.csv> \
  --runClustering \
  --threshold '25 50 75 100 125 150 200 250 300 350 400' \
  --linkage_type 'single' \
  --outdir <path/to/output_dir> \ 
  -resume
```

### Sample sheet
You can supply a samplesheet.csv to specify which samples are to be included for clustering. Samplesheet.csv can follow the same format as those for [kma-cgmlst] (https://github.com/BCCDC-PHL/kma-cgmlst), i.e, three columns with ID,R1,R2. Or it could a csv with only one column ID. When running the pipeline using samplesheet input, use `--samplesheet_input` flag:


```
nextflow run BCCDC-PHL/cgmlst-clustering \
  --cgmlst <path/to/combined_cgmlst.csv> \
  --outdir <path/to/output_dir> \
  --samplesheet_input <path/to/samplesheet.csv>
```

or 

```
nextflow run BCCDC-PHL/cgmlst-clustering \
  --cgmlst <path/to/combined_cgmlst.csv> \
  --runClustering \
  --threshold '25 50 75 100 125 150 200 250 300 350 400' \
  --linkage_type 'single' \
  --outdir <path/to/output_dir> \ 
  --samplesheet_input <path/to/samplesheet.csv> \
  -resume
```