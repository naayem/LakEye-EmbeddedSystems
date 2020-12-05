def get_callback_dict(self):
    functions_dict = {
        "/start": self.start_tutorial,
        "/capture_image": self.capture_image,
        "/lights": self.led_on_off,
        "/read_temperature": self.read_sensor,
        "/lakeye": self.read_lakeye,
        "/read_battery_charge": self.read_battery_charge,
        "/start_db_creation": self.start_db_creation,
        "/stop_db_creation": self.stop_db_creation,
        "/set_db_rate": self.set_db_rate,
    }

    return functions_dict
