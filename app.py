import os
import time
import json
import random
import logging
from azure.iot.device import IoTHubDeviceClient, Message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Read Azure IoT Hub connection string from environment variable
CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING", "")

def generate_sensor_data():
    # Simulates vibration (mm/s), temperature (°C), and pressure (PSI)
    return {
        "deviceId": os.getenv("DEVICE_ID", "industrial-machine-01"),
        "timestamp": time.time(),
        "vibration": round(random.uniform(0.5, 12.0), 2),
        "temperature": round(random.uniform(20.0, 95.0), 2),
        "pressure": round(random.uniform(14.0, 50.0), 2),
        "sensor_status": "OK" if random.random() > 0.1 else "FAILURE"  # 10% simulated failure
    }

def main():
    if not CONNECTION_STRING:
        logging.warning("IOTHUB_DEVICE_CONNECTION_STRING not set. Running in simulation mode...")
        client = None
    else:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        client.connect()
        logging.info("Successfully connected to Azure IoT Hub.")

    try:
        while True:
            data = generate_sensor_data()
            payload = json.dumps(data)
            
            # Failure detection flag set as application property for IoT Hub routing
            msg = Message(payload)
            msg.custom_properties["sensor_failure"] = "true" if data["sensor_status"] == "FAILURE" else "false"
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"

            if client:
                client.send_message(msg)
                logging.info(f"Sent telemetry: {payload}")
            else:
                logging.info(f"[SIMULATION] Telemetry output: {payload}")

            time.sleep(5)

    except KeyboardInterrupt:
        logging.info("Disconnecting application...")
        if client:
            client.disconnect()

if __name__ == "__main__":
    main()