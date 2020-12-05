import telepot
from .utils import get_callback_dict
from telepot.loop import MessageLoop
from cam_stream import CamStream
import pijuice
import cv2
from sensors import Dht
from leds import LedRing
import time


class TelegramInterface:
    def __init__(self):
        self.token = "1412003340:AAFw5tuKKywNVCsaFg1cpCzhKihr3Vi7nbQ"
        self.bot = telepot.Bot(self.token)

        self.message_loop = MessageLoop(self.bot, self.message_callback).run_as_thread()

        self.cam = CamStream(0).start()

        self.led_ring = LedRing()
        self.dht = Dht()

        self.bms = pijuice.PiJuice(1, 0x14)

        self.callback_dict = get_callback_dict(self)

        self.light_status = False

    def get_bot_info(self):
        return self.bot.getMe()

    def message_callback(self, msg):
        chat_id = msg["chat"]["id"]
        self.callback_dict[msg["text"]](chat_id)

    def capture_image(self, chat_id):
        print("we send the image")
        cv2.imwrite("data/img.jpg", self.cam.read()[1])
        self.bot.sendPhoto(chat_id, open("data/img.jpg", "rb"))

    def start_tutorial(self, chat_id):
        tutorial = "Welcome to lakeye, here are the available functions:\n"
        commands_string = "\n".join(self.callback_dict)
        self.bot.sendMessage(chat_id, tutorial + commands_string)

    def led_on_off(self, chat_id):
        self.led_ring.ring_white() if self.light_status else self.led_ring.ring_off()
        self.light_status = not self.light_status

    def read_sensor(self, chat_id):
        self.bot.sendMessage(chat_id, self.dht.sensor_ht())

    def read_lakeye(self, chat_id):
        self.bot.sendMessage(chat_id, "lakeye start")
        print("we turn on the led")
        self.led_ring.ring_white()
        time.sleep(1)
        print("we send the image")
        cv2.imwrite("data/img.jpg", self.cam.read()[1])
        self.bot.sendPhoto(chat_id, open("data/img.jpg", "rb"))
        time.sleep(1)
        self.led_ring.ring_off()
        self.bot.sendMessage(chat_id, "lakeye done")

    def read_battery_charge(self, chat_id):
        charge_level = self.bms.status.GetChargeLevel()
        if charge_level["error"] != "NO_ERROR":
            error_msg = "could not get charge state: " + charge_level["error"]
            self.bot.sendMessage(chat_id, error_msg)

        else:
            state_msg = "The current charging level is " + str(charge_level["data"]) + " %"
            self.bot.sendMessage(chat_id, state_msg)
