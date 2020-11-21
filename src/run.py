#!  /home/pi/.cache/pypoetry/virtualenvs/stream-video-n8sUmWYC-py3.7/bin/python

from telegram_interface import TelegramInterface


def main():
    print("hey vincent")

    interface = TelegramInterface()

    print(interface.get_bot_info())

    while True:
        pass


if __name__ == "__main__":
    main()
