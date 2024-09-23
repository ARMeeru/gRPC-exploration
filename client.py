# client.py

import grpc
import weather_pb2
import weather_pb2_grpc
from datetime import datetime

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = weather_pb2_grpc.WeatherServiceStub(channel)

    coordinates = weather_pb2.Coordinates(latitude=23.777176, longitude=-90.399452)  # Dhaka, Bangladesh

    request = weather_pb2.WeatherDataRequest(
        coordinates=coordinates,
        exclude=[],  # No exclusions
        units='metric',
        language='en'
    )

    try:
        response = stub.GetWeatherData(request)
        print_current_weather(response.current)
    except grpc.RpcError as e:
        print(f"Error occurred: {e.details()} (Code: {e.code()})")

def print_current_weather(current):
    print("\nCurrent Weather:")
    print(f"Timestamp: {datetime.fromtimestamp(current.dt)}")
    print(f"Temperature: {current.temp}°C")
    print(f"Feels Like: {current.feels_like}°C")
    print(f"Humidity: {current.humidity}%")
    print(f"Weather Description: {current.weather[0].description if current.weather else 'N/A'}")

if __name__ == '__main__':
    run()