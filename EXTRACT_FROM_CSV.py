import pandas as pd
import glob
import os

# chose the path to the directory containing the CSV files
path = '/Users/                                                             /Downloads/t1.5/'

all_files = glob.glob(os.path.join(path, "*.csv"))
hepes_files = []
non_hepes_files = []   # Aβ containing( which belong Alzheimer induced animals)

# Iterate over each CSV file
for file in all_files:
    file_name = os.path.basename(file)
    if 'HEPES' in file_name: #our animal code names had hepes words in it & it could be change
        hepes_df = pd.read_csv(file)
        # Calculate cumulative sum of "Distance_cm" column
        hepes_df['Cumulative Distance_cm'] = hepes_df['Distance_cm'].cumsum()
        total_distance = hepes_df['Distance_cm'].sum()
        hepes_files.append((file_name, hepes_df, total_distance))
    else:
        non_hepes_df = pd.read_csv(file)
        # Calculate cumulative sum of "Distance_cm" column
        non_hepes_df['Cumulative Distance_cm'] = non_hepes_df['Distance_cm'].cumsum()
        total_distance = non_hepes_df['Distance_cm'].sum()
        non_hepes_files.append((file_name, non_hepes_df, total_distance))

# then count the true values for object1 and object2 in each HEPES file
hepes_counts = {}
for file_name, df, total_distance in hepes_files:
    true_count_object1 = df['object1'].eq(True).sum()
    true_count_object2 = df['object2'].eq(True).sum()
    differences= (true_count_object1 - true_count_object2)
    Exploration= (true_count_object1 + true_count_object2)
    d2= differences/Exploration
    d3= true_count_object2 = (df['object2'].eq(True).sum()/Exploration)*100
    hepes_counts[file_name] = {'object1': true_count_object1, 'object2': true_count_object2,
                               'total_distance': total_distance,
                               'differences': differences, 'Exploration': Exploration, 'd2': d2, 'd3': d3}

# repeat the count the true values for object1 and object2 in each non-HEPES file
non_hepes_counts = {}
for file_name, df, total_distance in non_hepes_files:
    true_count_object1 = df['object1'].eq(True).sum()
    true_count_object2 = df['object2'].eq(True).sum()
    differences= (true_count_object1 - true_count_object2)
    Exploration= (true_count_object1 + true_count_object2)
    d2= differences/Exploration
    d3= true_count_object2 = (df['object2'].eq(True).sum()/Exploration)*100
    non_hepes_counts[file_name] = {'object1': true_count_object1, 'object2': true_count_object2,
                               'total_distance': total_distance,
                               'differences': differences, 'Exploration': Exploration, 'd2': d2, 'd3': d3}

# make an Excel writer
excel_file = 't1.5.xlsx'
writer = pd.ExcelWriter(excel_file)

# save HEPES counts in a sheet
hepes_counts_df = pd.DataFrame(hepes_counts).T
hepes_counts_df.index.name = 'CSV File'
hepes_counts_df.to_excel(writer, sheet_name='HEPES Counts')

# save non-HEPES counts in a sheet
non_hepes_counts_df = pd.DataFrame(non_hepes_counts).T
non_hepes_counts_df.index.name = 'CSV File'
non_hepes_counts_df.to_excel(writer, sheet_name='Non-HEPES Counts')

# finally you should save and close the Excel writer
writer.save()
writer.close()

