import serial
import requests
import time

ser = serial.Serial('COM5', 9600)  # Replace with the correct COM port name on Windows

API_URL = 'http://127.0.0.1:8000/api/pH_value/'  # Replace with your server's API URL

while True:
    data = ser.readline().strip()  # Read data from Arduino
    data = data.decode()  # Convert bytes to string

    try:
        value = float(data)  # Assuming the received data is a float
        payload = {'value': value}
        print(payload)
        response = requests.post(API_URL, data=payload)
        if response.status_code == 201:
            print("Data posted successfully:", data)
        else:
            print("Failed to post data:", data)
    except ValueError:
        print("Invalid data format:", data)

    time.sleep(5)  # Delay before reading next data