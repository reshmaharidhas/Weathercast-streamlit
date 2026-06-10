import time
import pandas as pd
import requests
import plotly.express as px
from datetime import date, timedelta
import streamlit as st

headers = {"authorization":st.secrets["API_KEY"],
           "content-type":"application/json"}

st.set_page_config(layout="wide",page_title="WeatherCast web",page_icon="🌤️")
st.session_state["is_unit_celsius"] = True
# Fetching API key for Weatherapi website from secrets.
API_KEY = st.secrets["API_KEY"]

# Caching fetched data for 1 month from API.
@st.cache_data(ttl=2592000)
def get_multiple_locations_list(ans):
    multiple_locations_url = f"https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={ans}"
    multiple_locations_response = requests.get(multiple_locations_url)
    return multiple_locations_response

col1, col2, col3 = st.columns([0.7,0.1,0.2],vertical_alignment="bottom")
with col1:
    with st.container():
        st.markdown("# ☀️:blue[WeatherCast]⛈️", text_alignment="center")
with col2:
    ans = st.selectbox("Choose city🔍",options=["Dubai","Auckland","Berlin","Abu Dhabi","New York","Paris"],accept_new_options=True)
    multiple_locations_response = get_multiple_locations_list(ans)
    if multiple_locations_response.status_code==200:
        multiple_locations_response = multiple_locations_response.json()
        multiple_locations_name_region_country = []
        multiple_locations_lat_lon = []
        # Getting all list of cities with the searched name around the world.
        for every_city in multiple_locations_response:
            name_region_country = every_city["name"]+", "+every_city["region"]+", "+every_city["country"]
            multiple_locations_name_region_country.append(name_region_country)
            multiple_locations_lat_lon.append([every_city["lat"],every_city["lon"]])
        with col3:
            exact_location = st.selectbox("Choose exact location📍",options=multiple_locations_name_region_country)
            selected_exact_location_index = multiple_locations_name_region_country.index(exact_location)
            selected_latitude_longitude = multiple_locations_lat_lon[selected_exact_location_index]
    else:
        st.write("Unable to fetch multiple locations")


# Caching fetched data from API for 1 hour.
@st.cache_data(ttl=3600)
def get_current_weather(selected_latitude_longitude):
    lat = selected_latitude_longitude[0]
    lon = selected_latitude_longitude[1]
    current_weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}&aqi=yes"
    time.sleep(0.2)
    current_weather_response = requests.get(current_weather_url)
    return current_weather_response

# Caching fetched data from API for 1 hour.
@st.cache_data(ttl=3600)
def get_weather_forecast(selected_latitude_longitude):
    lat = selected_latitude_longitude[0]
    lon = selected_latitude_longitude[1]
    forecast_url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat},{lon}&days=5&aqi=yes&alerts=yes"
    time.sleep(0.1)
    forecast_response = requests.get(forecast_url)
    return forecast_response

@st.cache_data(ttl=3600)
def get_yesterday_weather(selected_latitude_longitude):
    lat = selected_latitude_longitude[0]
    lon = selected_latitude_longitude[1]
    yesterday = date.today() - timedelta(days=1)
    yesterday_weather_url = f"https://api.weatherapi.com/v1/history.json?key={API_KEY}&q={lat},{lon}&dt={yesterday}"
    time.sleep(0.1)
    yesterday_weather_response = requests.get(yesterday_weather_url)
    return yesterday_weather_response

def get_uv_status(uv_index_arr):
    uv_index_status = []
    for curr_uv_index in uv_index_arr:
        if curr_uv_index<=2:
            uv_index_status.append("Low risk")
        elif curr_uv_index>=2 and curr_uv_index<=5:
            uv_index_status.append("Moderate risk")
        elif curr_uv_index>=5 and curr_uv_index<=7:
            uv_index_status.append("High risk")
        elif curr_uv_index>=7 and curr_uv_index<11:
            uv_index_status.append("Very high risk")
        elif curr_uv_index>=11:
            uv_index_status.append("Extreme risk")
    return uv_index_status

response = get_current_weather(selected_latitude_longitude)
forecast_response = get_weather_forecast(selected_latitude_longitude)
yesterday_weather_response= get_yesterday_weather(selected_latitude_longitude)
# Current weather data fetching.
if response.status_code==200:
    response = response.json()
else:
    st.write("No Weather data fetched. Status code=",response.status_code)
# Forecast data fetching.
if forecast_response.status_code==200:
    forecast_response = forecast_response.json()
else:
    st.write("Unable to fetch forecast data. Status=",forecast_response.status_code)
# historical yesterday weather data
if yesterday_weather_response.status_code==200:
    yesterday_weather_data = yesterday_weather_response.json()
else:
    st.write("Unable to fetch historical data. Status=",yesterday_weather_response.status_code)

# Tabs
current_weather_tab,forecast_tab,history_tab = st.tabs(["☀️Today's weather","📈Forecast","📒Historical weather"])
# Current weather tab
with current_weather_tab:
    with st.container(gap=None):
        current_weather_col1, current_weather_col2 = st.columns([0.4,0.6],border=True)
        with current_weather_col1:
            with st.container(height="content",horizontal=False,horizontal_alignment="center"):
                current_weather_col1_subcol_1,current_weather_col1_subcol_2 = st.columns(2,gap=None,vertical_alignment="center")
                with current_weather_col1_subcol_1:
                    city_name = response["location"]["name"]
                    country_name = response["location"]["country"]
                    curr_temperature_c = response["current"]["temp_c"]
                    feels_like_temp_c = response["current"]["feelslike_c"]
                    temp_condition = response["current"]["condition"]["text"]
                    temperature_image = response["current"]["condition"]["icon"]
                    st.markdown(f"#### 📍{city_name}")
                    st.markdown(f"###### {country_name}")
                    st.markdown(f"# {curr_temperature_c}°C")
                    st.markdown(f"###### Feels like {feels_like_temp_c}°C")
                    st.markdown(f"##### {temp_condition}")
                with current_weather_col1_subcol_2:
                    wind_speed_mph = response["current"]["wind_mph"]
                    pressure_mb = response["current"]["pressure_mb"]
                    precipitation_mm = response["current"]["precip_mm"]
                    humidity = response["current"]["humidity"]
                    dew_point_c = response["current"]["dewpoint_c"]
                    uv_current = response["current"]["uv"]
                    visibility = response["current"]["vis_km"]
                    st.markdown(f"###### Wind speed: {wind_speed_mph} mph")
                    st.markdown(f"###### Pressure: {pressure_mb} hPa")
                    st.markdown(f"###### Precipitation: {precipitation_mm} mm")
                    st.markdown(f"###### Humidity: {humidity}%")
                    st.markdown(f"###### Dewpoint: {dew_point_c}°C")
                    st.markdown(f"###### UV index: {uv_current}")
                    st.markdown(f"###### Visibility: {visibility} km")
                with st.container(horizontal=True):
                    with st.container(gap=None, border=True,width="content",horizontal=True,horizontal_alignment="center"):
                        aqi_index = response["current"]["air_quality"]["us-epa-index"]
                        st.write("AQI")
                        st.markdown(f"# {aqi_index}")
                    with st.container(gap=None,border=True,width="content"):
                        air_quality_dict = {1:"Good",2:"Moderate",3:"Unhealthy for sensitive group",4:"Unhealthy",5:"Very Unhealthy",6:"Hazardoud"}
                        air_quality = air_quality_dict.get(aqi_index)
                        st.write("Air quality")
                        if aqi_index==1:
                            st.markdown(f"## :green[{air_quality}]")
                        elif aqi_index==2:
                            st.markdown(f"## :yellow[{air_quality}]")
                        elif aqi_index==3:
                            st.markdown(f"## :orange[{air_quality}]")
                        elif aqi_index==4 or aqi_index==5:
                            st.markdown(f"## :red[{air_quality}]")
                        elif aqi_index==6:
                            st.markdown(f"## :violet[{air_quality}]")

                    with st.container(border=True,horizontal=True,horizontal_alignment="center"):
                        if aqi_index==1:
                            st.image("assets/images/face1-removebg-preview.png",width=90)
                        elif aqi_index==2:
                            st.image("assets/images/face2-removebg-preview.png",width=90)
                        elif aqi_index==3 or aqi_index==4:
                            st.image("assets/images/face3-removebg-preview.png",width=90)
                        elif aqi_index==5:
                            st.image("assets/images/face4-removebg-preview.png",width=90)
                        elif aqi_index==6:
                            st.image("assets/images/face5-removebg-preview.png",width=90)
                with st.container(horizontal=True):
                    with st.container(border=True,width="content"):
                        co = response["current"]["air_quality"]["co"]
                        no2 = response["current"]["air_quality"]["no2"]
                        o3 = response["current"]["air_quality"]["o3"]
                        so2 = response["current"]["air_quality"]["so2"]
                        pm2_5 = response["current"]["air_quality"]["pm2_5"]
                        pm10 = response["current"]["air_quality"]["pm10"]
                        st.markdown("##### 😷Air Pollutants")
                        st.write(f"Carbon Monoxide: {co} μg/m3")
                        st.write(f"Nitrogen Dioxide: {no2} μg/m3")
                        st.write(f"Ozone: {o3} μg/m3")
                        st.write(f"Sulphur dioxide: {so2} μg/m3")
                        st.write(f"PM 2.5: {pm2_5} μg/m3")
                        st.write(f"PM10: {pm10} μg/m3")
                    with st.container(horizontal=True):
                        with st.container(border=True,width="stretch",horizontal=True,horizontal_alignment="center"):
                            sunrise = forecast_response["forecast"]["forecastday"][0]["astro"]["sunrise"]
                            st.write("🌅 Sunrise")
                            st.markdown(f"###### {sunrise}")
                        with st.container(border=True,width="stretch",horizontal=True,horizontal_alignment="center"):
                            sunset = forecast_response["forecast"]["forecastday"][0]["astro"]["sunset"]
                            st.write("🌇 Sunset")
                            st.markdown(f"###### {sunset}")
                        with st.container(border=True,width="stretch",horizontal=True,horizontal_alignment="center"):
                            moonrise = forecast_response["forecast"]["forecastday"][0]["astro"]["moonrise"]
                            st.write("🌜 Moonrise")
                            st.markdown(f"###### {moonrise}")
                        with st.container(border=True,width="stretch",horizontal=True,horizontal_alignment="center"):
                            moonset = forecast_response["forecast"]["forecastday"][0]["astro"]["moonset"]
                            st.write("🌛 Moonset")
                            st.markdown(f"###### {moonset}")

        with current_weather_col2:
            with st.container(gap=None):
                with st.container():
                    today_temperature = list()
                    for current_hour in range(24):
                        today_temperature.append(forecast_response["forecast"]["forecastday"][0]["hour"][current_hour]["temp_c"])
                    weather_temp = pd.DataFrame({"hour":list(range(0,24)),"temp_c":today_temperature})
                    fig = px.line(weather_temp,x="hour",y="temp_c",markers=True,title="🌡️Today Temperature Hourly forecast",labels={"temp_c":"Temperature (Celsius)","hour":"Hour"},color_discrete_sequence=["orange"])
                    fig.update_traces(marker=dict(size=12, symbol="circle-dot"))
                    fig.update_layout(title_x=0.3)
                    fig.update_xaxes(tickmode="linear")
                    st.plotly_chart(fig,key="today_temperature_hourly_forecast")
                with st.container():
                    arr = list()
                    for current_hour in range(24):
                        arr.append(forecast_response["forecast"]["forecastday"][0]["hour"][current_hour]["uv"])
                    uv_status = get_uv_status(arr)
                    uv_data = pd.DataFrame({"hour":list(range(24)),"uv_index": arr,"uv_status":uv_status})
                    fig = px.bar(uv_data,y="uv_index",x="hour",title="🔆UV index today",color="uv_status",
                                  labels={"uv_index": "UV index", "hour": "Hour","uv_status":"UV status"},
                                 color_discrete_map={'Low risk': 'lime','Moderate risk': 'yellow',
                                'High risk':'orange',"Very high risk":"red","Extreme risk":"purple"},
                                 category_orders={"uv_status":["Low risk","Moderate risk","High risk","Very high risk","Extreme risk"]})
                    fig.update_layout(title_x=0.3)
                    fig.update_xaxes(tickmode="linear")
                    st.plotly_chart(fig)
        st.markdown(f"Last updated on {response['current']['last_updated']} *({response['location']['tz_id']})*")

# 3 days weather forecasting displayed in tab.
with forecast_tab:
    with st.container(border=True):
        forecast_selected = st.selectbox("Choose variable to forecast for next 3 days",options=["Temperature","Wind speed","Pressure","Humidity","UV index","Dew point","Visibility","Chance of rain","Chance of snow"])
        day_0_date = forecast_response["forecast"]["forecastday"][0]["date"]
        day_1_date = forecast_response["forecast"]["forecastday"][1]["date"]
        day_2_date = forecast_response["forecast"]["forecastday"][2]["date"]
        selectbox_options = ["Temperature","Wind speed","Pressure","Humidity","UV index","Dew point","Visibility","Chance of rain","Chance of snow"]
        selectbox_index = selectbox_options.index(forecast_selected)
        weather_variables = list(["temp_c","wind_mph","pressure_mb","humidity","uv","dewpoint_c","vis_miles","chance_of_rain","chance_of_snow"])
        y_axis_label_options = list(["Temperature (Celsius)","Wind speed (mph)","Pressure (millibars)","Humidity (%)","UV index","Dew point (Celsius)","Visibility (miles)","Chance of rain (%)","Chance of snow (%)"])
        marker_symbols = list(["circle-open","circle","circle-open","cross",None,"diamond-tall","hexagon2-dot","star-diamond","hexagram"])
        data_array_day_0 = list()
        data_array_day_1 = list()
        data_array_day_2 = list()
        for current_hour in range(24):
            data_array_day_0.append(
                forecast_response["forecast"]["forecastday"][0]["hour"][current_hour][weather_variables[selectbox_index]])
            data_array_day_1.append(
                forecast_response["forecast"]["forecastday"][1]["hour"][current_hour][weather_variables[selectbox_index]])
            data_array_day_2.append(
                forecast_response["forecast"]["forecastday"][2]["hour"][current_hour][weather_variables[selectbox_index]])
        df = pd.DataFrame(
            {"hour": list(range(0, 24)), "day_0": data_array_day_0, "day_1": data_array_day_1,
             "day_2": data_array_day_2})
        df_melted = df.melt(id_vars="hour", var_name="Date", value_name=selectbox_options[selectbox_index])
        df_melted["Date"] = df_melted["Date"].replace(
            {"day_0": day_0_date, "day_1": day_1_date, "day_2": day_2_date})
        if selectbox_options[selectbox_index]!="UV index":
            fig = px.line(df_melted, x="hour", y=selectbox_options[selectbox_index], color="Date", markers=True,title=selectbox_options[selectbox_index],
                      labels={selectbox_options[selectbox_index]: y_axis_label_options[selectbox_index], "hour": "Hour"})
            fig.update_traces(marker=dict(size=12, symbol=marker_symbols[selectbox_index]))
        else:
            fig = px.bar(df_melted, x="hour", y=selectbox_options[selectbox_index], color="Date",title=selectbox_options[selectbox_index],
                          labels={selectbox_options[selectbox_index]: "UV index", "hour": "Hour"})
        fig.update_layout(title_x=0.5)
        fig.update_xaxes(tickmode="linear")
        st.plotly_chart(fig)

# Historical weather data
with history_tab:
    with st.container(border=True):
        # selectbox to choose variable to view yesterday's weather.
        yesterday_var_selected = st.selectbox("Choose variable to view yesterday's weather data",options=["Temperature","Wind speed","Pressure","Humidity","UV index","Dew point","Visibility","Chance of rain","Chance of snow"])
        # Getting date of yesterday.
        yesterday = date.today() - timedelta(days=1)
        selectbox_options = ["Temperature","Wind speed","Pressure","Humidity","UV index","Dew point","Visibility","Chance of rain","Chance of snow"]
        selectbox_index = selectbox_options.index(yesterday_var_selected)
        weather_variables = list(["temp_c","wind_mph","pressure_mb","humidity","uv","dewpoint_c","vis_miles","chance_of_rain","chance_of_snow"])
        y_axis_label_options = list(["Temperature (Celsius)","Wind speed (mph)","Pressure (millibars)","Humidity (%)","UV index","Dew point (Celsius)","Visibility (miles)","Chance of rain (%)","Chance of snow (%)"])
        marker_symbols = list(["circle-open","circle","circle-open","cross",None,"diamond-tall","hexagon2-dot","star-diamond","hexagram"])
        data_array_previous_day = list()
        for current_hour in range(24):
            data_array_previous_day.append(
                yesterday_weather_data["forecast"]["forecastday"][0]["hour"][current_hour][weather_variables[selectbox_index]])
        df = pd.DataFrame({"hour": list(range(0, 24)), "day_0": data_array_previous_day})
        df_melted = df.melt(id_vars="hour", var_name="Date", value_name=selectbox_options[selectbox_index])
        df_melted["Date"] = df_melted["Date"].replace({"day_0": yesterday})
        if selectbox_options[selectbox_index]!="UV index":
            fig = px.line(df_melted, x="hour", y=selectbox_options[selectbox_index], color="Date", markers=True,title=selectbox_options[selectbox_index],
                      labels={selectbox_options[selectbox_index]: y_axis_label_options[selectbox_index], "hour": "Hour"},color_discrete_sequence=["magenta"])
            fig.update_traces(marker=dict(size=12, symbol=marker_symbols[selectbox_index]))
        else:
            fig = px.bar(df_melted, x="hour", y=selectbox_options[selectbox_index], color_discrete_sequence=["coral"],title=selectbox_options[selectbox_index],
                          labels={selectbox_options[selectbox_index]: "UV index", "hour": "Hour"})
        fig.update_layout(title_x=0.5)
        fig.update_xaxes(tickmode="linear")
        st.plotly_chart(fig)

# Outside tabs
