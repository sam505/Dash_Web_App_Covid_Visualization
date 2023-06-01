from sodapy import Socrata
import os
import pandas as pd
import logging


logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

client = Socrata("data.cdc.gov", None)

def download(data_id, name):
    if not os.path.isdir("data"):
        logger.info("Creating data directory")
        os.mkdir("data")
    logger.info(f"Fetching {name}.csv...")
    df = pd.from_records(client.get(data_id))
    df.to_csv(f"{name}.csv")
    logger.info(f"{name}.csv downloaded and saved")
    return df
