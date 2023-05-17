import argparse
import subprocess
import time
import os
import paho.mqtt.client as mqtt
from queue import Queue
from threading import Thread

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--broker", help="MQTT broker address")
parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
parser.add_argument("--topic", help="MQTT topic")
parser.add_argument('--username', default=None, help='MQTT broker username')
parser.add_argument('--password', default=None, help='MQTT broker password')
args = parser.parse_args()

# Get configuration from environment variables
broker = os.environ.get("MQTT_BROKER") or args.broker or "your_mqtt_broker_address"
port = int(os.environ.get("MQTT_PORT") or args.port or 1883)
topic = os.environ.get("MQTT_TOPIC") or args.topic or "your_topic"
username = os.environ.get("MQTT_USERNAME") or args.username or "your_username"
password = os.environ.get("MQTT_PASSWORD") or args.password or "your_password"

# Replace this with the shell command you want to run
shell_command = "your_shell_command"
shell_directory = "your_shell_directory"

payload_queue = Queue()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {payload}")

    if payload.startswith("magnet:?xt=urn:btih:"):
        print("Payload is a torrent magnet. Adding to queue...")
        payload_queue.put(payload)
    else:
        print("Payload is not a torrent magnet. Ignoring.")

def process_queue():
    while True:
        payload = payload_queue.get()
        print("Running shell command with payload...")
        print(f"{shell_command} {payload}")
        #subprocess.run(f"{shell_command} {payload}", shell=True, check=True, cwd=shell_directory)
        print("Shell command finished.")
        payload_queue.task_done()

if 1:

    # Connect to the MQTT broker
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    if username is not None and password is not None:
        client.username_pw_set(username, password)
    client.connect(broker, port, 60)

    # Start the queue processing thread
    queue_thread = Thread(target=process_queue)
    queue_thread.start()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting from MQTT broker...")
        client.disconnect()
