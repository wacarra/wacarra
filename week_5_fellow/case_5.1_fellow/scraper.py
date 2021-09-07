import pandas as pd
import random
import numpy as np

filenames = pd.read_csv("data/filenames.csv", header=None)[0].str.strip()
prefix = "https://cycling.data.tfl.gov.uk/usage-stats/"

df_list = []
for filen in filenames:
    url = prefix + filen
    df_list.append(
        pd.read_csv(url).drop(columns=["EndStation Name", "StartStation Name"])
    )
    print("Done " + filen)

df = pd.concat(df_list)
print("Dataframe concatenated")
# Adding tags
options = [
    "priority low",
    "Priority low",
    "priority_high",
    "priority_medium",
    "priority Medium",
]
df["tag"] = df["Bike Id"].apply(lambda x: random.choice(options))  # Adding the tags
print("Tags added")
# Adding user category
options = ["A", "B"]
df["userCategory"] = df["Bike Id"].apply(
    lambda x: np.random.choice(options, 1, replace=True, p=[0.8, 0.2])
)
print("User category added")
# Adding 68 duplicate rows
df = pd.concat([df, df.sample(68)]).reset_index()
print("Duplicates added")
# Adding NaNs (removing random cells)
drop_indices = []
for i in range(0, 1250):
    drop_indices.append(random.choice(df.index))
    i = i + 1
drop_indices = list(set(drop_indices))
df["Bike Id"] = df["Bike Id"].drop(drop_indices)
print("Bike Id NULLS added")
drop_indices = []
for i in range(0, 987):
    drop_indices.append(random.choice(df.index))
    i = i + 1
drop_indices = list(set(drop_indices))
df["userCategory"] = df["userCategory"].drop(drop_indices)
print("userCategory NULLS added")
drop_indices = []
for i in range(0, 1250):
    drop_indices.append(random.choice(df.index))
    i = i + 1
drop_indices = list(set(drop_indices))
drop_indices = np.random.choice(df.index, 7898, replace=False)
df["EndStation Id"] = df["EndStation Id"].drop(drop_indices)
print("EndStation Id NULLs added")
df = df.drop(columns=["index"])
df.to_csv("data/trips.csv", index=False)
