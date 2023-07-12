# HeatMaps for Senescence Bioassay
Purpose of the script: Generating HeatMaps for specific gene lists to compare different CK treatments 

Samples are Arabidopsis thaliana 4-weeks old leaves used for dark-induced senescence bioassay to compare the transcriptional patterns between 11 isoforms of 
cytokinin. 

Base forms: iP, tZ, and DZ. 
N-Glucosides: iP7G, iP9G, tZ7G, tZ9G, DZ7G, and DZ9G 

The experiment was conducted over four different time intervals [2 Hours, 48 Hours, 96 Hours, and 144 Hours] so each treatment will have different four different 
samples e.g. tZ 2 Hours, tZ 48 Hours ... etc. 

Two gene lists have been used in this analysis: 

- FunctionalAnnotation from TAIR

https://www.arabidopsis.org/download/index-auto.jsp?dir=%2Fdownload_files%2FGO_and_PO_Annotations%2FGene_Ontology_Annotations

  GeneLists

- CKGeneList: these are genes involved in the Cytokinin Two-Component Signaling (TCS) Pathway.

  The list was collected from this paper: https://doi.org/10.1016/S1369-5266(03)00087-6.


Gene lists corresponding to each GO term were matched with the datasets, displaying only genes found within those datasets.
Treatments exerting no gene regulation were excluded. 

