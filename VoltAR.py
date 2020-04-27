import numpy as np
import pandas as pd
import os


class VoltammetryExperiment:
    '''Exercise experiment information is stored this way and can be called '''

    def __init__(self, exp, file, tracker, norm):
        '''Initialize path attributes'''
        self.path = os.path.join(file, exp)
        self.search_term = exp
        self.tracker_path = tracker
        self.df = self.add_condition()
        self.norm = norm
        self.ctrl_df = self.dfs_lst()[0]
        self.D1_df = self.dfs_lst()[1]
        self.D2_df = self.dfs_lst()[2]
        self.D3_df = self.dfs_lst()[3]
        self.norm_ctrl_df = self.normalize_dfs()[0]
        self.norm_D1_df = self.normalize_dfs()[1]
        self.norm_D2_df = self.normalize_dfs()[2]
        self.norm_D3_df = self.normalize_dfs()[3]
        self.norm_df = self.normalize_dfs()[4]
        self.condition = self.conditions()
        self.norm_df = self.norm_whole_df()

    '''Imports the experimental dataframe based on the right file type'''

    def exp_df(self):

        '''Calls necessary terms from class'''
        experiment_path = self.path

        '''Imports correct file based on tsv or excel'''
        if experiment_path.find('tsv') > -1:
            df = pd.read_csv(experiment_path, sep='\t')

        elif experiment_path.find('xl') > -1:
            df = pd.read_excel(experiment_path)

        return df

    '''Generates a list of codes from the tracker for the animal number used for sorting'''

    def codes(self):

        '''Gets necessary terms from class, imports tracker df'''
        exp = self.search_term
        tracker = pd.read_excel(self.tracker_path)

        '''Locates correct animal in tracker df'''
        exp_search = exp.split('.')[0]
        df_t = tracker[tracker['Animal Number'] == exp_search]

        tracker_cols = list(df_t.columns)[6:12]

        # Create list of keys
        code_lst = []
        for i in range(0, len(tracker_cols)):
            code = list(df_t[tracker_cols[i]].values)

            code_lst.append(code[0])

        return code_lst

    '''Finds the condition of the experiment from the tracker'''

    def conditions(self):

        exp = self.search_term
        tracker = pd.read_excel(self.tracker_path)

        '''Locates correct animal in tracker df'''
        exp_search = exp.split('.')[0]
        df_t = tracker[tracker['Animal Number'] == exp_search].copy()

        df_t['Condition'] = df_t['Receptor'] + ' ' + df_t['Group']

        return df_t['Condition'].iloc[0]

    '''Creates a list of Dfs sorted by the drug applied. Ctrl is index0, drug application is in order'''

    def dfs_lst(self):

        exp_df = self.exp_df()
        codes_lst = self.codes()

        dfs_lst = []
        for i in range(0, 4):
            df = exp_df[(exp_df['File Name'].str.find(str(codes_lst[i])) > -1) & (exp_df['File Name'].str.find(str(codes_lst[4])) > -1) ]
            dfs_lst.append(df)

        return dfs_lst

    '''Adds Conditions'''
    def add_condition (self):

        dfs_lst = self.dfs_lst()
        condis = self.conditions()

        final_lst = []

        for df in dfs_lst:
            df['Conditions'] = [condis]*len(df)
            final_lst.append(df)

        final_df = pd.concat(final_lst)

        return final_df

    '''Creates a np array of the terms used for normalization for each measure, except [DAc], which is always inf.'''
    def norm_terms(self):

        term = int(self.norm)
        df = self.ctrl_df

        means_array = df[-term:].drop(['File Name', '[DAc]'], axis=1).copy().describe().iloc[1]

        return means_array

    '''Creates list of normalized dfs for each drug normalized to the control, last item is the concatenated list'''
    def normalize_dfs(self):

        dfs_lst = self.dfs_lst()
        norm_arr = self.norm_terms()

        final_lst = []
        for i in range(0, len(dfs_lst)):
            df = dfs_lst[i]
            names = df['File Name']
            df = df.drop(['File Name', '[DAc]'], axis=1)
            df_n = df / norm_arr

            df_n['File Name'] = names
            df_n = df_n.set_index('File Name').reset_index()
            final_lst.append(df_n)

        concat = pd.concat(final_lst)
        final_lst.append(concat)
        return final_lst

    '''Returns normalized dataframe'''
    def norm_whole_df (self):

        df = self.df
        norm_arr = self.norm_terms()

        names = df['File Name']
        condis = df['Conditions']
        df = df.drop(['File Name', '[DAc]','Conditions'], axis=1)
        df_n = df / norm_arr

        df_n['File Name'] = names
        df_n['Conditions'] = condis
        df_n = df_n.set_index('File Name').reset_index()

        return df_n










