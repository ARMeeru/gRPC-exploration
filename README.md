# Weather Microservice with gRPC and Python

Welcome to the **Weather Microservice** project! This application provides comprehensive weather data using the OpenWeatherMap One Call API 3.0 and exposes it through a gRPC service.

## Table of Contents

- [Weather Microservice with gRPC and Python](#weather-microservice-with-grpc-and-python)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features (in progress)](#features-in-progress)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the Repository](#clone-the-repository)
    - [Set Up a Virtual Environment](#set-up-a-virtual-environment)
    - [Install Required Packages](#install-required-packages)
  - [Configuration](#configuration)
    - [Obtain OpenWeatherMap API Key](#obtain-openweathermap-api-key)
    - [Export the API Key](#export-the-api-key)
  - [Generating gRPC Code from Protobuf Files](#generating-grpc-code-from-protobuf-files)
    - [Install Protocol Buffer Compiler (`protoc`)](#install-protocol-buffer-compiler-protoc)
    - [Generate Python Code from `.proto` File](#generate-python-code-from-proto-file)
  - [Running the Application](#running-the-application)
    - [Running the Server](#running-the-server)
    - [Running the Client](#running-the-client)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [License](#license)

---

## Introduction

This project is a microservice that fetches weather data from the OpenWeatherMap One Call API 3.0 and provides it through a gRPC interface. It's built with Python and uses Protocol Buffers for defining the service interface.

---

## Features (in progress)

- **Current Weather Conditions**: Get real-time weather data for any location.
- **Minute Forecast**: Receive minute-by-minute forecasts for the next hour.
- **Hourly Forecast**: Access hourly forecasts for the next 48 hours.
- **Daily Forecast**: Obtain daily forecasts for the next 8 days.
- **Weather Alerts**: Get national weather alerts (if available).
- **Historical Weather Data**: Retrieve historical weather data (subject to API availability).

---

## Prerequisites

- **Python**: Version 3.7 or higher
- **pip**: Python package manager
- **Protocol Buffer Compiler (`protoc`)**
- **OpenWeatherMap API Key**: Sign up [here](https://openweathermap.org/api) to obtain an API key (One Call 3.0 will require subscription)

---

## Installation

### Clone the Repository

Clone this repository to your local machine using:

```bash
git clone git@github.com:ARMeeru/gRPC-exploration.git
cd gRPC-exploration
```

### Set Up a Virtual Environment

Create and activate a virtual environment to manage project dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Required Packages

Install the packages manually:

```bash
pip install grpcio grpcio-tools requests
```

---

## Configuration

### Obtain OpenWeatherMap API Key

1. **Sign Up** at [OpenWeatherMap](https://openweathermap.org/api).
2. **Get Your API Key** from your account dashboard.

### Export the API Key

Set the API key as an environment variable so that the application can access it.

```bash
export OPENWEATHER_API_KEY='your_openweathermap_api_key_here'
```

Replace `'your_openweathermap_api_key_here'` with your actual API key.

---

## Generating gRPC Code from Protobuf Files

The service interface is defined in the `weather.proto` file using Protocol Buffers.

### Install Protocol Buffer Compiler (`protoc`)

If you haven't installed `protoc`, use Homebrew:

```bash
brew install protobuf
```

### Generate Python Code from `.proto` File

Run the following command from the project root directory:

```bash
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/weather.proto
```

This command generates `weather_pb2.py` and `weather_pb2_grpc.py` files needed for the gRPC server and client.

---

## Running the Application

### Running the Server

1. **Activate the Virtual Environment**:

   ```bash
   source venv/bin/activate
   ```

2. **Run the Server**:

   ```bash
   python server.py
   ```

   You should see:

   ```
   Weather gRPC server is running on port 50051...
   ```

### Running the Client

In a new terminal window or tab:

1. **Activate the Virtual Environment**:

   ```bash
   source venv/bin/activate
   ```

2. **Run the Client**:

   ```bash
   python client.py
   ```

   The client will request weather data from the server and display it.

---

## Usage

The client is currently configured to request weather data for **Dhaka, Bangladesh**. You can modify `client.py` to request data for different coordinates or customize the request parameters.

**Example**: Changing the location in `client.py`:

```python
coordinates = weather_pb2.Coordinates(latitude=40.7128, longitude=-74.0060)  # New York City, USA
```

**Excluding Data Sections**:

```python
request = weather_pb2.WeatherDataRequest(
    coordinates=coordinates,
    exclude=['minutely', 'alerts'],  # Exclude minutely data and alerts
    units='metric',
    language='en'
)
```

---

## Project Structure

```
weather-microservice/
├── protos/
│   └── weather.proto          # Protobuf definitions
├── weather_pb2.py             # Generated code from .proto
├── weather_pb2_grpc.py        # Generated gRPC code from .proto
├── server.py                  # Server implementation
├── client.py                  # Client implementation
├── README.md                  # Project documentation
└── venv/                      # Python virtual environment
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note**: This application is for educational purposes and may require additional enhancements for production use, such as improved error handling, security features, and scalability considerations.

**Disclaimer**: Be mindful of the OpenWeatherMap API usage limits and terms of service when using this application.

---