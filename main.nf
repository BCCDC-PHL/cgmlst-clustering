#!/usr/bin/env nextflow

nextflow.enable.dsl = 2


params.kma_folder = '/scratch/sherrie.wang/PRJEB40777/output'
params.output="."
params.runClustering = false
params.threshold=50
params.linkage_type='Single'

process combine_cgmlst{

    publishDir params.output

    input:
    path(cgmlst)

    output:
    path("combined_cgmlst.tab") 

    """
    dirs=(${cgmlst}/*/)
    echo \$dirs

    DIRNAME=\$(basename \$dirs)
     
    head -n 1 \$dirs\$DIRNAME"_cgmlst.csv" > cgmlst_header.csv
    tail -qn+2 ${cgmlst}/*/*_cgmlst.csv > combined_cgmlst_data.csv
    cat cgmlst_header.csv combined_cgmlst_data.csv > combined_cgmlst.csv
    sed 's|,|\t|g' combined_cgmlst.csv > combined_cgmlst.tab
    """

}

process calculate_distance {
    publishDir params.output

    input:
    path(cgmlst_tab)

    output:
    path("distance.csv")

    script:
    """
    cgmlst-dists -c ${cgmlst_tab} > distance.csv

    """

}

process dendrogram {
    publishDir params.output

    input:
    path(distance_matrix)

    output:
    path("dendrogram.pdf")

    script:
    """
    dendrogram.py ${distance_matrix}

    """

}

process cluster_py {
    when:
    params.runClustering == true

    
    input:
    tuple path(distance_matrix)

    output:
    path('runclustering')

    script:
    """

    echo cluster.py  ${distance_matrix} -t ${params.threshold} --linkage ${params.linkage_type} > runclustering
    """
}


workflow {


    ch_cgmlst = Channel.fromPath(params.kma_folder)
    
    combine_cgmlst(ch_cgmlst)
    calculate_distance(combine_cgmlst.out)
    dendrogram(calculate_distance.out)
    cluster_py(calculate_distance.out)


}
