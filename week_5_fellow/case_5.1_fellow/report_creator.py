import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv("data/trips.csv")
profile = ProfileReport(df, title="Trips", explorative=True)
profile.to_file("data/trips_report.html")
