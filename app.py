import requests

api_key = '8ab027fd7f3da3ad99c890d0210deb42'

user_input = input("Enter a city name: ")
print(user_input)

weather_data = requests.get(
    f"http://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}&units=metric")

if weather_data.json()["cod"] == "404":
    print("City does not exist. Try Harder!!")
else:
    weather = weather_data.json()["weather"][0]['main']
    temp = round(weather_data.json()["main"]["temp"])
    visibility = weather_data.json()["visibility"]
    feels_like = round(weather_data.json()["main"]["feels_like"])
    wind_speed = weather_data.json()["wind"]["speed"]
    Humidity = weather_data.json()["main"]["humidity"]

    print(f'The weather in {user_input} is: {weather}')
    print(f'The temperature in {user_input} is: {temp}°C')
    print(f'Visibility in {user_input} is: {visibility} meters')
    print(f'This shit feels like {feels_like}°C in {user_input}')
    print(f'Wind speed in {user_input} is: {wind_speed} m/s')
    print(f'Humidity in {user_input} is: {Humidity}%')
