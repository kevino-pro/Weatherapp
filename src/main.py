import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("What's the weather")
        self.setMinimumWidth(400)

        self.api_key = '8ab027fd7f3da3ad99c890d0210deb42'
        # GUI elementen
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Vul jouw stad in...")

        self.search_button = QPushButton("Zoek")
        self.search_button.clicked.connect(self.get_weather)

        # Labels voor weergegevens
        self.weather_label = QLabel("Weer: --")
        self.temp_label = QLabel("Temperatuur: --")
        self.feels_like_label = QLabel("Voelt als: --")
        self.visibility_label = QLabel("Zichtbaarheid: --")
        self.wind_label = QLabel("Windsnelheid: --")
        self.humidity_label = QLabel("Luchtvochtigheid: --")

        # Layout opbouwen
        layout = QVBoxLayout()

        # Input en knop horizontaal
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)
        layout.addLayout(input_layout)

        # Resultaat labels
        layout.addWidget(self.weather_label)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.feels_like_label)
        layout.addWidget(self.visibility_label)
        layout.addWidget(self.wind_label)
        layout.addWidget(self.humidity_label)

        layout.addStretch()
        self.setLayout(layout)

    def get_weather(self):
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
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())