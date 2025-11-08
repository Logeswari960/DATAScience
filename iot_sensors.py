import random
import time
from datetime import datetime

class IoTSensors:
    def __init__(self):
        self.base_temp = 22.0
        self.base_humidity = 55.0
    
    def read_temperature(self):
        # Simulate DHT22 temperature sensor
        variation = random.uniform(-2, 3)
        temp = self.base_temp + variation
        return round(temp, 1)
    
    def read_humidity(self):
        # Simulate DHT22 humidity sensor
        variation = random.uniform(-10, 15)
        humidity = self.base_humidity + variation
        return round(max(30, min(80, humidity)), 1)
    
    def get_sensor_data(self):
        return {
            'temperature': self.read_temperature(),
            'humidity': self.read_humidity(),
            'timestamp': datetime.now().isoformat()
        }

# Simulate Arduino/Raspberry Pi connection
def connect_to_device():
    print("Connecting to IoT device...")
    time.sleep(1)
    print("IoT sensors connected successfully!")
    return IoTSensors()