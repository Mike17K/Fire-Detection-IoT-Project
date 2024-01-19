import paho.mqtt.client as mqtt
import json

from context_broker import ContextBroker

class MqttClient:
    def __init__(self, host, port, broker_connection:ContextBroker):
        self.broker_connection = broker_connection

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(host, port, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe([
            ("json/Room monitoring/mclimate-co2-sensor:1", 0),
            ("json/Environmental/barani-meteowind-iot-pro:1", 0),
            ("json/Environmental/barani-meteohelix-iot-pro:1", 0),
        ])

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic)

        decoded_payload = msg.payload.decode("utf8")
        data = json.loads(decoded_payload)

        match msg.topic:
            case "json/Room monitoring/mclimate-co2-sensor:1":
                self.handle_mclimate_co2(data)
            case "json/Environmental/barani-meteowind-iot-pro:1":
                self.handle_meteowind(data)
            case "json/Environmental/barani-meteohelix-iot-pro:1":
                self.handle_meteohelix(data)

    def handle_meteowind(self, data):
        print(json.dumps(data, indent=4, sort_keys=True))

        serialNumber = data["deviceInfo"]["devEui"]
        device = self.broker_connection.find_device_by_serial(serialNumber)

        windSpeed = data["object"]["3_Wind_ave10"]
        windDirection = data["object"]["6_Dir_ave10"]

    def handle_meteohelix(self, data):
        print(json.dumps(data, indent=4, sort_keys=True))

        serialNumber = data["deviceInfo"]["devEui"]
        device = self.broker_connection.find_device_by_serial(serialNumber)

        temperature = data["object"]["Temperature"]
        relativeHumidity = data["object"]["Humidity"]

    def handle_mclimate_co2(self, data):
        print(json.dumps(data, indent=4, sort_keys=True))

        serialNumber = data["deviceInfo"]["devEui"]
        device = self.broker_connection.find_device_by_serial(serialNumber)

        co2 = data["object"]["CO2"]
        relativeHumidity = data["object"]["relativeHumidity"]

if __name__ == "__main__":
    cb = ContextBroker("192.168.1.2")
    client = MqttClient("150.140.186.118", 1883, cb)
