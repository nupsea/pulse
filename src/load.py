import duckdb
from pathlib import Path

# load parquet to duckDB
def upsert_pq_to_db(file_path: str | Path, data_group: str = "VehiclePositions"):

    with duckdb.connect(database='DATA/pulse.duckdb', read_only=False) as conn:

        if data_group == "VehiclePositions":
            # Check if table already exists, if not create it
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vehicle_positions (
                    entity_id VARCHAR,
                    vehicle_id VARCHAR,
                    trip_id VARCHAR,
                    route_id VARCHAR,
                    start_date VARCHAR,
                    lat VARCHAR,
                    lon VARCHAR,
                    stop_id VARCHAR,
                    current_stop_sequence VARCHAR,
                    current_status VARCHAR,
                    vehicle_ts VARCHAR,
                    fetch_ts VARCHAR,
                    PRIMARY KEY (entity_id, vehicle_ts, fetch_ts)
                )
            """)
            
            # UPSERT parquet to vehicle_positions table on entity_id + vehicle_ts + fetch_ts
            conn.execute(f"""
                INSERT INTO vehicle_positions SELECT * FROM read_parquet('{file_path}')
                ON CONFLICT (entity_id, vehicle_ts, fetch_ts) DO UPDATE SET
                    vehicle_id = EXCLUDED.vehicle_id,
                    trip_id = EXCLUDED.trip_id,
                    route_id = EXCLUDED.route_id,
                    start_date = EXCLUDED.start_date,
                    lat = EXCLUDED.lat,
                    lon = EXCLUDED.lon,
                    stop_id = EXCLUDED.stop_id,
                    current_stop_sequence = EXCLUDED.current_stop_sequence,
                    current_status = EXCLUDED.current_status;
            """)
            
            print(f"Updated {conn.execute('SELECT COUNT(*) FROM vehicle_positions').fetchone()[0]} records in vehicle_positions")

        elif data_group == "TripUpdates":
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trip_updates (
                    entity_id VARCHAR,
                    trip_id VARCHAR,
                    route_id VARCHAR,
                    start_date VARCHAR,
                    vehicle_id VARCHAR,
                    stop_sequence VARCHAR,
                    stop_id VARCHAR,
                    arrival_delay VARCHAR,
                    arrival_time VARCHAR,
                    departure_delay VARCHAR,
                    departure_time VARCHAR,
                    schedule_relationship VARCHAR,
                    trip_update_ts VARCHAR,
                    fetch_ts VARCHAR,
                    PRIMARY KEY (entity_id, stop_sequence, stop_id, trip_update_ts, fetch_ts)
                )
            """)

            conn.execute(f"""
                INSERT INTO trip_updates SELECT * FROM read_parquet('{file_path}')
                ON CONFLICT (entity_id, stop_sequence, stop_id, trip_update_ts, fetch_ts) DO UPDATE SET
                    trip_id = EXCLUDED.trip_id,
                    route_id = EXCLUDED.route_id,
                    start_date = EXCLUDED.start_date,
                    vehicle_id = EXCLUDED.vehicle_id,
                    arrival_delay = EXCLUDED.arrival_delay,
                    arrival_time = EXCLUDED.arrival_time,
                    departure_delay = EXCLUDED.departure_delay,
                    departure_time = EXCLUDED.departure_time,
                    schedule_relationship = EXCLUDED.schedule_relationship;
            """)

            print(f"Updated {conn.execute('SELECT COUNT(*) FROM trip_updates').fetchone()[0]} records in trip_updates")

        else:
            raise ValueError(f"Unsupported data_group: {data_group}")



    