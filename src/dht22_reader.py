from dht import DHT, DHTResult
import time
from collections import deque
from statistics import mean

class DHT22Reader:
    def __init__(self, gpio_pin, max_retries=3, retry_delay=0.1, cache_time=2):
        self.gpio_pin = gpio_pin
        self.dht = DHT(pin=gpio_pin, sensor=22)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.cache_time = cache_time
        self._last_valid_read = None
        self._last_temperature = None
        self._last_humidity = None
        self._last_read_time = 0
        
        # Son 1 dakikalık verileri tutmak için
        self.temp_history = deque(maxlen=60)  # 60 saniyelik veri
        self.humid_history = deque(maxlen=60)  # 60 saniyelik veri
        self.last_average_time = 0

    def _should_use_cache(self):
        return (time.time() - self._last_read_time) < self.cache_time

    def _read_with_retry(self):
        if self._should_use_cache() and self._last_valid_read is not None:
            return self._last_valid_read

        for attempt in range(self.max_retries):
            result = self.dht.read()
            if result.is_valid():
                self._last_valid_read = result
                self._last_read_time = time.time()
                self._last_temperature = result.temperature
                self._last_humidity = result.humidity
                return result
            
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
        
        # Eğer son geçerli okuma varsa ve 10 saniyeden eski değilse onu kullanalım
        if self._last_valid_read is not None and (time.time() - self._last_read_time) < 10:
            return self._last_valid_read
            
        raise RuntimeError("Sensör okunamadı")

    def read_temperature(self):
        try:
            result = self._read_with_retry()
            self.temp_history.append(result.temperature)
            return result.temperature
        except Exception as e:
            if self._last_temperature is not None:
                return self._last_temperature
            raise RuntimeError("Sıcaklık okunamadı")

    def read_humidity(self):
        try:
            result = self._read_with_retry()
            self.humid_history.append(result.humidity)
            return result.humidity
        except Exception as e:
            if self._last_humidity is not None:
                return self._last_humidity
            raise RuntimeError("Nem okunamadı")

    def get_averages(self):
        """Son 1 dakikalık verilerin ortalamasını döndürür"""
        if not self.temp_history or not self.humid_history:
            raise RuntimeError("Henüz yeterli veri yok")
            
        avg_temp = mean(self.temp_history)
        avg_humid = mean(self.humid_history)
        self.last_average_time = time.time()
        
        return avg_temp, avg_humid