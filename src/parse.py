from google.transit.gtfs_realtime_pb2 import FeedEntity, FeedMessage
from urllib import request

class GTFSEntity:

    def __repr__(self, entity: FeedEntity) -> str:
        field_list = ['FeedEntity: ']
        for field in entity.DESCRIPTOR.fields_by_name: 
            field_list.append(field)
        return ' '.join(field_list)

    
    def read_from_url(self, url: str) -> FeedMessage:
        with request.urlopen(url) as response:
            feed_message = FeedMessage()
            feed_message.ParseFromString(response.read())
        return feed_message


    def read_from_file(self, file_path: str) -> FeedMessage:
        with open(file_path, 'rb') as f:
            feed_message = FeedMessage()
            feed_message.ParseFromString(f.read())
        return feed_message 


    def flatten(self, feed_message: FeedMessage, fetch_ts: int | None = None) -> list[dict]:
        if fetch_ts is None:
            fetch_ts = feed_message.header.timestamp
        flattened_data = []
        for entity in feed_message.entity:
            if entity.HasField('vehicle'):
                flattened_data.append({
                    'entity_id': entity.id,
                    'vehicle_id': entity.vehicle.vehicle.id,
                    'trip_id': entity.vehicle.trip.trip_id,
                    'route_id': entity.vehicle.trip.route_id,
                    'start_date': entity.vehicle.trip.start_date,
                    'lat': entity.vehicle.position.latitude,
                    'lon': entity.vehicle.position.longitude,
                    'stop_id': entity.vehicle.stop_id,
                    'current_stop_sequence': entity.vehicle.current_stop_sequence,
                    'current_status': entity.vehicle.current_status,
                    'vehicle_ts': entity.vehicle.timestamp,
                    'fetch_ts': fetch_ts,
                })
            elif entity.HasField('trip_update'):
                for stu in entity.trip_update.stop_time_update:
                    flattened_data.append({
                        'entity_id': entity.id,
                        'trip_id': entity.trip_update.trip.trip_id,
                        'route_id': entity.trip_update.trip.route_id,
                        'start_date': entity.trip_update.trip.start_date,
                        'vehicle_id': entity.trip_update.vehicle.id,
                        'stop_sequence': stu.stop_sequence,
                        'stop_id': stu.stop_id,
                        'arrival_delay': stu.arrival.delay if stu.HasField('arrival') else None,
                        'arrival_time': stu.arrival.time if stu.HasField('arrival') else None,
                        'departure_delay': stu.departure.delay if stu.HasField('departure') else None,
                        'departure_time': stu.departure.time if stu.HasField('departure') else None,
                        'schedule_relationship': stu.schedule_relationship,
                        'trip_update_ts': entity.trip_update.timestamp,
                        'fetch_ts': fetch_ts,
                    })
        return flattened_data


if __name__ == "__main__":
    # Understand FeedEntity Structure of GTFS Real Time
    gtfsEntity = GTFSEntity()
    print(gtfsEntity.__repr__(FeedEntity))

    # Read the contents of a sample VehicleEntity file
    contents = gtfsEntity.read_from_file('DATA/raw/20261026/133349.pb')
    print(gtfsEntity.flatten(contents))






    