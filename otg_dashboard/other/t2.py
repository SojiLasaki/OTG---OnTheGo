import os
import pandas as pd

# datasets = [maps for maps in os.listdir("../Datasets") if not maps.startswith(".")]
# datasets_capitalized = [folder.capitalize() for folder in datasets]

# print(datasets)
# print(datasets_capitalized)
dataset_folder = "../Datasets" 
datasets = [f for f in os.listdir(dataset_folder) if not f.startswith(".")]


df = pd.read_csv(f"{dataset_folder}/Sebring/Race 1/03_Provisional Results_Race 1_Anonymized.csv")

print(df)