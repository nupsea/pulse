# DuckDB

SELECT vehicle_id, COUNT(*) as cnt 
    FROM vehicle_positions
WHERE fetch_ts = '1793077479' 
GROUP BY vehicle_id
ORDER BY vehicle_id
HAVING cnt > 1;

