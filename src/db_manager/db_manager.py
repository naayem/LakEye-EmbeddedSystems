import time
import os
from threading import Thread


class DBManager:
    def __init__(self, db_path="data/DB", rate=10):
        self.db_id = str(int(time.time()))
        self.db_path = db_path + "/DB_" + self.db_id + "/"

        try:
            os.mkdir(self.db_path)
        except FileExistsError:
            print("DB already exists!!")

        self.rate = rate
        self.running = False

    def set_rate(self, rate):
        self.rate = rate

    def get_rate(self):
        return self.rate

    def get_db_path(self):
        return self.db_path

    def get_db_id(self):
        return "/DB_" + self.db_id

    def start(self, telegram_inteface):
        self.running = True
        Thread(target=self.update, args=([telegram_inteface])).start()

    def stop(self, telegram_interface):
        self.running = False

    def update(self, telegram_inteface):
        while self.running:
            start_time = time.time()
            img_path = self.db_path + "image_" + str(int(start_time)) + ".jpg"
            telegram_inteface.read_lakeye(None, None, img_path=img_path)
            elapsed = time.time() - start_time

            time.sleep(self.rate - elapsed)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
