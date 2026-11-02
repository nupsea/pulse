import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    Import necessary packages and libs to analyse GTFS data.
    """)
    return


@app.cell
def _():

    import marimo as mo
    import polars as pl
    import duckdb

    return duckdb, mo, pl


@app.cell
def _(mo, pl):
    trip_path = "/Users/sethurama/DEV/LM/pulse/DATA/SAMPLE/static/trips.txt"
    trip_data = pl.read_csv(trip_path, separator=',')
    mo.sql("SELECT * FROM trip_data")
    return trip_data, trip_path


@app.cell
def _(mo, trip_path):
    df2 = mo.sql(
        f"""
        SELECT * 
        FROM read_csv('{trip_path}', delim = ',', header = TRUE)
        """
    )
    df2
    return


@app.cell
def _(duckdb):
    conn = duckdb.connect('/Users/sethurama/DEV/LM/pulse/DATA/pulse.duckdb')
    return (conn,)


@app.cell
def _(conn, mo, trip_path):
    _df = mo.sql(
        f"""
        DROP TABLE pulse.my_trip_data;
        CREATE TABLE pulse.my_trip_data AS 
            SELECT * FROM read_csv('{trip_path}', delim=',', header=true);
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(conn, mo):
    _df = mo.sql(
        f"""
        SELECT route_id, service_id 
        FROM pulse.my_trip_data;
        """,
        engine=conn
    )
    return


@app.cell
def _():
    vp_path_1 = "/Users/sethurama/DEV/LM/pulse/DATA/SAMPLE/realtime/VehiclePositions"
    vp_path_2 = "/Users/sethurama/DEV/LM/pulse/DATA/SAMPLE/realtime/VehiclePositions.1"
    with open(vp_path_2, 'rb') as fb:
        raw_bytes = fb.read()
    return (raw_bytes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Decode a snapshot

    Read GTFS realtime data and understand the structure, see what's missing to understand what can be done.
    """)
    return


@app.cell
def _(raw_bytes):

    from google.transit import gtfs_realtime_pb2
    feed = gtfs_realtime_pb2.FeedMessage()
    res = feed.ParseFromString(raw_bytes) 

    print(f"HEADER:\n{feed.header}")
    print(f"LEN of FEED ENTITY:{len(feed.entity)}\n")

    print(f"ENTITY:\n{feed.entity}")
    return (feed,)


@app.cell
def _(feed):
    # Iterate 

    first_entity = next(iter(feed.entity), None)
    print(first_entity)
    return


@app.cell
def _(feed):
    # Gap b/w header timestamp and vehicle timestamp

    header_ts = feed.header.timestamp

    for entity in (feed.entity):
      if entity.HasField('vehicle'):
        vehicle_ts = entity.vehicle.timestamp
        print(f"Gap for trip: {entity.vehicle.trip.trip_id} in secs is: {header_ts - vehicle_ts}")
    return


@app.cell
def _(conn, mo):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS trips ;
        CREATE TABLE trips AS 
            SELECT * FROM read_csv('DATA/gtfs/trips.txt', all_varchar = true);
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(conn, mo, trips):
    _df = mo.sql(
        f"""
        DESCRIBE trips;
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(conn, mo):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS routes;
        CREATE TABLE routes AS 
            SELECT * FROM read_csv('DATA/gtfs/routes.txt', all_varchar = true);
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(conn, mo):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS stop_times;
        CREATE TABLE stop_times AS 
            SELECT * FROM read_csv('DATA/gtfs/stop_times.txt', all_varchar = true);
        """,
        engine=conn
    )
    return


@app.cell
def _(conn, mo, trips):
    _df = mo.sql(
        f"""
        SELECT * FROM trips LIMIT 5;
        """,
        engine=conn
    )
    return


@app.cell
def _(conn, mo, routes):
    _df = mo.sql(
        f"""
        SELECT * FROM routes LIMIT 5;
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Determine number of Trips per Route type.
    """)
    return


@app.cell(hide_code=True)
def _(conn, mo):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS route_types;
        CREATE TABLE route_types (route_type_id VARCHAR, route_type_name VARCHAR);

        INSERT INTO route_types VALUES 
        (0, 'tram'), 
        (2, 'rail'), 
        (3, 'bus'), 
        (4, 'ferry');
        """,
        engine=conn
    )
    return


@app.cell
def _(conn, mo, route_types, routes, trips):
    _df = mo.sql(
        f"""
        SELECT route_type_name, COUNT(trip_id) as route_count
        FROM routes 
            INNER JOIN trips ON routes.route_id = trips.route_id 
        	INNER JOIN route_types ON routes.route_type = route_types.route_type_id
        GROUP BY route_type_name
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 6
    """)
    return


@app.cell(hide_code=True)
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        SELECT count(*), count(DISTINCT fetch_ts) FROM vehicle_positions
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Volume**: how many vehicles per poll, and how does that split by mode?
    >
    """)
    return


@app.cell(hide_code=True)
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        SELECT * FROM vehicle_positions LIMIT 5;
        """,
        engine=conn
    )
    return


@app.cell
def _(conn, mo, route_types, routes, trips, vehicle_positions):
    _df = mo.sql(
        f"""
        SELECT fetch_ts, route_type_name, COUNT(trips.trip_id) 
        FROM vehicle_positions
        INNER JOIN trips 
            ON vehicle_positions.trip_id = trips.trip_id
        INNER JOIN routes 
            ON routes.route_id = trips.route_id
        INNER JOIN route_types
            ON routes.route_type = route_types.route_type_id
        GROUP BY fetch_ts, route_type_name
        ORDER BY fetch_ts
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Freshness**: how often does the feed really change?

    Count distinct feed_ts vs number of polls. Then look at how often a single vehicle's vehicle_ts changes.
    """)
    return


@app.cell
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        SELECT COUNT(DISTINCT fetch_ts) as distinct_feeds, COUNT(fetch_ts) as num_polls
            FROM vehicle_positions;
        """,
        engine=conn
    )
    return


@app.cell
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        SELECT vehicle_id, COUNT(*) as cnt 
            FROM vehicle_positions
        WHERE fetch_ts = '1793077479' 
        GROUP BY vehicle_id
        HAVING COUNT(*) = 1
        ORDER BY vehicle_id;
            -- AND vehicle_id = '73DD7B678B530932DF783319BBF95E95_1007'
        """,
        engine=conn
    )
    return


@app.cell
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        -- How frequently vehicle_ts changes.

        SELECT fetch_ts, COUNT(DISTINCT vehicle_ts) as cnt 
        FROM vehicle_positions
        GROUP BY fetch_ts
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Lag:**  how old is a position when you receive it?

    fetch_ts − vehicle_ts, median and p95 (quantile_cont).
    """)
    return


@app.cell
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        WITH computed_lag AS (
            SELECT (fetch_ts::BIGINT - vehicle_ts::BIGINT) as diff 
        	FROM vehicle_positions
        )
        SELECT MEDIAN(diff) as median_diff_secs, quantile_cont(diff, 0.95) as p95_lag_secs
            FROM computed_lag
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Duplicates:** how often do you see the same report twice?

    Same (vehicle_id, vehicle_ts) in more than one poll, as a share of all rows.
    """)
    return


@app.cell
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        WITH ranked_vps AS (
            SELECT vehicle_id, ROW_NUMBER() OVER (
                PARTITION BY (vehicle_id, vehicle_ts)
                ORDER BY fetch_ts
        	) as ranked 
        FROM vehicle_positions
        )
        SELECT vehicle_id, ranked  
        FROM ranked_vps
        WHERE ranked > 1
        ORDER BY ranked DESC
        """,
        engine=conn
    )
    return


@app.cell
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        WITH duped_vps AS (
            SELECT vehicle_id, ROW_NUMBER() OVER (
                PARTITION BY (vehicle_id, vehicle_ts)
                ORDER BY fetch_ts
        	) as duped 
        FROM vehicle_positions
        )
        SELECT 
            COUNT_IF (duped > 1) as duped_count, 
            COUNT(*) AS total_count,
            duped_count::DOUBLE/total_count * 100 as duped_percentage
        FROM duped_vps
        """,
        engine=conn
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Join quality:** what share of realtime trip_ids exist in the timetable?

    Distinct realtime trip_ids found in trips ÷ all distinct.
    """)
    return


@app.cell
def _(conn, mo, trips, vehicle_positions):
    _df = mo.sql(
        f"""
        WITH rt_trips AS (
            SELECT DISTINCT trip_id
            FROM vehicle_positions
        )

        SELECT 
            COUNT(DISTINCT trips.trip_id) as shared_rt_trips, 
            COUNT(rt_trips.trip_id) as all_distinct,
            shared_rt_trips::DOUBLE/all_distinct * 100 AS shared_trip_percentage
        FROM rt_trips
        LEFT JOIN trips 
        	ON rt_trips.trip_id = trips.trip_id


            	;
        """,
        engine=conn
    )
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Trip Updates
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(conn, mo, vehicle_positions):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) 
        FROM vehicle_positions
        -- WHERE to_timestamp(fetch_ts::BIGINT)::DATE = CURRENT_DATE;
        """,
        engine=conn
    )
    return


@app.cell
def _(pl):
    from google.transit import gtfs_realtime_pb2 as pb2
    from datetime import datetime   

    import os
    import time
    from pathlib import Path
    from urllib import request

    from src.parse import GTFSEntity

    url = "https://gtfsrt.api.translink.com.au/api/realtime/SEQ/" 
    data_group = "TripUpdates"

    now = datetime.now()
    dir_path = Path(f"DATA/gtfs/{data_group}") / now.strftime("%Y%m%d")
    dir_path.mkdir(parents=True, exist_ok=True)

    # download, parse using GTFSEntity and save to parquet file
    file_path = dir_path / f"{data_group}_{now.strftime('%H%M%S')}.parquet"

    content = GTFSEntity().read_from_url(url + data_group)
    flattened_content = GTFSEntity().flatten(content, fetch_ts=int(now.timestamp()))

    #write to parquet file
    df = pl.DataFrame(flattened_content)
    df.write_parquet(file=file_path)

    # request.urlretrieve(url, file_path)
    print(f"Saved: {file_path}")
    return


@app.cell
def _(pl):
    tru_df = pl.read_parquet("DATA/gtfs/TripUpdates/20261102/TripUpdates_131301.parquet")
    return (tru_df,)


@app.cell
def _(tru_df):
    tru_df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
