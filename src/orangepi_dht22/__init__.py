"""
Orange Pi DHT22 Temperature and Humidity Monitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A library for reading temperature and humidity data from DHT22 sensors
connected to Orange Pi Zero boards.
"""

from .dht import DHT, DHTResult
from .dht22_reader import DHT22Reader
from .gpio_handler import GPIOHandler

__version__ = '1.0.0'
__all__ = ['DHT22Reader', 'GPIOHandler']
