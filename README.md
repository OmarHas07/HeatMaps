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

### Files Used: 

* Differential expression DZs.xlsx
* Differential expression iP.xlsx
* Differential expression tZ.xlsx

Each of these files contains data for Base form DZ, iP, or tZ and their N-conjugates at the four different time points. 


## Getting Started 

#### Importing required packages 

```
import openpyxl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import product
```

The first step is loading the annotation file, in this walk-through I am going to work with the annotation file from TAIR. 

```
# Make sure your annotation files is in the working directory
Functional_annotation = pd.read_csv('Functional Annotation.csv')
Functional_annotation.columns = ['gene_id, 'GO'] # Adding column names
gene_of_interest = ['chlorophyll catabolic process'] # Change it with whatever you want to compare from the annotation file

# Obtaining just the genes of interests from the annotation file
filtered_annotation = Functional_annotation[Functional_annotation['GO'].isin(gene_of_interest)] # ensure you've got the correct column name.
filtered_gene_ids = filtered_annotation['gene_id'].unique()
filtered_annotation.head(), len(filtered_gene_ids)
```


#### Extracting each DEGs for each treatment from the excel files

This function is made specifically because I have different datasets(comparisons) in the same files but different ex el sheet so I am just extracting each comaprison.



