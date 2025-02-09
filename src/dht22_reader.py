from dht import DHT, DHTResult
from time import sleep

class DHT22Reader:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.dht = DHT(pin=gpio_pin, sensor=22)

    def read_temperature(self):
        MAX_RETRIES = 3
        for _ in range(MAX_RETRIES):
            result = self.dht.read()
            if result.is_valid():
                return result.temperature
            sleep(1)  # Yeniden denemeden önce bekle
        raise RuntimeError("Sıcaklık okunamadı")

    def read_humidity(self):
        MAX_RETRIES = 3
        for _ in range(MAX_RETRIES):
            result = self.dht.read()
            if result.is_valid():
                return result.humidity
            sleep(1)  # Yeniden denemeden önce bekle
        raise RuntimeError("Nem okunamadı")