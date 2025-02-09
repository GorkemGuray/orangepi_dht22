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
    PIN = port.PA6  # Orange Pi Zero'da PA6 pini
    gpio_handler = None
    
    try:
        gpio_handler = GPIOHandler()
        gpio_handler.setup_pin(PIN)
        dht22_reader = DHT22Reader(PIN)

        while True:
            try:
                temperature = dht22_reader.read_temperature()
                humidity = dht22_reader.read_humidity()
                
                logging.info(f"Sıcaklık: {temperature:.1f}°C, Nem: {humidity:.1f}%")
                
            except RuntimeError as e:
                logging.error(f"Okuma hatası: {str(e)}")
            except Exception as e:
                logging.error(f"Beklenmeyen hata: {str(e)}")
            
            time.sleep(2)

    except KeyboardInterrupt:
        logging.info("Program kullanıcı tarafından sonlandırıldı")
    except Exception as e:
        logging.error(f"Program hatası: {str(e)}")
    finally:
        if gpio_handler:
            gpio_handler.cleanup()

if __name__ == "__main__":
    main()