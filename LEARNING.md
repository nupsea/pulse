#Learnings from Pulse Project

## Chapter 1

### Step 1

The data downloaded from the link `https://gtfsrt.api.translink.com.au/api/realtime/SEQ/VehiclePositions` was saved into a raw file using wget command. 

When raw bytes was read and parsed it gave an output 503, which is the number of bytes parsed. Checking on the data files, it looks what was downloaded at that point in time..
```
-rw-r--r--  1 sethurama  staff   503B 22 Oct 21:45 VehiclePositions
-rw-r--r--@ 1 sethurama  staff  7061 24 Oct 21:09 VehiclePositions.1
-rw-r--r--@ 1 sethurama  staff   573 24 Oct 21:09 pulse.pb
```

Reading and parsing the entities stored in notebooks/spike.py. 
> Used polars, duckDB and marimo functionalities to play. Setup section in spike.py


### Step 2

Read data from VehiclePositions.1 for initial data comprehension. 

> Found no missing data. All fields look populated at least with the ones I imported.
> Avg gap time between vechicle timestamp and header timestamp looks to be around 20 sec.. with few outliers like ~3000 sec

### Step 3

parse.py read the contents from the DATA/raw/sample.pb file and flattens it into a list of entities, where entity is a dict. 
I didn't find any missing data. Not sure how it needs to be handled for proper analysis as of now.

### Step 4

Captured the count from couple of runs.. So it is almost double the expected.

### Step 5

Loaded the static timetable data into duckDB. Read it after joining trips with routes. Refer to spike.py.


### Step 6

Flattened the realtime poll data into parquet and then uploaded that into DuckDB


### Step 7

Tried writing each query myself. Got stuck at places and got some AI assistance for learning them. Probably would need more practice as I've lost touch. 


 

