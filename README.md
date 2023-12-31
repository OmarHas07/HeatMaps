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


#### Extracting DEG lists for each treatment from the Excel files

This function is made specifically because I have different datasets(comparisons) in the same files but different Excel sheets so I am just extracting each comparison.

You don't have to do it if you have your DEG lists in separate files. 

```
def process_file(file_path):
    # Load the Excel file
    workbook = openpyxl.load_workbook(file_path, read_only=True)

    # Get the names of all the sheets in the file
    sheet_names = workbook.sheetnames

    # Create a dictionary to hold the data from each sheet
    data_dict = {}

    # Process each sheet
    for sheet_name in sheet_names:
        # Get the condition and time point from the sheet name
        parts = sheet_name.split(" ")
        condition = parts[0]
        time_point = " ".join(parts[1:])  # Join the second and third parts to form the time point

        # Load the sheet into a DataFrame
        data = pd.read_excel(file_path, sheet_name=sheet_name)

        # Skip empty sheets
        if data.empty: # this is because I have some empty DEG lists 
            continue

        # Add the DataFrame to the dictionary
        data_dict[(condition, time_point)] = data

    return data_dict
```

#### In case your data files are separate 

Alternatively, if your data files are separate you can use the below code to import your data. 

```
filename = pd.read_csv(path_to_file)
```


Now that we established the function we can start importing the data

```
data_dict_DZ = process_file("/Users/omarhasannin/Library/CloudStorage/OneDrive-AuburnUniversity/AT DATA/RNA-Seq Data/Gene Ontology Analysis/Differential expression DZs.xlsx")

(data_dict_DZ)  # Display the data for inspection

# Process the second file: iP treatmetns
data_dict_iP = process_file("/Users/omarhasannin/Library/CloudStorage/OneDrive-AuburnUniversity/AT DATA/RNA-Seq Data/Gene Ontology Analysis/Differential expression iP.xlsx")

data_dict_iP  # Display the data for inspection


# Process the second file: tZ treatments
data_dict_tZ = process_file("/Users/omarhasannin/Library/CloudStorage/OneDrive-AuburnUniversity/AT DATA/RNA-Seq Data/Gene Ontology Analysis/Differential expression tZ.xlsx")

data_dict_tZ
```

#### In case your data files are separate 

Alternatively, if your data files are separate you can use the below code to import your data. 

```
filename = pd.read_csv(path_to_file)
```

## Preparing Data for HeatMap


```
def prepare_data_for_heatmap(data_dict, gene_sets)
  for (cytokinin, timepoint), df in data_dict.items()
    df_filtered = df[df'gene_id'].isin(gene_sets)]
    for _, row in filtered_df.iterrows():
      fold_change_column = [col for col in df.columns if log2FoldChange' in col][0]


