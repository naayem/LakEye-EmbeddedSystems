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

    def sensor_ht(telegram, chat_id):
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            sensor_print = "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity)
            telegram.bot.sendMessage(chat_id, sensor_print)

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            telegram.bot.sendMessage(chat_id, error.args[0])
            return
        except Exception as error:
            dhtDevice.exit()
            telegram.bot.sendMessage(chat_id, error)
            raise error
