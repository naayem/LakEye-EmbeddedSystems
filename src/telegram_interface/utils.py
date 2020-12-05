def get_callback_dict(self):
    functions_dict = {
        "/capture_image": self.capture_image,
        "/start": self.start_tutorial,
        "/lights": self.led_on_off,
        "/read_temperature": self.read_sensor,
        "/lakeye": self.read_lakeye,
        "/read_battery_charge": self.read_battery_charge,
    }

    return functions_dict
