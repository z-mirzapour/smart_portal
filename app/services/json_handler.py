import json
import os
from flask import current_app

class JSONHandler:
    @staticmethod
    def load_data(filename):
        filepath = os.path.join(current_app.config['DATA_FOLDER'], filename)
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_data(filename, data):
        filepath = os.path.join(current_app.config['DATA_FOLDER'], filename)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)