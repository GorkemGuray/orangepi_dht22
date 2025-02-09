from pyA20.gpio import gpio

class GPIOHandler:
    def __init__(self):
        gpio.init()
        self.initialized_pins = set()

    def setup_pin(self, pin_number):
        gpio.setcfg(pin_number, gpio.OUTPUT)
        gpio.pullup(pin_number, gpio.PULLUP)
        self.initialized_pins.add(pin_number)

    def cleanup(self):
        # pyA20'de cleanup metodu yok, manuel olarak pinleri sıfırlayalım
        for pin in self.initialized_pins:
            try:
                gpio.setcfg(pin, gpio.INPUT)  # Pini input moduna al
                gpio.pullup(pin, 0)           # Pull-up'ı kapat
            except:
                pass
        self.initialized_pins.clear()