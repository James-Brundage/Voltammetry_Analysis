import pandas as pd
import numpy as np
import seaborn as sns
import os, sys
import matplotlib.pyplot as plt

def import_clean (path):

    df = pd.read_csv(path,sep= '\t')
    df = df[df['File Name'] != 'default.tdms']

    return df

def import_clean_excel (path):

    df = pd.read_excel(path,sep= '\t')
    df = df[df['File Name'] != 'default.tdms']

    return df

# Returns normalized df
def normalize_by_last (df,num):
    df_lst = []
    df_lst.append(df['File Name'])
    df.drop(['File Name','[DAc]'],axis=1,inplace=True)
    means_list = []
    for i in range(10):

        newdf = df.iloc[:,i].copy()

        mean_val = newdf.iloc[len(newdf)-num:len(newdf)].mean()
        means_list.append(mean_val)
        res_df = newdf.apply(lambda x : x/mean_val)
        df_lst.append(res_df)

    final_df = pd.concat(df_lst,axis=1)
    return [final_df, means_list]


def sort_by_drug (df,cont,d1,d2,d3):

    df0 = df[df['File Name'].str.find(cont) > -1].copy()
    df1 = df[df['File Name'].str.find(d1) > -1].copy()
    df2 = df[df['File Name'].str.find(d2) > -1].copy()
    df3 = df[df['File Name'].str.find(d3) > -1].copy()
    lst = [df0, df1, df2,df3]

    return lst

def norm_by_cont (df,cont_lst):
    df_lst = []
    df_lst.append(df['File Name'])
    df.drop(['File Name', '[DAc]'], axis=1, inplace=True)

    for i in range(10):
        newdf = df.iloc[:, i].copy()

        mean_val = cont_lst[i]

        res_df = newdf.apply(lambda x: x / mean_val)

        df_lst.append(res_df)


    final_df = pd.concat(df_lst, axis=1)
    return final_df
# Normalizes individual files by drug name, combines normalize by last and sort_by_drug
def sort_norm (path):

    df = import_clean(path)
    print(df['File Name'])
    print(path)
    cont = input('What is the cont code? ')
    d1 = input('What is the d1 code? ')
    d2 = input('What is the d2 code? ')
    d3 = input('What is the d3 code? ')
    A_num = input('What is the animal number? ')
    BR = input('What is the brain region? ')

    num = int(input('By how many trials do you want to normalize? '))



    lst = sort_by_drug(df,cont,d1,d2,d3)

    means = normalize_by_last(lst[0].copy(),num)[1]

    df_lst = []

    for dfa in lst[:]:

        dfc = norm_by_cont(dfa,means)
        dfc['Animal Number'] = [A_num] * len(dfc)
        dfc['Brain Region'] = [BR] * len(dfc)

        df_lst.append(dfc)

    pd.DataFrame.to_clipboard(pd.concat(df_lst))
    return pd.concat(df_lst)

def sort_norm_excel (path):

    df = import_clean_excel(path)
    # print(df['File Name'])
    # print(path)
    # cont = input('What is the cont code? ')
    # d1 = input('What is the d1 code? ')
    # d2 = input('What is the d2 code? ')
    # d3 = input('What is the d3 code? ')
    # A_num = input('What is the animal number? ')
    # BR = input('What is the brain region? ')
    #
    # num = int(input('By how many trials do you want to normalize? '))

    cont = 'base'
    d1 = 'clon'
    d2 = 'yoh'
    d3 = 'desi'
    A_num = 'x'
    BR = 'BR'
    num = 3

    lst = sort_by_drug(df,cont,d1,d2,d3)

    means = normalize_by_last(lst[0].copy(),num)[1]

    df_lst = []

    for dfa in lst[:]:

        dfc = norm_by_cont(dfa,means)
        dfc['Animal Number'] = [A_num] * len(dfc)
        dfc['Brain Region'] = [BR] * len(dfc)

        df_lst.append(dfc)


    return pd.concat(df_lst)

# Sort_norm on a file containing tsv or excel files
def multiple_file_sort_norm (dir):

    sub = dir + "\\"
    dir = os.listdir(dir)

    cv_paths_lst = []
    xl_paths_lst = []
    for file in dir:
        path = (sub + file)
        if path.find('xlsx') > -1 :
            xl_paths_lst.append(path)

        else :
            cv_paths_lst.append(path)

    norm_df_lst = []
    for path in cv_paths_lst:

        norm_df_lst.append(sort_norm(path))

    for path in xl_paths_lst:

        norm_df_lst.append(sort_norm_excel(path))

    pd.DataFrame.to_clipboard(pd.concat(norm_df_lst,axis=0))
    return pd.concat(norm_df_lst,axis=0)

'''The following functions will be used to help in the psychostimulatns project'''

# Reads in the txt files strucured like brns files (aka weird txt files Jordan named after me)
def read_brn_JYorg (path,plot=False,dr=False):

    if dr == False:

        first_df = pd.read_csv(path, sep='\t', engine='python', header=None, error_bad_lines=False)
        kinetics_df = first_df.loc[0:1]

        time_df = first_df.iloc[2:,0:2]
        time_df.columns = ['Time (s)','Current (nA)']
        time_df.reset_index()
        time_df.drop(2,0,inplace=True)

        if plot == True:

            time_df['Time (s)'] = time_df['Time (s)'].astype(float)
            time_df['Current (nA)'] = time_df['Current (nA)'].astype(float)
            sns.lineplot('Time (s)', 'Current (nA)', data=time_df)
            plt.show()
        return [kinetics_df,time_df]

    else:

        sub = path + "\\"
        lst_dir = os.listdir(path)

        dire = []
        for file in lst_dir:
            if file.find('brn') > -1:
                dire.append(file)

        kin_df_lst = []
        time_df_lst = []
        for file in dire:
            pathb = (sub + file)

            first_df = pd.read_csv(pathb, sep='\t', engine='python', header=None, error_bad_lines=False)
            kinetics_df = first_df.loc[0:1].copy()
            kinetics_df.columns = kinetics_df.iloc[0]
            kinetics_df.drop(0,axis=0,inplace=True)
            kinetics_df['Relational'] = ['file code'] * len(kinetics_df)

            time_df = first_df.iloc[2:, 0:2]
            time_df.columns = ['Time (s)', 'Current (nA)']
            time_df['File Name'] = [file] * len(time_df)
            time_df.reset_index()
            time_df.drop(2, 0, inplace=True)

            if plot == True:
                time_df['Time (s)'] = time_df['Time (s)'].astype(float)
                time_df['Current (nA)'] = time_df['Current (nA)'].astype(float)
                sns.lineplot('Time (s)', 'Current (nA)', data=time_df)
                plt.show()

            kin_df_lst.append(kinetics_df)
            time_df_lst.append(time_df)

        kin_df_con = pd.concat(kin_df_lst,axis=0)
        time_df_con = pd.concat(time_df_lst,axis=0)

        return [kin_df_con,time_df_con]


def add_drug_conc (path):

    flatten = lambda l: [item for sublist in l for item in sublist]
    df = pd.read_csv(path)
    print(df['File Name'])

    n = int(input('How many drugs are there, including control? '))

    name_lst = df['File Name']

    final_lst_names = []
    final_lst_conc = []
    for i in range(n):
        code = input('What is the code? ')
        name = input('What is the name? ')
        conc = input('What is the concentration? ')

        names_lst = []
        conc_lst = []
        for file in name_lst:

            if file.find(code) > -1:
                names_lst.append(name)
                conc_lst.append(conc)

        final_lst_names.append(names_lst)
        final_lst_conc.append(conc_lst)

    final_lst_names = flatten(final_lst_names)
    final_lst_conc = flatten(final_lst_conc)

    df['Drug Applied'] = final_lst_names
    df['Drug Concentration'] = final_lst_conc

    print(df)
    return df







