import os
import asyncio
from datetime import datetime

os.environ["RUUVI_BLE_ADAPTER"] = "bleak"
from prometheus_client import Gauge, start_http_server
from ruuvitag_sensor.ruuvi import RuuviTagSensor

temp_gauge = Gauge("ruuvi_temperature_c", "Temperature in Celsius", ["location"])
humidity_gauge = Gauge("ruuvi_humidity_percent", "Humidity %", ["location"])
pressure_gauge = Gauge("ruuvi_pressure_hpa", "Air pressure hPa", ["location"])
battery_gauge = Gauge("ruuvi_battery_v", "Battery V", ["location"])

sensors = {
    "Livingroom": "F8:50:A3:13:1D:B7",
    "Bedroom": "D4:EF:90:6E:11:4F",
}


def set_gauges(data: tuple, room: str):
    """Sets gauges for Prometheus to scrape"""
    temp = data[1]["temperature"]
    humidity = data[1]["humidity"]
    pressure = data[1]["pressure"]
    battery = data[1]["battery"]

    temp_gauge.labels(room).set(temp)
    humidity_gauge.labels(room).set(humidity / 100.0)
    pressure_gauge.labels(room).set(pressure)
    battery_gauge.labels(room).set(battery / 1000.0)
    print(f"{room} temp:{temp}")


async def main():
    """Async function that runs and gathers data from RuuviTags"""
    async for data in RuuviTagSensor.get_data_async():
        sensor_mac = data[0]
        print("Received data")
        if sensor_mac == sensors["Livingroom"]:
            room = "Livingroom"
            set_gauges(data, room)
        elif sensor_mac == sensors["Bedroom"]:
            room = "Bedroom"
            set_gauges(data, room)


if __name__ == "__main__":
    print("Starting HTTP server for Prometheus scraping on localhost:8000")
    start_http_server(8000)
    print("Reading data from Ruuvi tags")
    asyncio.get_event_loop().run_until_complete(main())
