from dht22_reader import DHT22Reader
from gpio_handler import GPIOHandler
from pyA20.gpio import port
import time
import logging

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    PIN = port.PA6
    gpio_handler = None
    READING_INTERVAL = 1    # Her 1 saniyede bir oku
    DISPLAY_INTERVAL = 60   # Her 60 saniyede bir göster
    
    try:
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
                    next_display = current_time + DISPLAY_INTERVAL

                # Bir sonraki okuma zamanını ayarla
                next_reading += READING_INTERVAL
                sleep_time = next_reading - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
            except RuntimeError as e:
                logging.debug(f"Okuma hatası: {str(e)}")  # Debug seviyesine düşürdük
                time.sleep(0.5)
            except Exception as e:
                logging.error(f"Beklenmeyen hata: {str(e)}")
                time.sleep(0.5)

    except KeyboardInterrupt:
        logging.info("Program kullanıcı tarafından sonlandırıldı")
    except Exception as e:
        logging.error(f"Program hatası: {str(e)}")
    finally:
        if gpio_handler:
            gpio_handler.cleanup()

if __name__ == "__main__":
    main()