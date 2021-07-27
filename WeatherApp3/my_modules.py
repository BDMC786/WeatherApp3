def fixnyc(city): #MIGRATED
    nyc_alts = ["new york" , "new york, ny" , "new york city" "new york, new york" , "new york ny" , "new york new york"]
    if city.lower() in nyc_alts:
        city = "manhattan"
    bayonne_alts = ["bayonne", "bayonne "]
    if city.lower() in bayonne_alts:
        city = "Bayonne, NJ"
    
    return city

def getlocation(city): #MIGRATED
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(timeout=300, user_agent="WeatherApp")
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude
    print(location)
    
    #Get location name from geopy
    city_mod = f"{location}".split(", ") 
    place = f'{city_mod[0]}, {city_mod[2]}'

    return(place, latitude, longitude)

def get_url(latitude, longitude): #MIGRATED

    key = "2f2ce2142c650c2e629355e66b97e530" 
    # key = "5fc1f583fa2e15d8a27208e502ba5fb0" #Dark Sky
    #Get URL for API call to DarkSky
    # url = f'https://api.darksky.net/forecast/{key}/{latitude},{longitude}'
    #Get URL for API call to OpenWeatherAPI
    url = f'http://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&units=imperial&appid={key}'
    print(f'the url is {url}')

    return url



def getdata(url): #MIGRATED 
    import requests
    #Make API Call
    response = requests.get(url)
    response_json = response.json()

    #Get timezone offset
    # x = response_json["offset"]
    # time_adjust = (int(x)) * 3600

    time_adjust = int(response_json["timezone_offset"]) 
    print(f'time adjust = {time_adjust}')
    
    return (response_json, time_adjust)

def getcurrent(current_weather, time_adjust): #
    from datetime import datetime as dt
    #Pull data from current conditions
    current_dict = {}
    current_list_try = ["feels_like",  "clouds", "humidity", "rain", "snow", "precipAccumulation",  "temp", "dt", "uvi", "wind_speed"]
    for elements in current_list_try:
        if elements in current_weather:
            current_dict[elements] = current_weather[elements]
    
     
    
    #Adjusts Time to local time
    try:
        current_dict["dt"] = current_dict["dt"] + time_adjust
    except:
        print("current_dict[dt] = current_dict[dt] + time_adjust failed")
    
    #Gets the Day of the week and the time in AM PM format
    try:
        current_dict["dt"] = f"{dt.utcfromtimestamp(current_dict['dt']).strftime('%A')} {dt.utcfromtimestamp(current_dict['dt']).strftime('%r')}".lstrip("0").replace(" 0", " ")
    except:
        print("current_dict[dt] format failed")
    #Correct Formats Current
    try:
        current_dict["feels_like"] = f'{round(current_dict["feels_like"])} °F' #Round 
    except:
        print("current_dict[feels_like] FAILED")
    try:
        current_dict["clouds"] = f'{round(current_dict["clouds"])}%' #Percentage    
    except:
        print("current_dict[clouds] FAILED")
    try:
        current_dict["uvi"] = f'{round(current_dict["uvi"])}'     
    except:
        print("current_dict[uvi] FAILED")
    try:
        current_dict["humidity"] = f'{round(current_dict["humidity"])}%' 
    except:
        print("current_dict[humidity] FAILED")
    try:    
        current_dict["temp"] = f'{round(current_dict["temp"])} °F'
    except:
        print("current_dict[temp] FAILED")
    print(current_dict)
    if "snow" in current_dict:
        current_dict["snow"] = f'Snowfall Accumulation: {current_dict["snow"]} Inches'
    current_dict["wind_speed"] = f'{round(current_dict["wind_speed"])} MPH'
    try:
        current_dict["summary"] = current_weather["weather"][0]["description"]
    except:
        print("current_dict[summary] FAILED")
    try:
        current_dict["rain"] = current_dict["rain"]["1h"]
    except:
        print('current_dict["rain"] FAILED')
    print("END OF CURRENT")

    return current_dict

def gethourly(hourly_weather, time_adjust): #
    from datetime import datetime as dt
    #Pull data from Hourly Conditions
    
    print(hourly_weather[0]["weather"])
    hourly_list = []
    hourly_elements_try = ["feels_like", "clouds", "humidity", "rain", "snow", "pop", 
                     "temp", "dt", "uvi", "wind_speed" , "wind_gust"]
    for hours in hourly_weather:
        print("_____________________")
        print(hours)
        hour_dict = {}
        for element in hourly_elements_try:
            if element in hours:
                hour_dict[element] = hours[element]

        try:
            hour_dict["dt"] = dt.utcfromtimestamp(int(hours["dt"]) + int(time_adjust)).strftime('%A %I:%M %p')
            hour_dict["dt"] = hour_dict["dt"].lstrip("0").replace(" 0", " ")
        except:
            print('hour_dict["dt"] failed')
        try:
            hour_dict["feels_like"] = f'{round(hour_dict["feels_like"])} °F' #Round 
        except:
            print('hour_dict["feels_like"] failed')
        try:
            hour_dict["clouds"] = f'{round(hour_dict["clouds"] )}%' #Percentage
        except:
            print('hour_dict["clouds"] failed')
        try:
            hour_dict["uvi"] = f'{round(hour_dict["uvi"] )}' #Percentage
        except:
            print('hour_dict["uvi"] failed')
        try:
            hour_dict["humidity"] = f'{round(hour_dict["humidity"] )}%'
        except:
            print('hour_dict["humidity"] failed')
        try:
            hour_dict["pop"] = f'{round(hour_dict["pop"] * 100)}%'
        except:
            print('hour_dict["pop"] failed')
        try:
            hour_dict["temp"] = f'{round(hour_dict["temp"])} °F'
        except:
            print('hour_dict["temp"] failed')
        try:
            hour_dict["wind_speed"] = f'{round(hour_dict["wind_speed"])} MPH'
        except:
            print('hour_dict["wind_speed"]')
        try:
            hour_dict["wind_gust"] = f'{round(hour_dict["wind_gust"])} MPH'
        except:
            print('hour_dict["wind_gust"]')
        
        try:
            hour_dict["summary"] = hours["weather"][0]["description"]
        except:
            print('hour_dict["summary"] FAILED')
        try:
            hour_dict["rain"] = hour_dict["rain"]["1h"]
        except:
            print('hour_dict["rain"] FAILED')
        try:
            hour_dict["snow"] = hour_dict["snow"]["1h"]
        except:
            print('hour_dict["snow"] FAILED')
        # try:
        #     hour_dict["summary"] =
        
        hourly_list.append(hour_dict)

    return hourly_list

def getdaily(daily_weather, time_adjust): #
    from datetime import datetime as dt
    #Pull data from Daily Conditions
    daily_elements_try = ["clouds", "humidity", "rain", "snow",  
     "pop", "description", "sunrise", "sunset", "temp", 
       "dt", "uvi",  "wind_speed" , "wind_gust"] 
    daily_list = []
    print(daily_weather[0])
    # print("enter daily loop")

    for days in daily_weather:
        daily_dict = {}
        for elements in daily_elements_try:
            if elements in days:
                daily_dict[elements] = days[elements]

        #Format Fixing
        try:
            daily_dict["clouds"] = f'{round(daily_dict["clouds"])}%'
        except:
            print('daily_dict["clouds"] failed')
        try:
            daily_dict["humidity"] = f'{round(daily_dict["humidity"])}%'
        except:
            print('daily_dict["humidity"] failed')
        try:
            daily_dict["uvi"] = f'{round(daily_dict["uvi"])}'
        except:
            print('daily_dict["uvi"] failed')
        try:
            daily_dict["rain"] = f'{daily_dict["rain"]}'
            print("rain")
            print(daily_dict["rain"])
        except:
            print('daily_dict["rain"] failed')
        try:
            daily_dict["pop"] = f'{round(daily_dict["pop"] * 100)}%'
        except:
            print('daily_dict["pop"] failed')
        try:
            daily_dict["snow"] = f'{daily_dict["snow"]}'
        except:
            print('daily_dict["snow"] failed')
        try:
            daily_dict["temp_low"] = f'{round(days["temp"]["min"])} °F'
        except:
            print('daily_dict["temp"] failed')
        try:
            daily_dict["temp_high"] = f'{round(days["temp"]["max"])} °F'
        except:
            print('daily_dict["temp"] failed')
        try:
            daily_dict["wind_speed"] = f'{round(daily_dict["wind_speed"])} MPH'
        except:
            print('daily_dict["wind_speed"] failed')
        try:
            daily_dict["wind_gust"] = f'{round(daily_dict["wind_gust"])} MPH'
        except:
            print('daily_dict["wind_gust"] failed')
        try:
            daily_dict["summary"] = days["weather"][0]["description"]
        except:
            print('daily_dict["summary"] = days["weather"][0]["description"] FAILED')

        #TIMES
        
        try:
            daily_dict["sunrise"] = f"{dt.utcfromtimestamp(daily_dict['sunrise'] + time_adjust).strftime('%I:%M %p')}".lstrip("0").replace(" 0", " ")
        except:
            print('daily_dict["sunrise"] failed')
        try:
            daily_dict["sunset"] = f"{dt.utcfromtimestamp(daily_dict['sunset'] + time_adjust).strftime('%I:%M %p')}".lstrip("0").replace(" 0", " ")
        except:
            print('daily_dict["sunset"] failed')
        
        try:
            daily_dict["dt"] = f"{dt.utcfromtimestamp(daily_dict['dt'] + time_adjust).strftime('%A %B %d')}".lstrip("0").replace(" 0", " ")
        except:
            print('daily_dict["dt"] failed')
        
        
        
        daily_list.append(daily_dict)
    print(daily_list[0])
    print("___________________")
    return daily_list


def getweather_input(city): #
    city = fixnyc(city)

    location_response = getlocation(city)
    place = location_response[0]
    print(place)

    url = get_url(location_response[1], location_response[2])
    data_response = getdata(url)
    response_json = data_response[0]
    time_adjust = data_response[1]
    #MIGRATED TO HERE


    current_dict = getcurrent(response_json["current"], time_adjust)

    hourly_list = gethourly(response_json["hourly"], time_adjust)

    daily_list = getdaily(response_json["daily"], time_adjust)
    

    #Get Next Hour Summary (gone with new API, kept element to reduce changes)
    next_hour = "Unavailable"

    #Get Alerts
    if "alerts" in response_json:
        all_alerts = response_json["alerts"]
        alerts = []
        for messages in all_alerts:
            alerts.append(messages["description"])
    else:
        alerts = []
        alerts.append("CLEAR")

    data = [place, current_dict, hourly_list, daily_list, next_hour, alerts]

    return data


def getweather_link(city): #
    # city_urls = {"Bayonne, NJ" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.6687141,-74.1143091" ,
    # "Atlanta, GA" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/33.7490987,-84.3901849",
    # "Cranston, RI" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/41.7809588,-71.4371257", 
    # "Culver, IN" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/41.2189311,-86.4230626" ,
    # "Magic Kingdom, Disney World, Florida" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/28.4190753,-81.58171584246976" ,
    # "Easton, PA" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.6916081,-75.2099866" , 
    # "Hightstown, NJ" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.2695538,-74.5232089" , 
    # "Montclair, NJ" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.8164458,-74.2210643" , 
    # "New York, NY" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.7896239,-73.9598939" ,
    # "Warren Township, NJ" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.63065715,-74.52266308479568" , 
    # "West New York, NJ" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.7856117,-74.0093129",
    # "Lincoln Park, NJ" : "https://api.darksky.net/forecast/5fc1f583fa2e15d8a27208e502ba5fb0/40.9242652,-74.3020933"

    # }

    city_urls = {"Bayonne, NJ" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.6687141&lon=-74.1143091&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" ,
    "Atlanta, GA" : "http://api.openweathermap.org/data/2.5/onecall?lat=33.7489924&lon=-84.3902644&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530",
    "Cranston, RI" : "http://api.openweathermap.org/data/2.5/onecall?lat=41.7809588&lon=-71.4371257&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530", 
    "Culver, IN" : "http://api.openweathermap.org/data/2.5/onecall?lat=50.406915049999995&lon=-4.20954003080163&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" ,
    "Magic Kingdom, Disney World, Florida" : "http://api.openweathermap.org/data/2.5/onecall?lat=28.4190753&lon=-81.58171584246976&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" ,
    "Easton, PA" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.6916081&lon=-75.2099866&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" , 
    "Hightstown, NJ" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.269559&lon=-74.5232454&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" , 
    "Montclair, NJ" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.8164458&lon=-74.2210643&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" , 
    "New York, NY" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.7896239&lon=-73.9598939&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" ,
    "Warren Township, NJ" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.63065715&lon=-74.52266308479568&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530" , 
    "West New York, NJ" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.7856117&lon=-74.0093129&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530",
    "Lincoln Park, NJ" : "http://api.openweathermap.org/data/2.5/onecall?lat=40.9242652&lon=-74.3020933&units=imperial&appid=2f2ce2142c650c2e629355e66b97e530"

    }

    url = city_urls[city]

    place = city

    data_response = getdata(url)
    response_json = data_response[0]
    time_adjust = data_response[1]

    current_dict = getcurrent(response_json["current"], time_adjust)

    hourly_list = gethourly(response_json["hourly"], time_adjust)

    daily_list = getdaily(response_json["daily"], time_adjust)
    


    #Get Next Hour Summary
    try:
        next_hour = response_json["minutely"]["summary"]
    except:
        print("next hour failed")
        next_hour = "Unavailable"

    #Get Alerts
    if "alerts" in response_json:
        all_alerts = response_json["alerts"]
        alerts = []
        for messages in all_alerts:
            alerts.append(messages["description"])
    else:
        alerts = []
        alerts.append("CLEAR")

    data = [place, current_dict, hourly_list, daily_list, next_hour, alerts]

    return data



# 100, 60th Street, West New York, Hudson County, New Jersey, 07093, United States
# Bayonne, Hudson County, New Jersey, 07002, United States
# Manhattan, New York County, New York, United States
# Empire State Building, 350, 5th Avenue, Koreatown, Midtown South, Manhattan, New York County, New York, 10018, United States
# Brooklyn, Kings County, New York, United States
# state names don't work, index issue 
# Walt Disney World Resort, Bay Lake, Reedy Creek Improvement District, Orange County, Florida, 32830, United States
# Splash Mountain, Frontierland North, Bay Lake, Reedy Creek Improvement District, Orange County, Florida, United States
# 29, Avenue B, Bayonne, Hudson County, New Jersey, 07002, United States
# Bayonne High School, West 30th Street, Bayonne, Hudson County, New Jersey, 07002, United States
# JFK + 58th Street, John F. Kennedy Boulevard, Bayonne, Hudson County, New Jersey, 07305, United States
# Albany, Albany County, New York, 12207, United States
# Yankee Stadium, 1, East 161st Street, The Bronx, Bronx County, New York, 10451, United States
# Los Angeles, California, United States
# Paris, Île-de-France, France métropolitaine, France
# Washington, District of Columbia, United States
# 
# 
# 