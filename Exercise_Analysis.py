import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from VoltAR import VoltammetryExperiment

# File paths
path = r"R:\SteffensenLab\STUDENTS--DO NOT DELETE\JAMES\Lab\Projects\Voluntary Exercise"
tracker_path = r"R:\SteffensenLab\STUDENTS--DO NOT DELETE\JAMES\Lab\Projects\Voluntary Exercise\Data_Tracker.xlsx"

# Gets file paths for each receptor
level_1 = os.listdir(path)
DOR_Path = os.path.join(path,level_1[1])
KOR_Path = os.path.join(path,level_1[2])
MOR_Path = os.path.join(path,level_1[3])

paths = [DOR_Path,MOR_Path,KOR_Path]

def batch_prep_master(paths,verbose=True,norm=True):

    master_sheet_dfs = []
    # Operates on each path
    for path in paths:

        # Creates paths for each receptor
        files = os.listdir(path)
        files = [s for s in files if 'R_' in s]

        file_paths = [os.path.join(path,s) for s in files]

        # Operates on each receptor
        for file in file_paths:

            experiments = os.listdir(file)

            for exp in experiments:

                if exp.find('Thumb') > -1:
                    continue

                current_exp = VoltammetryExperiment(exp,file,tracker_path,3)

                if norm == True:

                    master_sheet_dfs.append(current_exp.norm_df)
                else:
                    master_sheet_dfs.append(current_exp.df)

                if verbose == True:
                    print(exp + ' processed')

    master_sheet = pd.concat(master_sheet_dfs)

    pd.DataFrame.to_clipboard(master_sheet)
    return master_sheet

master_sheet = batch_prep_master(paths)











































