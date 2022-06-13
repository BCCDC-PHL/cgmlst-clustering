#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

process filter_by_samplesheet{

    publishDir params.outdir, mode: 'copy'

    input:
    path(cgmlsttab)
    path(samplesheet)

    output:
    path("filtered_cgmlst.tab")

    """
    cat ${samplesheet} | cut -d',' -f1 > ids.csv
    awk -F '\t' 'NR==FNR {id[\$1]; next} \$1 in id' ids.csv ${cgmlsttab} > filtered_cgmlst.tab
    
    """
}
process combine_cgmlst{

    publishDir params.outdir, mode: 'copy'

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
    publishDir params.outdir, mode: 'copy'

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
    publishDir params.outdir, mode: 'copy'

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
    publishDir params.outdir, mode: 'copy'
    
    when:
    params.runClustering == true

    input:
    path(distance_matrix)

    output:
    path("${params.linkage_type}_cluster_*.csv")

    script:
    """

    for i in ${params.threshold}; do cluster.py  ${distance_matrix} -t \${i} --linkage ${params.linkage_type} | awk 'BEGIN {OFS=","; print "run_accession","our_clusters"} {print \$0}' > ${params.linkage_type}_cluster_\${i}.csv; done
   
    """
}


workflow {

   
    ch_cgmlst = Channel.fromPath(params.kma_folder)
    combine_cgmlst(ch_cgmlst)

    if(params.samplesheet_input != 'NO_FILE'){
    //filter out combined_cgmlst.csv based on sample ids in the sample sheet
    ch_samplesheet = Channel.fromPath(params.samplesheet_input)   
    
    filter_by_samplesheet(combine_cgmlst.out, ch_samplesheet)    
    calculate_distance(filter_by_samplesheet.out)	
    }else{

    calculate_distance(combine_cgmlst.out)
    
   }
    dendrogram(calculate_distance.out)
    cluster_py(calculate_distance.out)


}
