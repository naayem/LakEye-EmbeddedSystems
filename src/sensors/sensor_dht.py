import board
import adafruit_dht

#  Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

#  you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
#  This may be necessary on a Linux single board computer like the Raspberry Pi,
#  but it will not work in CircuitPython.
#  dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)


class Dht:
    def __init__(self):
        self.variable = 0

    def sensor_ht(self):
        sensor_print = ""
        while not sensor_print:
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = dhtDevice.humidity
                sensor_print = "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])

            except Exception:
                sensor_print = "Failed to get temperature."
        return sensor_print
