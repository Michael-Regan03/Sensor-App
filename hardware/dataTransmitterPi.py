import serial
import requests
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)  # port for pi

API_URL = 'http://127.0.0.1:8000/api/sensorData/'  # Server's API URL

while True:
    data = ser.readline().strip()  # Read data from Arduino
    data = data.decode()  # Convert bytes to string

    try:
        # Split the received data into three values
        pH_value, temperature, tds_value = map(float, data.split())
        
        # Create a payload with three values
        payload = {
            'pH_value': pH_value,
            'temperature': temperature,
            'tds_value': tds_value
        }
        response = requests.post(API_URL, json=payload)  # Use json parameter to send JSON data
        if response.status_code == 201:
            print("Data posted successfully:", data)
        else:
            print("Failed to post data:", data)
    except ValueError:
        print("Invalid data format:", data)

    time.sleep(5)  # Delay before reading the next data
