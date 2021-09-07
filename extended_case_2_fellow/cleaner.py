import os
import pandas as pd
import glob
import datetime


os.system("wget -i urls.txt")
all_files = glob.glob("*.gz")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
    #os.system("rm " + filename)

df = pd.concat(li, axis=0, ignore_index=True)

df = df.drop(columns=["YEAR", "MONTH_NAME", "BEGIN_TIME", "END_TIME", "BEGIN_DAY", "END_DAY", "BEGIN_YEARMONTH", "END_YEARMONTH", "BEGIN_RANGE", "BEGIN_AZIMUTH", "EPISODE_NARRATIVE", "EVENT_NARRATIVE", "DATA_SOURCE"])

df["BEGIN_DATE_TIME"] = pd.to_datetime(df["BEGIN_DATE_TIME"], errors="coerce", format="%d-%b-%y %H:%M:%S")
df["END_DATE_TIME"] = pd.to_datetime(df["END_DATE_TIME"], errors="coerce", format="%d-%b-%y %H:%M:%S")

# Basic cleaning
df["EVENT_TYPE"] = df["EVENT_TYPE"].str.lower().str.replace("/"," ").str.replace("  "," ").str.strip()

#### Label merging

# Merging all thunderstorm winds
keys_thunder = ["thunderstorm wind trees", "thunderstorm winds", "thunderstorm wind tree",
             "thunderstorm winds flood", "thunderstorm winds flash flood","thunderstorm winds flooding",
             "thunderstorm heavy rain", "thunderstorm winds heavy rain", "thunderstorm winds lightning",
             "thunderstorm winds funnel clou"]

replace_dict_thunder = dict()
for key in keys_thunder:
    replace_dict_thunder[key] = "thunderstorm wind"

df["EVENT_TYPE"] = df["EVENT_TYPE"].replace(replace_dict_thunder)

# Merging hurricanes
df["EVENT_TYPE"] = df["EVENT_TYPE"].replace({"marine hurricane typhoon":"hurricane", "hurricane (typhoon)":"hurricane"})

# Merging volcanic ashfall
df["EVENT_TYPE"] = df["EVENT_TYPE"].replace({"volcanic ash":"volcanic ashfall"})

# Feature engineering
def adjust_damage(value):
    """
    Convert from millions or thousands of dollars, etc., to dollars.
    
    Input:
    `value`: An object that can be None, a number, or a
    string of the form "xxK", where "xx" is a number or an empty string (ie. a value can be
    "28K" or often simply "K"), and "K" is a literal multiplier. Multipliers can be
    either "H"/"h" (hundreds), "K"/"T"/"k" (thousands), "M" (millions), or "B" (billions).
    See examples below.
    
    Output:
    `adjusted`: A float (None for null values of `value` or when it is an empty string)
    See examples below.
    
    Note:
    Some values have question marks (?) as their multipliers. Treat those as if they were
    nulls.
    
    Examples:
    "0.5K" should become 500.0
    "K" should become 1000.0
    "2B" should become 2000000000.0
    "1.3H" should become 130
    "750" should become 750
    "0?" should beocome `None`
    `None` should stay being `None`
    "" should become `None`
    
    """
    
    if value == None:
        pass
    else:
        value = str(value) # Make value a string
      
    if value == None:
        adjusted = None # If input is null, output is null
    elif value == "": # If input is an empty string, output is null
        adjusted = None
    elif value[-1] in ["H","h","K","T","k","M","B","?"]: # If string has a literal multiplier
        if value[:-1] == "": # If the multiplier is alone, attach a 1
            value = "1" + value
        # Do the multiplications
        if value[-1] in ["H", "h"]:
            adjusted = float(value[:-1]) * 100
        elif value[-1] in ["K", "T", "k"]:
            adjusted = float(value[:-1]) * 1000
        elif value[-1] == "M":
            adjusted = float(value[:-1]) * 1000000
        elif value[-1] == "B":
            adjusted = float(value[:-1]) * 1000000000
        elif value[-1] == "?":
            adjusted = None
    else:
        adjusted = float(value) # If value is a number, just make it a float
    
    return adjusted
    
df["DAMAGE_PROPERTY"] = df["DAMAGE_PROPERTY"].apply(adjust_damage)
df["DAMAGE_CROPS"] = df["DAMAGE_CROPS"].apply(adjust_damage)

# Replacing nulls with zeroes
cols = ["DEATHS_DIRECT","DEATHS_INDIRECT","INJURIES_DIRECT","INJURIES_INDIRECT","DAMAGE_CROPS","DAMAGE_PROPERTY"]
df[cols] = df[cols].fillna(0)

# Creating the columns
df["TOTAL_DEATHS"] = df["DEATHS_DIRECT"] + df["DEATHS_INDIRECT"]
df["TOTAL_INJURIES"] = df["INJURIES_DIRECT"] + df["INJURIES_INDIRECT"]
df["TOTAL_DAMAGE"] = df["DAMAGE_PROPERTY"] + df["DAMAGE_CROPS"]

cpi = pd.read_csv("data/cpi.csv")

df["BEGIN_DATE_TIME"] = pd.to_datetime(df["BEGIN_DATE_TIME"])
df["BEGIN_YEAR"] = df["BEGIN_DATE_TIME"].dt.year
df["cpi"] = pd.merge(df.copy(), cpi, right_on="year", left_on="BEGIN_YEAR", how="left")["cpi"]/100
df["TOTAL_DAMAGE_DEFLATED"] = df["TOTAL_DAMAGE"]/df["cpi"]

df = df[
    'EPISODE_ID', 'EVENT_ID', 'STATE', 'EVENT_TYPE', 'BEGIN_DATE_TIME', 'BEGIN_YEAR',
       'CZ_TIMEZONE', 'END_DATE_TIME', 'TOR_F_SCALE', 'BEGIN_LOCATION', 'END_LOCATION', 'BEGIN_LAT',
       'BEGIN_LON', 'END_LAT', 'END_LON', 'TOTAL_DEATHS', 'TOTAL_INJURIES', 'TOTAL_DAMAGE_DEFLATED'
]

df.to_csv("data/dataset.csv.gz", index=False)
