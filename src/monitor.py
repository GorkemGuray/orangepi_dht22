#!/usr/bin/env python3
"""
DHT22 Environment Monitor

This module provides continuous monitoring of temperature and humidity
using a DHT22 sensor connected to an Orange Pi Zero.
It calculates and logs one-minute averages of environmental readings.
"""

from orangepi_dht22 import DHT22Reader, GPIOHandler
from pyA20.gpio import port
from pathlib import Path
import sys
import time
import logging
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import json
import ssl

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_PORT = int(os.getenv('MQTT_PORT', 8883))
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC_TEMP = "sensors/dht22/temperature"
MQTT_TOPIC_HUMID = "sensors/dht22/humidity"

def setup_mqtt_client():
    # Generate a unique client ID
    client_id = f'orangepi-dht22-{os.getpid()}'
    client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected to MQTT broker with client ID: {client_id}")
        else:
            error_messages = {
                1: "Incorrect protocol version",
                2: "Invalid client identifier",
                3: "Server unavailable",
                4: "Bad username or password",
                5: "Not authorized"
            }
            logging.error(f"Connection failed: {error_messages.get(rc, f'Unknown error {rc}')}")

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection. Attempting to reconnect...")
        else:
            logging.info("Disconnected from broker")

    def on_publish(client, userdata, mid):
        logging.debug(f"Message {mid} delivered to broker")

    # Set callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    # Set authentication
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # Set up TLS
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(False)

    # Set last will message
    will_payload = json.dumps({
        "status": "offline",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    })
    client.will_set("sensors/dht22/status", will_payload, qos=1, retain=True)

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.publish("sensors/dht22/status", json.dumps({
            "status": "online",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }), qos=1, retain=True)
        client.loop_start()
        return client
    except Exception as e:
        logging.error(f"MQTT connection failed: {str(e)}")
        return None

def main():
    PIN = port.PA6
    gpio_handler = None
    READING_INTERVAL = 1    # Her 1 saniyede bir oku
    DISPLAY_INTERVAL = 60   # Her 60 saniyede bir göster
    
    try:
        mqtt_client = setup_mqtt_client()
        if not mqtt_client:
            logging.error("Failed to setup MQTT client. Exiting...")
            return
            
        gpio_handler = GPIOHandler()
        gpio_handler.setup_pin(PIN)
        dht22_reader = DHT22Reader(
            gpio_pin=PIN,
            max_retries=2,     # Hızlı okuma için az deneme
            retry_delay=0.1,   # Kısa bekleme
            cache_time=1       # Kısa önbellek
        )

        next_reading = time.time()
        next_display = time.time() + DISPLAY_INTERVAL

        while True:
            try:
                # Sensörden veri oku
                dht22_reader.read_temperature()
                dht22_reader.read_humidity()
                
                current_time = time.time()
                
                # Her dakika ortalamaları göster
                if current_time >= next_display:
                    avg_temp, avg_humid = dht22_reader.get_averages()
                    logging.info(f"1 Dakikalık Ortalama - Sıcaklık: {avg_temp:.1f}°C, Nem: {avg_humid:.1f}%")
                    
                    # Send data to MQTT broker
                    if mqtt_client:
                        temp_payload = {
                            "value": round(avg_temp, 1),
                            "unit": "C",
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time))
                        }
                        humid_payload = {
                            "value": round(avg_humid, 1),
                            "unit": "%",
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time))
                        }
                        # Use QoS 1 for reliable delivery
                        mqtt_client.publish(MQTT_TOPIC_TEMP, json.dumps(temp_payload), qos=1)
                        mqtt_client.publish(MQTT_TOPIC_HUMID, json.dumps(humid_payload), qos=1)
                    
                    next_display = current_time + DISPLAY_INTERVAL

                # Bir sonraki okuma zamanını ayarla
                next_reading += READING_INTERVAL
                sleep_time = next_reading - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
            except RuntimeError as e:
                logging.debug(f"Okuma hatası: {str(e)}")
                time.sleep(0.5)
            except Exception as e:
                logging.error(f"Beklenmeyen hata: {str(e)}")
                time.sleep(0.5)

    except KeyboardInterrupt:
        logging.info("Program kullanıcı tarafından sonlandırıldı")
    finally:
        if gpio_handler:
            gpio_handler.cleanup()
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()

if __name__ == "__main__":
    main()
