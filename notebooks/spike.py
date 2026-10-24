import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    vp_path_1 = "/Users/sethurama/DEV/LM/pulse/DATA/VehiclePositions"
    vp_path_2 = "/Users/sethurama/DEV/LM/pulse/DATA/VehiclePositions.1"
    with open(vp_path_1, 'rb') as fb:
        raw_bytes = fb.read()
    
    return (raw_bytes,)


@app.cell
def _(raw_bytes):

    from google.transit import gtfs_realtime_pb2
    feed = gtfs_realtime_pb2.FeedMessage()
    res = feed.ParseFromString(raw_bytes) 

    for entity in feed.entity:
      if entity.HasField('vehicle'):
        print(entity.vehicle)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
