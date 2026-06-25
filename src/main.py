import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

if api_key:
    print(f"API key succesvol geladen: {api_key[:4]}...")
else:
    print("Fout: kon niet vinden")

import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox,
)
from PySide6.QtCore import QTimer, Qt



class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("What's the weather?")
        self.resize(400, 300)

        self.api_key = api_key
       
        # QTimer voor de een seconde laadtijd bij het ophalen van gegevens.
        self.zoek_timer = QTimer(self)
        self.zoek_timer.setSingleShot(True)
        self.zoek_timer.timeout.connect(self.get_weather)

        # GUI elementen
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Vul jouw stad in...")
        self.city_input.returnPressed.connect(self.get_weather)
        self.city_input.textChanged.connect(self.user_typing)

        self.search_button = QPushButton("Zoek")
        self.search_button.clicked.connect(self.get_weather)
        
        # Labels voor weergegevens
        self.weather_label = QLabel("Weer: --")
        self.temp_label = QLabel("Temperatuur: --")
        self.feels_like_label = QLabel("Voelt als: --")
        self.visibility_label = QLabel("Zichtbaarheid: --")
        self.wind_label = QLabel("Windsnelheid: --")
        self.humidity_label = QLabel("Luchtvochtigheid: --")

        self.initUI()

    def user_typing(self):
        self.zoek_timer.stop()
        self.zoek_timer.start(1500)

    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # Input en knop horizontaal
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)
        layout.addLayout(input_layout)

        # Resultaat labels
        layout.addWidget(self.weather_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.temp_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feels_like_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.visibility_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.wind_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.humidity_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)
    
    def get_weather(self):
        self.zoek_timer.stop()

        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Fout", "Voer een stadnaam in.")
            return

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") == "404":
                QMessageBox.information(self, "Niet gevonden", f"Heh? Waar ligt '{city}'?. Try again!")
                return

            # Data ophalen
            weather = data["weather"][0]["main"]
            temp = round(data["main"]["temp"])
            feels_like = round(data["main"]["feels_like"])
            visibility = data["visibility"] / 1000  # Verandert meter naar km
            wind_speed = data["wind"]["speed"]
            humidity = data["main"]["humidity"]

            # Labels bijwerken
            self.weather_label.setText(f"Weer: {weather}")
            self.temp_label.setText(f"Temperatuur: {temp}°C")
            self.feels_like_label.setText(f"Voelt als: {feels_like}°C")
            self.visibility_label.setText(f"Zichtbaarheid: {visibility:.2f} km")  # Show visibility in km
            self.wind_label.setText(f"Windsnelheid: {wind_speed} m/s")
            self.humidity_label.setText(f"Luchtvochtigheid: {humidity}%")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Netwerkfout", f"Kan geen verbinding maken: {e}")
        except KeyError:
            QMessageBox.critical(self, "Datafout", "Onverwachte respons van de API.")

if __name__ == "__main__":
    print("1. app word gemaakt...")
    app = QApplication(sys.argv)

    print("2. venster word geladen...")
    window = WeatherApp()

    print("3. venster show() word aangeroepen...")
    window.show()

    print("4. app start...")
    sys.exit(app.exec())
    
