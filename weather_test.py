import pyowm

API_key = '373575716a2a4a494cf852827616ff19'
owm = pyowm.OWM(API_key)
observation = owm.weather_at_coords(46.73, -117.18)
w = observation.get_weather()
temperature = w.get_temperature('fahrenheit')


print('It is ' + str(temperature['temp']) + ' degrees Fahrenheit and ' + w.get_detailed_status() + ' in ' + observation.get_location().get_name())

print('**************')
print('**************')

forecast = owm.daily_forecast_at_id(observation.get_location().get_ID(), limit=5)
f = forecast.get_forecast()
for weather in f:
	t = weather.get_reference_time('iso')
	print(t.split(" ")[0][5:])
	print('     ' + str(weather.get_temperature('fahrenheit')) + ' degrees')
	print('     ' + weather.get_detailed_status())