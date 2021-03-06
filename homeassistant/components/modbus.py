"""
components.modbus
~~~~~~~~~~~~~~~~~~~~~~~~~
Modbus component, using pymodbus (python3 branch)

typical declaration in configuration.yaml

#Modbus TCP
modbus:
    type: tcp
    host: 127.0.0.1
    port: 2020

#Modbus RTU
modbus:
    type: serial
    method: rtu
    port: /dev/ttyUSB0
    baudrate: 9600
    stopbits: 1
    bytesize: 8
    parity: N

"""
import logging

from homeassistant.const import (EVENT_HOMEASSISTANT_START,
                                 EVENT_HOMEASSISTANT_STOP)

# The domain of your component. Should be equal to the name of your component
DOMAIN = "modbus"

# List of component names (string) your component depends upon
DEPENDENCIES = []

# Type of network
MEDIUM = "type"

# if MEDIUM == "serial"
METHOD = "method"
SERIAL_PORT = "port"
BAUDRATE = "baudrate"
STOPBITS = "stopbits"
BYTESIZE = "bytesize"
PARITY = "parity"

# if MEDIUM == "tcp" or "udp"
HOST = "host"
IP_PORT = "port"

_LOGGER = logging.getLogger(__name__)

NETWORK = None
TYPE = None


def setup(hass, config):
    """ Setup Modbus component. """

    # Modbus connection type
    # pylint: disable=global-statement, import-error
    global TYPE
    TYPE = config[DOMAIN][MEDIUM]

    # Connect to Modbus network
    # pylint: disable=global-statement, import-error
    global NETWORK

    if TYPE == "serial":
        from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        NETWORK = ModbusClient(method=config[DOMAIN][METHOD],
                               port=config[DOMAIN][SERIAL_PORT],
                               baudrate=config[DOMAIN][BAUDRATE],
                               stopbits=config[DOMAIN][STOPBITS],
                               bytesize=config[DOMAIN][BYTESIZE],
                               parity=config[DOMAIN][PARITY])
    elif TYPE == "tcp":
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient
        NETWORK = ModbusClient(host=config[DOMAIN][HOST],
                               port=config[DOMAIN][IP_PORT])
    elif TYPE == "udp":
        from pymodbus.client.sync import ModbusUdpClient as ModbusClient
        NETWORK = ModbusClient(host=config[DOMAIN][HOST],
                               port=config[DOMAIN][IP_PORT])
    else:
        return False

    def stop_modbus(event):
        """ Stop Modbus service"""
        NETWORK.close()

    def start_modbus(event):
        """ Start Modbus service"""
        NETWORK.connect()
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_modbus)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, start_modbus)

    # Tells the bootstrapper that the component was succesfully initialized
    return True
