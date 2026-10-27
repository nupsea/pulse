import duckdb

# load parquet to duckDB
def upsert_pq_to_db(file_path: str):

    with duckdb.connect(database='DATA/pulse.duckdb', read_only=False) as conn:

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
        
        print(f"Updated {conn.execute('SELECT COUNT(*) FROM vehicle_positions').fetchone()[0]} records")


    