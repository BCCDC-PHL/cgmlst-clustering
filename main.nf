#!/usr/bin/env nextflow

params.kma_folder = '/scratch/sherrie.wang/PRJEB40777/output'
params.output="."

process combine_cgmlst{

    publishDir params.output

    output:
    file("combined_cgmlst.csv") 

    """
    dirs=(${params.kma_folder}/*/)
    echo \$dirs

    DIRNAME=\$(basename \$dirs)
    
    head -n 1 \$dirs\$DIRNAME"_cgmlst.csv" > cgmlst_header.csv
    tail -qn+2 ${params.kma_folder}/*/*_cgmlst.csv > combined_cgmlst_data.csv
    cat cgmlst_header.csv combined_cgmlst_data.csv > combined_cgmlst.csv

    """

}