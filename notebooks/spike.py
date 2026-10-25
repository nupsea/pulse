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
def _():
    return


if __name__ == "__main__":
    app.run()
