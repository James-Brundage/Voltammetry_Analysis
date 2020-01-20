import pandas as pd
import numpy as np
import seaborn as sns
import os, sys
from Voltammetry_Analysis_Funcs import import_clean,import_clean_excel,normalize_by_last,sort_norm,sort_norm_excel,multiple_file_sort_norm, norm_by_cont
import matplotlib.pyplot as plt

dir = r"R:\SteffensenLab\STUDENTS--DO NOT DELETE\JAMES\Lab\Projects\Central Amygdala\New folder"

sort_norm(r"R:\SteffensenLab\VOLTAMMETRY DATA--DO NOT DELETE\Altar 3 - ExVivo Rig 1\m1234\m1234.tsv")


