import telepot
from .utils import get_callback_dict
from telepot.loop import MessageLoop
from cam_stream import CamStream
from db_manager import DBManager, zipdir
import pijuice
import cv2
from sensors import Dht
from leds import LedRing
from datetime import datetime
import time
import zipfile
import os
import shutil


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

        self.light_status = True

        self.db_manager = DBManager(rate=10)

        self.db_creation = False

    def get_bot_info(self):
        return self.bot.getMe()

    def message_callback(self, msg):
        chat_id = msg["chat"]["id"]
        text = msg["text"].split()
        command = text[0]
        args = text[1:]

        if command in self.callback_dict:
            self.callback_dict[command](chat_id, args)

    # All callbacks
    def capture_image(self, chat_id, args):
        print("we send the image")
        cv2.imwrite("data/img.jpg", self.cam.read()[1])
        self.bot.sendPhoto(chat_id, open("data/img.jpg", "rb"))

    def start_tutorial(self, chat_id, args):
        tutorial = "Welcome to lakeye, here are the available functions:\n"
        commands_string = "\n".join(self.callback_dict)
        self.bot.sendMessage(chat_id, tutorial + commands_string)

    def led_on_off(self, chat_id, args):
        self.led_ring.ring_white() if self.light_status else self.led_ring.ring_off()
        self.light_status = not self.light_status

    def read_sensor(self, chat_id, args):
        self.bot.sendMessage(chat_id, self.dht.sensor_ht())

    def read_lakeye(self, chat_id, args, img_path="data/img.jpg"):
        if chat_id:
            self.bot.sendMessage(chat_id, "lakeye start")
            print("we turn on the led")

        self.led_ring.ring_white()
        time.sleep(1)

        if chat_id:
            print("we send the image")

        cv2.imwrite(img_path, self.cam.read()[1])
        if chat_id:
            self.bot.sendPhoto(chat_id, open(img_path, "rb"))

        time.sleep(1)
        self.led_ring.ring_off()
        if chat_id:
            self.bot.sendMessage(chat_id, "lakeye done")

    def read_battery_charge(self, chat_id, args):
        charge_level = self.bms.status.GetChargeLevel()
        if charge_level["error"] != "NO_ERROR":
            error_msg = "could not get charge state: " + charge_level["error"]
            self.bot.sendMessage(chat_id, error_msg)

        else:
            state_msg = "The current charging level is " + str(charge_level["data"]) + " %"
            self.bot.sendMessage(chat_id, state_msg)

    def start_db_creation(self, chat_id, args):
        if self.db_creation is False:
            self.bot.sendMessage(chat_id, "we started the DB at " + str(datetime.now()))
            self.db_creation = True
            self.db_manager.start(self)

    def stop_db_creation(self, chat_id, args):
        if self.db_creation is True:
            self.bot.sendMessage(chat_id, "Saving...")
            self.db_creation = False
            self.db_manager.stop(self)

            zip_path = "data/zip" + self.db_manager.get_db_id() + ".zip"
            zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
            zipdir(self.db_manager.get_db_path(), zipf)
            zipf.close()
            time.sleep(1)
            self.bot.sendDocument(chat_id, open(zip_path, "rb"))

            shutil.rmtree(self.db_manager.get_db_path())
            os.remove(zip_path)

    def set_db_rate(self, chat_id, args):
        try:
            new_rate = float(args[0])
        except Exception:
            self.bot.sendMessage(chat_id, "no float value given!!")
            return

        self.db_manager.set_rate(new_rate)
        self.bot.sendMessage(chat_id, "we set the new rate to: " + str(self.db_manager.get_rate()))
