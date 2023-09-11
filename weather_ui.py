import pygame
from pygame.locals import *
import sys
from datetime import datetime, date
import requests, json
import os

# Initialize Pygame and create a screen
pygame.init()
screen = pygame.display.set_mode((320, 480))
pygame.display.set_caption('Weather UI')

def get_weather_data():
   api_key = "53d49e051998f471aaa37589c21fec91"
   base_url = "https://api.openweathermap.org/data/2.5/weather"
   lat = "45.424721"
   lon = "-75.695000"

   params = {
      'appid': api_key,
      'lat': lat,
      'lon': lon
   }

   response = requests.get(base_url, params=params)
   x = response.json()

   if "main" in x:
      y = x["main"]
      current_temperature = y["temp"]
      current_pressure = y["pressure"]
      current_humidity = y["humidity"]
      z = x["weather"]
      weather_description = z[0]["description"]

      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      today = date.today()

      weather_data = [
         'Date: ' + str(today) + ' : ' + str(current_time),
         'Temperature (C): ' + str(round(int(current_temperature) - 273.15)),
         'Atmospheric Pressure (hPA): ' + str(current_pressure),
         'Humidity (%): ' + str(current_humidity),
         'Description: ' + str(weather_description)
      ]

      return weather_data
   else:
      return ["City Not Found or API response is not as expected"]

def render_weather_data(screen, weather_data, weather_image_path, bg_image_path):
   # Load and display the background image
   bg_image = pygame.image.load(bg_image_path)
   image_width, image_height = bg_image.get_size()
   new_width = 320
   new_height = int((new_width / image_width) * image_height)
   bg_image = pygame.transform.scale(bg_image, (new_width, new_height))
   screen.blit(bg_image, (0, 0))

   # Create a card surface with a black background
   card_width, card_height = 240, 320
   card = pygame.Surface((card_width, card_height))
   card.fill((0, 0, 0))

   # Load and display the weather icon on the card
   weather_image = pygame.image.load(weather_image_path)
   weather_image = pygame.transform.scale(weather_image, (100, 100))
   card.blit(weather_image, (70, 30))

   # Display the date and time in big bold words centered under the photo on the card
   font_size = 24
   font = pygame.font.Font(None, font_size)
   date_time_text = weather_data[0]
   text = font.render(date_time_text, True, (255, 255, 255))
   text_width, text_height = text.get_size()
   card.blit(text, (120 - (text_width // 2), 140))

   # Display the temperature centered under the time on the card
   temperature_text = weather_data[1]
   text = font.render(temperature_text, True, (255, 255, 255))
   text_width, text_height = text.get_size()
   card.blit(text, (120 - (text_width // 2), 170))

   # Display the rest of the weather data on the card
   font_size = 20
   font = pygame.font.Font(None, font_size)
   y_spacing = 30
   y_position = 210

   for data_line in weather_data[2:]:
      text = font.render(data_line, True, (255, 255, 255))
      text_width, text_height = text.get_size()
      card.blit(text, (120 - (text_width // 2), y_position))
      y_position += y_spacing

   # Display the card on the main screen surface
   screen.blit(card, (40, 80))

def get_weather_images(description):
   images_folder = "images/"
   description = description.lower()

   if "broken clouds" in description:
      return images_folder + "brocken_clouds.png", images_folder + "brocken_clouds_background.jpg"
   elif "clear sky" in description:
      return images_folder + "clear_sky.png", images_folder + "clear_sky_background.jpg"
   elif "few clouds" in description:
      return images_folder + "few_clouds.png", images_folder + "few_clouds_background.jpg"
   elif "mist" in description:
      return images_folder + "mist.png", images_folder + "mist_background.png"
   elif "rain" in description:
      return images_folder + "rain.png", images_folder + "rain_background.jpg"
   elif "scattered clouds" in description:
      return images_folder + "scattered_clouds.png", images_folder + "scattered_clouds_background.jpg"
   elif "shower rain" in description:
      return images_folder + "shower_rain.png", images_folder + "shower_rain_background.jpg"
   elif "snow" in description:
      return images_folder + "snow.png", images_folder + "snow_background.jpg"
   elif "thunderstorm" in description:
      return images_folder + "thunderstorm.png", images_folder + "thunderstorm_background.jpg"

while True:
   weather_data = get_weather_data()
   weather_image_path, bg_image_path = get_weather_images(weather_data[-1])  # Get the image and background file names based on the description
   render_weather_data(screen, weather_data, weather_image_path, bg_image_path)
   pygame.display.flip()

   for event in pygame.event.get():
      if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
         pygame.quit()
         sys.exit()