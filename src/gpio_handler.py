from pyA20.gpio import gpio

class GPIOHandler:
    def __init__(self):
        gpio.init()

    def setup_pin(self, pin_number):
        gpio.setcfg(pin_number, gpio.OUTPUT)
        gpio.pullup(pin_number, gpio.PULLUP)

    def cleanup(self):
        gpio.cleanup()