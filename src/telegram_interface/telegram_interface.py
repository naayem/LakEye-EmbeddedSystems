import telepot
from telepot.loop import MessageLoop
from cam_stream import CamStream
import cv2
from sensors import Dht
from leds import LedRing


class TelegramInterface:
    def __init__(self):
        self.token = "1412003340:AAFw5tuKKywNVCsaFg1cpCzhKihr3Vi7nbQ"
        self.bot = telepot.Bot(self.token)

        self.message_loop = MessageLoop(self.bot, self.message_callback).run_as_thread()

        self.cam = CamStream(0).start()

        self.led_ring = LedRing()
        self.dht = Dht()

        self.light_status = False

    def get_bot_info(self):
        return self.bot.getMe()

    def message_callback(self, msg):
        chat_id = msg["chat"]["id"]

        if msg["text"] == "/capture_image":
            self.capture_image(chat_id)

        if msg["text"] == "/start":
            self.start_tutorial(chat_id)

        if msg["text"] == "/lights":
            self.led_on_off(chat_id)

        if msg["text"] == "/read_temperature":
            self.read_sensor(chat_id)

    def capture_image(self, chat_id):
        print("we send the image")
        cv2.imwrite("data/img.jpg", self.cam.read()[1])
        self.bot.sendPhoto(chat_id, open("data/img.jpg", "rb"))

    def start_tutorial(self, chat_id):
        tutorial = "Welcome to lakeye, try to take a picture with:\n /capture_image\n /lights\n /read_temperature"
        self.bot.sendMessage(chat_id, tutorial)

    def led_on_off(self, chat_id):
        self.led_ring.ring_white() if self.light_status else self.led_ring.ring_off()
        self.light_status = not self.light_status

    def read_sensor(self, chat_id):
        self.bot.sendMessage(chat_id, self.dht.sensor_ht())
