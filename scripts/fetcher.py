
from google.transit import gtfs_realtime_pb2 as pb2
from datetime import datetime   

import os
import time
import polars as pl 
from pathlib import Path
from urllib import request

from src.parse import GTFSEntity
from src.load import upsert_pq_to_db

FREQUENCY_SEC = 30  # in seconds
DURATION_MIN = 30  # in minutes 

URL = "https://gtfsrt.api.translink.com.au/api/realtime/SEQ/" 
DATA = "VehiclePositions"

# TODO Lots of failure scenarios to be handled. 
# TODO 1. Break it downn into smaller functionalities and use an orchestrator. 
# TODO 2. Add logging. 
# TODO 3. Use an async fetching to get faster download of file?
# TODO 4. Parallel processing ? 
# TODO 5. Use faster file formats for the raw data. 
# TODO 6. How to handle schema evolution.
# TODO 7. How to handle missing values in the data.
# TODO 8. How to handle duplicates in the data.
# TODO 9. How to handle the state. Use a message broker? 
# TODO 10. How to handle backpressure? and ingest into DB. 

def fetch_and_load(url: str) -> pb2.FeedMessage:
    """Fetch the GTFS VechilePositions DATA from the url and return the feed message every FREQUENCY_SEC seconds for DURATION_MIN mins"""

    for _ in range(DURATION_MIN * 60 // FREQUENCY_SEC):
        now = datetime.now()
        dir_path = Path(f"DATA/gtfs/{DATA}") / now.strftime("%Y%m%d")
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # download, parse using GTFSEntity and save to parquet file
        file_path = dir_path / f"{DATA}_{now.strftime('%H%M%S')}.parquet"

        content = GTFSEntity().read_from_url(URL + DATA)
        flattened_content = GTFSEntity().flatten(content, fetch_ts=int(now.timestamp()))

        #write to parquet file
        df = pl.DataFrame(flattened_content)
        df.write_parquet(file=file_path)
        
        # request.urlretrieve(url, file_path)
        print(f"Saved: {file_path}")

        #upsert parquet to duckDB ? What if this becomes the bottleneck??
        upsert_pq_to_db(file_path)
        
        time.sleep(FREQUENCY_SEC)

def main():
    fetch_and_load(URL + DATA)



if __name__ == "__main__":
    main()