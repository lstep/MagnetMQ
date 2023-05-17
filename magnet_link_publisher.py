import argparse
import os
import re
import pyperclip
import paho.mqtt.client as mqtt

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

# Connect to the MQTT broker
client = mqtt.Client()
if args.username is not None and args.password is not None:
    client.username_pw_set(args.username, args.password)
client.connect(args.broker, args.port)

# Function to check if the text is a magnet link
def is_magnet_link(text):
    magnet_pattern = r'^magnet:\?xt=urn:btih:[a-zA-Z0-9]{32,40}.*$'
    return bool(re.match(magnet_pattern, text))

# Monitor the clipboard for magnet links
previous_clipboard_content = ""
while True:
    current_clipboard_content = pyperclip.waitForNewPaste()
    if current_clipboard_content != previous_clipboard_content:
        if is_magnet_link(current_clipboard_content):
            print("Magnet link detected:", current_clipboard_content)
            #client.publish(topic, current_clipboard_content)
            print("new content: ", current_clipboard_content)
        previous_clipboard_content = current_clipboard_content
