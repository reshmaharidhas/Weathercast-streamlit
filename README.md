# Weathercast streamlit [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) ![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

<p align="center">
  <a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Freshmaharidhas%2FWeathercast-streamlit"><img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Freshmaharidhas%2FWeathercast-streamlit&label=Visitors&labelColor=%2300ff00&countColor=%23000000&style=plastic&labelStyle=none" /></a>
  <img alt="GitHub file size in bytes" src="https://img.shields.io/github/size/reshmaharidhas/Weathercast-streamlit/main.py?label=file%20size">
  <img alt="GitHub Created At" src="https://img.shields.io/github/created-at/reshmaharidhas/Weathercast-streamlit">
  <img alt="GitHub License" src="https://img.shields.io/github/license/reshmaharidhas/Weathercast-streamlit">
</p>
'Weathercast streamlit' is a web app to check weather for different locations built using Python and Streamlit.

## Tech Stack💻
- Python
- Streamlit
- Pandas
- Plotly
- REST API

### API used
- WeatherAPI

### Features
- Current weather information of selected city.
  - Current temperature and description of current temperature (sunny☀️/cloudy☁️/rainy🌧️/thunder⛈️/Snow)
  - Feels-like temperature
  - Wind speed
  - Humidity
  - Dew point
  - Visibility
  - Pressure
  - UV index
  - Air Quality Index (AQI)
- Displays global cities with the same name of the city you searched in dropdown to let the user choose from.
- Displays sunrise🌅, sunset🌇, moon rise, and moon set🌕 timing of present day in the selected city.
- Present day's air pollutants and their concentrations to safeguard your respiratory health.
- Multilingual weather current condition displayed.
- Displays the hourly weather forecast for the next 2 days.
- Displays the current air pollution index with a human face depicting the air pollution level of the selected city.
- Bar chart📊 to visualize the present day's hourly UV index with varied colors.
- Search for weather data for any city around the world in a navigation friendly interface.🔍
- Interactive hourly weather forecast for the next 3 days including the present day visualized using line charts for,
  - Temperature
  - Pressure
  - Wind speed
  - Humidity
  - Chance of rain
  - Chance of snow
  - Visibility
  - Dew point
  - UV index (bar chart)
- Satellite map with location.

### Deployment Tools
- Streamlit

### Screenshots
<img width="1917" height="867" alt="image" src="https://github.com/user-attachments/assets/ed564ceb-108b-4c29-a786-6c521e52f2e7" />
<img width="1917" height="862" alt="image" src="https://github.com/user-attachments/assets/625741d3-7d8b-4805-91b7-efe103c2931a" />
<img width="1918" height="911" alt="image" src="https://github.com/user-attachments/assets/329367ca-6033-4485-ab46-479a77dcd3ae" />
<img width="1918" height="847" alt="image" src="https://github.com/user-attachments/assets/f3f8e7df-6236-44cc-8faf-13b5fb2ceafe" />
<img width="1917" height="851" alt="image" src="https://github.com/user-attachments/assets/cb2233a1-ba7b-44a7-a20b-04315f2081ee" />

### Running locally in IDE⚙️
Before running the application files in your IDE,
- Obtain API key from WeatherAPI.
- Insert your API keys into secrets.toml file at appropriate places in the code and replace with your new registered API keys = 'API_KEY'
- Run the main.py file in terminal of IDE.

### License
MIT License
