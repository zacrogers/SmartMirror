import pyowm

API_KEY = "b836329a048e17c098713fa2587cf192"

def get_temp(city, country):
    try:
        owm = pyowm.OWM(API_KEY)
        mgr = owm.weather_manager()
        obs = mgr.weather_at_place(f'{city}, {country}')
        weather = obs.weather
        return weather.temperature('celsius')['temp']

    except Exception as e:
        print(f"Weather api exception: {e}")
        return 99

def get_status(city, country):
    try:    
        owm = pyowm.OWM(API_KEY)
        mgr = owm.weather_manager()
        obs = mgr.weather_at_place(f'{city}, {country}')
        weather = obs.weather
        return weather.status

    except Exception as e:
        print(f"Weather api exception: {e}")
        return "Clear"
#print(get_status('Wellington', 'NZ'))
#get_temp('Christchurch', 'NZ')
#get_temp('Auckland', 'NZ')
#get_temp('Dunedin', 'NZ')
