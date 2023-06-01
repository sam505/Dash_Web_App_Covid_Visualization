from sodapy import Socrata
import os
import pandas as pd

client = Socrata("data.cdc.gov", None)

def download(data_id, name):
    if not os.path.isdir("data"):
        os.mkdir("data")

    df = pd.from_records(client.get(data_id))
    df.to_csv(f"{name}.csv")
    return df
