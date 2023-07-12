import openpyxl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import product

### Load the genes Cytokinin related genes
#CK_Genes = pd.read_csv('/Users/omarhasannin/Library/CloudStorage/OneDrive-AuburnUniversity/AT DATA/RNA-Seq Data/Gene Ontology Analysis/CKGenes.csv')

# Create a dictionary mapping gene IDs to gene names
#gene_id_to_name = CK_Genes.set_index('GeneIDs')['Gene Name'].to_dict()

# Get a list of all unique gene IDs
#filtered_gene_ids = CK_Genes['GeneIDs'].unique()

# Loading gene IDs for leaf senescence from the annotation file

Functional_annotation = pd.read_csv('FunctionalAnnotation.csv')
Functional_annotation.columns = ['gene_id', 'GO']
gene_of_interest = ['response to jasmonic acid']
filtered_annotation = Functional_annotation[Functional_annotation['GO'].isin(gene_of_interest)]
filtered_gene_ids = filtered_annotation['gene_id'].unique()
filtered_annotation.head(), len(filtered_gene_ids)




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
        if data.empty:
            continue

        # Add the DataFrame to the dictionary
        data_dict[(condition, time_point)] = data

    return data_dict


# Process the first file again
data_dict_DZ = process_file("/Users/omarhasannin/Library/CloudStorage/OneDrive-AuburnUniversity/AT DATA/RNA-Seq Data/Gene Ontology Analysis/Differential expression DZs.xlsx")

(data_dict_DZ)  # Display the data for inspection

# Process the second file
data_dict_iP = process_file("/Users/omarhasannin/Library/CloudStorage/OneDrive-AuburnUniversity/AT DATA/RNA-Seq Data/Gene Ontology Analysis/Differential expression iP.xlsx")

data_dict_iP  # Display the data for inspection


# Process the second file
data_dict_tZ = process_file("/Users/omarhasannin/Library/CloudStorage/OneDrive-AuburnUniversity/AT DATA/RNA-Seq Data/Gene Ontology Analysis/Differential expression tZ.xlsx")

data_dict_tZ

# Define a function to filter and prepare DataFrame for heatmap
def prepare_data_for_heatmap(data_dict, gene_sets):
    heatmap_data = []
    all_conditions_timepoints = []

    # Iterate over each dataset in the data dictionary
    for (cytokinin, timepoint), df in data_dict.items():
        # Filter the DataFrame based on the genes of interest
        df_filtered = df[df['gene_id'].isin(gene_sets)]

        # Iterate over each row in the filtered DataFrame
        for _, row in df_filtered.iterrows():
            # Extract the log2 fold change
            fold_change_column = [col for col in df.columns if 'log2FoldChange' in col][0]
            log2_fold_change = row[fold_change_column]

            # Append the data to the heatmap data list
            heatmap_data.append([cytokinin, timepoint, row['gene_id'], log2_fold_change])

        # Add the current condition and timepoint to the list
        all_conditions_timepoints.append((cytokinin, timepoint))

    # Convert the heatmap data list to a DataFrame
    df_heatmap = pd.DataFrame(heatmap_data, columns=['Cytokinin', 'Timepoint', 'Gene', 'log2FoldChange'])

    # Create a DataFrame with all possible combinations of treatments and genes
    all_combinations = pd.DataFrame(list(product(all_conditions_timepoints, gene_sets)),
                                    columns=['Condition_Timepoint', 'Gene'])
    all_combinations[['Cytokinin', 'Timepoint']] = pd.DataFrame(all_combinations['Condition_Timepoint'].tolist(),
                                                                index=all_combinations.index)
    all_combinations.drop(columns=['Condition_Timepoint'], inplace=True)

    return df_heatmap, all_combinations

# Prepare the data for the heatmap
heatmap_data_DZ, all_combinations_DZ = prepare_data_for_heatmap(data_dict_DZ, filtered_gene_ids)
heatmap_data_iP, all_combinations_iP = prepare_data_for_heatmap(data_dict_iP, filtered_gene_ids)
heatmap_data_tZ, all_combinations_tZ = prepare_data_for_heatmap(data_dict_tZ, filtered_gene_ids)


# Concatenate all the dataframes into a single one
heatmap_data = pd.concat([heatmap_data_DZ, heatmap_data_iP, heatmap_data_tZ])
all_combinations = pd.concat([all_combinations_DZ, all_combinations_iP, all_combinations_tZ])

# Merge the heatmap data with the dataframe containing all combinations
heatmap_data_full = pd.merge(all_combinations, heatmap_data, how='left',
                             on=['Cytokinin', 'Timepoint', 'Gene'])

# Replace gene IDs with gene names
#heatmap_data_full['Gene'] = heatmap_data_full['Gene'].map(filtered_gene_ids)

# Pivot the DataFrame to get the required format for the heatmap
heatmap_df = heatmap_data_full.pivot_table(index='Gene', columns=['Cytokinin', 'Timepoint'],
                                           values='log2FoldChange')

# Get the actual column order in the DataFrame
actual_columns = heatmap_df.columns.tolist()

# Define the desired general order
general_order = [
    "DZ", "DZ7G", "DZ9G", "iP", "iP7G", "iP9G", "tZ", "tZ7G", "tZ9G"
]

# Define the desired timepoint order
timepoint_order = ["2 Hours", "48 Hours", "96 Hours", "144 Hours"]

# Create a new column order based on the general order but only including actual columns
new_column_order = []
for cytokinin in general_order:
    for timepoint in timepoint_order:
        column = (cytokinin, timepoint)
        if column in actual_columns:
            new_column_order.append(column)

# Reorder the columns based on the new column order
heatmap_df_ordered = heatmap_df[new_column_order]

# Create a heatmap
plt.figure(figsize=(20, 13))
sns.heatmap(heatmap_df_ordered, cmap="vlag", center=0, linewidths=.5)
plt.title("Log2 Fold Change of Gene Expressions")
plt.show()




# Extract the dataframe for "tZ 2 Hours"
df_tZ_2Hours = data_dict_tZ.get(('tZ', '2 Hours'))

if df_tZ_2Hours is not None:
    # Check if 'log2FoldChange' is in column names
    fold_change_columns = [col for col in df_tZ_2Hours.columns if 'log2FoldChange' in col]

    if not fold_change_columns:  # if the list is empty
        print("No 'log2FoldChange' column in 'tZ 2 Hours' dataframe.")
    else:
        # Filter the DataFrame based on the genes of interest
        df_filtered = df_tZ_2Hours[df_tZ_2Hours['gene_id'].isin(filtered_gene_ids)]

        # Display the first few rows of the filtered dataframe
        print(df_filtered.head())
else:
    print("No data for 'tZ 2 Hours'.")
