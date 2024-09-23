# server.py

from concurrent import futures
import grpc
import weather_pb2
import weather_pb2_grpc
import requests
import os

API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not API_KEY:
    print("Please set the OPENWEATHER_API_KEY environment variable.")
    exit(1)

class WeatherServiceServicer(weather_pb2_grpc.WeatherServiceServicer):

    def GetWeatherData(self, request, context):
        latitude = request.coordinates.latitude
        longitude = request.coordinates.longitude
        exclude = ','.join(request.exclude)
        units = request.units or 'metric'
        lang = request.language or 'en'

        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude={exclude}&appid={API_KEY}&units={units}&lang={lang}"

        response = requests.get(url)
        data = response.json()

        if 'cod' in data and data['cod'] != 200:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, data.get('message', 'Invalid request'))

        weather_data_response = weather_pb2.WeatherDataResponse()

        # Process current weather
        if 'current' in data:
            weather_data_response.current.CopyFrom(self.parse_current_weather(data['current']))

        # Process minutely forecast
        if 'minutely' in data:
            for minute_data in data['minutely']:
                minute_forecast = self.parse_minute_forecast(minute_data)
                weather_data_response.minutely.append(minute_forecast)

        # Process hourly forecast
        if 'hourly' in data:
            for hourly_data in data['hourly']:
                hourly_forecast = self.parse_hourly_forecast(hourly_data)
                weather_data_response.hourly.append(hourly_forecast)

        # Process daily forecast
        if 'daily' in data:
            for daily_data in data['daily']:
                daily_forecast = self.parse_daily_forecast(daily_data)
                weather_data_response.daily.append(daily_forecast)

        # Process alerts
        if 'alerts' in data:
            for alert_data in data['alerts']:
                alert = self.parse_weather_alert(alert_data)
                weather_data_response.alerts.append(alert)

        return weather_data_response

    # Helper methods to parse data
    def parse_weather_condition(self, conditions):
        weather_conditions = []
        for condition in conditions:
            weather_condition = weather_pb2.WeatherCondition(
                id=condition.get('id', 0),
                main=condition.get('main', ''),
                description=condition.get('description', ''),
                icon=condition.get('icon', '')
            )
            weather_conditions.append(weather_condition)
        return weather_conditions

    def parse_current_weather(self, data):
        return weather_pb2.CurrentWeather(
            dt=data.get('dt', 0),
            sunrise=data.get('sunrise', 0),
            sunset=data.get('sunset', 0),
            temp=data.get('temp', 0.0),
            feels_like=data.get('feels_like', 0.0),
            pressure=data.get('pressure', 0),
            humidity=data.get('humidity', 0),
            dew_point=data.get('dew_point', 0.0),
            uvi=data.get('uvi', 0.0),
            clouds=data.get('clouds', 0),
            visibility=data.get('visibility', 0),
            wind_speed=data.get('wind_speed', 0.0),
            wind_deg=data.get('wind_deg', 0),
            wind_gust=data.get('wind_gust', 0.0),
            weather=self.parse_weather_condition(data.get('weather', []))
        )

    def parse_minute_forecast(self, data):
        return weather_pb2.MinuteForecast(
            dt=data.get('dt', 0),
            precipitation=data.get('precipitation', 0.0)
        )

    def parse_hourly_forecast(self, data):
        return weather_pb2.HourlyForecast(
            dt=data.get('dt', 0),
            temp=data.get('temp', 0.0),
            feels_like=data.get('feels_like', 0.0),
            pressure=data.get('pressure', 0),
            humidity=data.get('humidity', 0),
            dew_point=data.get('dew_point', 0.0),
            clouds=data.get('clouds', 0),
            visibility=data.get('visibility', 0),
            wind_speed=data.get('wind_speed', 0.0),
            wind_deg=data.get('wind_deg', 0),
            wind_gust=data.get('wind_gust', 0.0),
            pop=data.get('pop', 0.0),
            weather=self.parse_weather_condition(data.get('weather', []))
        )

    def parse_daily_forecast(self, data):
        temp = weather_pb2.Temperature(
            day=data['temp'].get('day', 0.0),
            min=data['temp'].get('min', 0.0),
            max=data['temp'].get('max', 0.0),
            night=data['temp'].get('night', 0.0),
            eve=data['temp'].get('eve', 0.0),
            morn=data['temp'].get('morn', 0.0)
        )
        feels_like = weather_pb2.FeelsLike(
            day=data['feels_like'].get('day', 0.0),
            night=data['feels_like'].get('night', 0.0),
            eve=data['feels_like'].get('eve', 0.0),
            morn=data['feels_like'].get('morn', 0.0)
        )
        return weather_pb2.DailyForecast(
            dt=data.get('dt', 0),
            sunrise=data.get('sunrise', 0),
            sunset=data.get('sunset', 0),
            moonrise=data.get('moonrise', 0),
            moonset=data.get('moonset', 0),
            moon_phase=data.get('moon_phase', 0.0),
            temp=temp,
            feels_like=feels_like,
            pressure=data.get('pressure', 0),
            humidity=data.get('humidity', 0),
            dew_point=data.get('dew_point', 0.0),
            wind_speed=data.get('wind_speed', 0.0),
            wind_deg=data.get('wind_deg', 0),
            wind_gust=data.get('wind_gust', 0.0),
            clouds=data.get('clouds', 0),
            pop=data.get('pop', 0.0),
            uvi=data.get('uvi', 0.0),
            weather=self.parse_weather_condition(data.get('weather', []))
        )

    def parse_weather_alert(self, data):
        return weather_pb2.WeatherAlert(
            sender_name=data.get('sender_name', ''),
            event=data.get('event', ''),
            start=data.get('start', 0),
            end=data.get('end', 0),
            description=data.get('description', ''),
            tags=data.get('tags', [])
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Weather gRPC server is running on port 50051...")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()