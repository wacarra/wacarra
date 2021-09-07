#!/usr/bin/env python
# coding: utf-8

# In[121]:


import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
from scipy.stats import chi2
import seaborn as sns


# In[123]:


df = pd.read_csv('data/chicago_crime_data.csv', dtype={'ID': object, 'beat_num': object})
df.head()


# In[9]:


type_loc_cross = pd.crosstab(df["Primary Type"], df["Location Description"])
type_loc_cross.to_html().replace("\n","")


# In[10]:


Locations_dict                     ={
    'Airport & Related' :{
        'AIRCRAFT', 
        'AIRPORT BUILDING NON-TERMINAL - NON-SECURE AREA',
        'AIRPORT BUILDING NON-TERMINAL - SECURE AREA',
        'AIRPORT EXTERIOR - NON-SECURE AREA',
        'AIRPORT EXTERIOR - SECURE AREA', 'AIRPORT PARKING LOT',
        'AIRPORT TERMINAL LOWER LEVEL - NON-SECURE AREA',
        'AIRPORT TERMINAL LOWER LEVEL - SECURE AREA',
        'AIRPORT TERMINAL MEZZANINE - NON-SECURE AREA',
        'AIRPORT TERMINAL UPPER LEVEL - NON-SECURE AREA',
        'AIRPORT TERMINAL UPPER LEVEL - SECURE AREA',
        'AIRPORT TRANSPORTATION SYSTEM (ATS)',
        'AIRPORT VENDING ESTABLISHMENT', 'AIRPORT/AIRCRAFT'
    } ,
    
    'Hospitals & Related':{
        'ANIMAL HOSPITAL', 
        'HOSPITAL BUILDING/GROUNDS', 
        'MEDICAL/DENTAL OFFICE', 
        'NURSING HOME',
        'NURSING HOME/RETIREMENT HOME',
    },
    
    'Residential & Related':{
        'APARTMENT',
        'BASEMENT', 
        'STAIRWELL', 
        'CHA APARTMENT', #Chicago Housing Autority
        'CHA HALLWAY',
        'CHA HALLWAY/STAIRWELL/ELEVATOR',
        'CHA PARKING LOT',
        'CHA PARKING LOT/GROUNDS', 
        'DRIVEWAY - RESIDENTIAL', 
        'PORCH',
        'RESIDENCE',
        'RESIDENCE PORCH/HALLWAY',
        'RESIDENCE-GARAGE',
        'RESIDENTIAL YARD (FRONT/BACK)',  
        'ROOMING HOUSE',
        'GARAGE', 
        'HOTEL/MOTEL',
        'HOUSE',
    },
    
    'Colleges & Related': {
        'SCHOOL, PRIVATE, BUILDING',
        'SCHOOL, PRIVATE, GROUNDS',
        'SCHOOL, PUBLIC, BUILDING',
        'SCHOOL, PUBLIC, GROUNDS', 
        'COLLEGE/UNIVERSITY GROUNDS',
        'COLLEGE/UNIVERSITY RESIDENCE HALL', 
        'DAY CARE CENTER', 
        'SCHOOL YARD',
                         },
    
    'Goverment Buildings & Related':{ 
        'FEDERAL BUILDING',
        'FIRE STATION', 
        'FOREST PRESERVE', 
        'POLICE FACILITY/VEH PARKING LOT',
        'GOVERNMENT BUILDING/PROPERTY', 
        'JAIL / LOCK-UP FACILITY', 
        'LIBRARY',
        'PARK PROPERTY',},
    
    'Liquor Stores & Related':{
        'TAVERN',
        'TAVERN/LIQUOR STORE', 
        'BAR OR TAVERN', 
        'CLUB',  
        'POOL ROOM',
         },
    
    'Stores & Related':{
        'SMALL RETAIL STORE',
        'APPLIANCE STORE',
        'BARBERSHOP', 
        'ATHLETIC CLUB', 
        'BOWLING ALLEY', 
        'CAR WASH', 
        'CLEANING STORE', 
        'COIN OPERATED MACHINE', 
        'COMMERCIAL / BUSINESS OFFICE',
        'CONVENIENCE STORE', 
        'DEPARTMENT STORE', 
        'DRUG STORE', 
        'VESTIBULE',  
        'GAS STATION',
        'GAS STATION DRIVE/PROP.', 
        'RESTAURANT', 
        'GROCERY FOOD STORE', 
        'RETAIL STORE', 
        'MOVIE HOUSE/THEATER', 
        'FACTORY/MANUFACTURING BUILDING',
        'NEWSSTAND',
        'PARKING LOT',},
    
    'Vehicles & Related':{
        'VEHICLE - DELIVERY TRUCK',
        'VEHICLE - OTHER RIDE SERVICE',
        'VEHICLE - OTHER RIDE SHARE SERVICE (E.G., UBER, LYFT)',
        'VEHICLE NON-COMMERCIAL',
        'VEHICLE-COMMERCIAL','TAXICAB', 'AUTO',
        'AUTO / BOAT / RV DEALERSHIP','BOAT/WATERCRAFT', 'GANGWAY', 'OTHER COMMERCIAL TRANSPORTATION',
        
        
    }, 
    
    'Public Transport & Related':{
        'CTA "L" PLATFORM',
        'CTA BUS',
        'CTA BUS STOP',
        'CTA GARAGE / OTHER PROPERTY',
        'CTA PLATFORM',
        'CTA PROPERTY',
        'CTA STATION',
        'CTA TRACKS - RIGHT OF WAY',
        'CTA TRAIN', 'OTHER RAILROAD PROP / TRAIN DEPOT',

                    },
    
    'Street & Related': {
        'ALLEY', 
        'BRIDGE', 
        'CEMETARY',
        'CHURCH',
        'CHURCH/SYNAGOGUE/PLACE OF WORSHIP', 
        'CONSTRUCTION SITE', 
        'DRIVEWAY', 
        'YARD', 
        'VACANT LOT',
        'VACANT LOT/LAND', 
        'SIDEWALK', 
        'PARKING LOT/GARAGE(NON.RESID.)', 
        'ABANDONED BUILDING', 
        'STREET', 
        'HIGHWAY/EXPRESSWAY',  
        'HALLWAY',
        'LAKEFRONT/WATERFRONT/RIVERBANK', 
        'SPORTS ARENA/STADIUM'    
        
    },
    
    'Bank & Related':{
        'BANK',
        'ATM (AUTOMATIC TELLER MACHINE)', 
        'CREDIT UNION', 
        'CURRENCY EXCHANGE', 
        'RIVER BANK',
        'SAVINGS AND LOAN', 
        'PAWN SHOP', 
        'WAREHOUSE'},
    
    'Other Locations':{'OTHER', }
    
}


Offenses_dict={
    'Theft Related': {
        'BURGLARY', 
        'THEFT',
        'CRIMINAL TRESPASS', 
        'MOTOR VEHICLE THEFT', 
        'ROBBERY',
        },
    
    'Property Damage': {
        'CRIMINAL DAMAGE', 
        'ARSON', 
        },

    'Violence & Related' :{
        'BATTERY',
        'ASSAULT',
        'KIDNAPPING',   
        'HOMICIDE', 
        },
    
    'Sexual Offenses & Related':{
        'CRIM SEXUAL ASSAULT',
        'SEX OFFENSE',
        'OBSCENITY',
        'HUMAN TRAFFICKING', 
        'PROSTITUTION',
        'PUBLIC INDECENCY',
        'STALKING',
        'OFFENSE INVOLVING CHILDREN'},
    
    'Dangerous practices':{ 
        'DECEPTIVE PRACTICE', 
        'WEAPONS VIOLATION',
        'INTIMIDATION',
        'CONCEALED CARRY LICENSE VIOLATION',
        'INTERFERENCE WITH PUBLIC OFFICER'},
    
    'Substances & Related':{
        'NARCOTICS',
        'OTHER NARCOTIC VIOLATION',
        'GAMBLING', 
        'LIQUOR LAW VIOLATION'},
    
    'Other Offenses':{
        'PUBLIC PEACE VIOLATION'
        'NON-CRIMINAL',
        'OTHER OFFENSE',
        'NON-CRIMINAL (SUBJECT SPECIFIED)' }}


# In[13]:


for key in Locations_dict.keys():
    print(key)


# In[14]:


for key in Offenses_dict.keys():
    print(key)


# In[16]:


#Here is one possible answer.

#Let us reverse the keys/values of our dictionary.
dict_Locations=dict()
for key in Locations_dict.keys():
    for value in Locations_dict[key]:
        dict_Locations[value]=key

dict_Offenses=dict()
for key in Offenses_dict.keys():
    for value in Offenses_dict[key]:
        dict_Offenses[value]=key

#Then, we use the new dicts to create new columns the in the data frame.
df["Offenses_cat"]=df["Primary Type"].map(dict_Offenses)
df["Location_cat"]=df["Location Description"].map(dict_Locations)

#Finally, we create the contingency table.
Offense_Location_cross = pd.crosstab(df["Offenses_cat"], df["Location_cat"])
Offense_Location_cross.to_html().replace("\n","")


# In[35]:


Offense_Location_prop = (pd.crosstab(df["Offenses_cat"], df["Location_cat"], normalize="index")*100).round(2)
Offense_Location_prop = Offense_Location_prop.sort_values(by=["Residential & Related","Street & Related"], ascending=False)
Offense_Location_prop.to_html().replace("\n","")


# In[42]:


ax = sns.heatmap(Offense_Location_prop, cmap="Reds", cbar_kws={"label":"% of offenses of each type in that location"})
ax.set_title("Primary type vs. Location description")
plt.show()


# In[46]:


Location_Offense_prop = (pd.crosstab(df["Offenses_cat"], df["Location_cat"], normalize="columns")*100).round(2)
Location_Offense_prop = Location_Offense_prop.T.sort_values(by=["Theft Related","Violence & Related"], ascending=False)

ax = sns.heatmap(Location_Offense_prop.T, cmap="Reds", cbar_kws={"label":"% of offenses in each location that were of this primary type"})
ax.set_title("Primary type vs. Location description")
plt.show()


# In[56]:


off_ft = df["Offenses_cat"].value_counts()/len(df["Offenses_cat"])
off_ft


# In[55]:


loc_ft = df["Location_cat"].value_counts()/len(df["Location_cat"])
loc_ft


# In[81]:


mult_list = []
for indexo in off_ft.index:
    for indexl in loc_ft.index:
        mult = off_ft.loc[indexo] * loc_ft.loc[indexl]
        mult_list.append([indexl, indexo, mult])
        
null_ct = (pd.DataFrame(mult_list).pivot(index=0,columns=1,values=2)*267178).astype(int)
null_ct.columns = null_ct.columns.rename("")
null_ct.index = null_ct.index.rename("")
null_ct#.to_html().replace("\n","")


# In[83]:


ax = sns.heatmap(null_ct, cmap="Reds", cbar_kws={"label":"Count of offenses"})
ax.set_title("Primary type vs. Location description under the null hypothesis")
plt.show()


# In[87]:


null_ct


# In[94]:


# Normalizing by location
null_ct_location = null_ct.copy()
for col in null_ct.columns:
    null_ct_location[col] = 100*null_ct_location[col] / null_ct.sum(axis="columns")
    
ax = sns.heatmap(null_ct_location, cmap="Reds", cbar_kws={"label":"% of offenses in this location\n that are of this type"})
ax.set_title("Primary type vs. Location description under the null hypothesis")
plt.show()


# In[97]:


null_ct.sum(axis="index")


# In[102]:


# Normalizing by type
null_ct_type = null_ct.copy()
for col in null_ct.columns:
    null_ct_type[col] = 100*null_ct_type[col] / null_ct_type[col].sum()
    
ax = sns.heatmap(null_ct_type, cmap="Reds", cbar_kws={"label":"% of offenses of this type\n that happened in this location"})
ax.set_title("Primary type vs. Location description under the null hypothesis")
plt.show()


# In[105]:


primary_location_cross = pd.crosstab(df['Location_cat'], df['Offenses_cat'])
g, p, dof, expctd = chi2_contingency(primary_location_cross)
print("p-value of Chi-square test for Primary Type vs. Location (both grouped) =", p)
g, p, dof, expctd


# In[108]:


#First, we filter our data to include only violent offences that took place around residential areas.

df4=df[df['Location_cat'].isin({'Residential & Related'})]
df4=df4[df4['Offenses_cat']=='Violence & Related']
#type_loc_cross4 = pd.crosstab(df4["Location Description"],df4["Primary Type"]).apply(lambda r: r/r.sum()*100, axis=0)
type_loc_cross4 = pd.crosstab(df4["Location Description"],df4["Primary Type"])
type_loc_cross4.to_html().replace("\n","")


# In[107]:


g, p, dof, expctd = chi2_contingency(type_loc_cross4)
print("p-value of Chi-square test for Violence & Related Offenses vs. Residential & Related Locations =", p)


# In[113]:


# discretize time
df["date_py"] = pd.to_datetime(df.Date)
df["day_of_week"] = df.date_py.dt.dayofweek
type_dow_cross = pd.crosstab(df['Primary Type'], df['day_of_week'], normalize="index")
type_dow_cross


# In[118]:


plt.figure(figsize=(10,10))
ax = sns.heatmap(type_dow_cross*100, cmap="Reds", cbar_kws={"label":"% offenses in each weekday that belong to this type"})
ax.set_title("Primary type vs. day of the week")
plt.show()


# In[120]:


type_dow_cross_counts = pd.crosstab(df['Primary Type'], df['day_of_week'])
g, p, dof, expctd = chi2_contingency(type_dow_cross_counts)
print("p-value of Chi-square test for Primary Type vs. Day of week =", p)

