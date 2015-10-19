# -*- coding: utf-8 -*-
import pyowm
from time import *
from PyQt4 import QtCore, QtGui

API_key = '373575716a2a4a494cf852827616ff19'
owm = pyowm.OWM(API_key)
wIcons = {800:'sunny.png', 801:'partcloudy.png', 802:'cloudy.png', 803:'clouds.png', 804:'clouds.png', 701:'mist.png',
          500:'drizzle.png', 301:'drizzle.png', 501:'drizzle.png', 502:'rainy.png', 503:'rainy.png', 504:'rainy.png',
          600:'snowfall.png', 601:'snowfall.png', 602:'snowstorm.png',
          200:'lightning.png', 201:'lightning.png', 202:'lightningstorms.png', 211:'lightningstorms.png', 212:'lightningstorms.png'}

class WeatherWidget(QtGui.QWidget):

    def __init__(self, parent):
        """
            Initialize the browser GUI and connect the events
        """
        super(WeatherWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.grid = QtGui.QGridLayout(self)
        self.observation = owm.weather_at_coords(46.73, -117.18)

        #Initialize timers
        self.currentTimer = QtCore.QTimer()
        self.currentTimer.timeout.connect(self.updateWeather)
        self.currentTimer.start(900000) # Update current weather every 15 min

        self.forecastTimer = QtCore.QTimer()
        self.forecastTimer.timeout.connect(self.updateForecast)
        self.forecastTimer.start(3600000) # Update forecast every hour

        # Initialize current Temperatures
        w = self.observation.get_weather()

        date = QtGui.QLabel()
        date.setText("Today") # date
        date.setScaledContents(True)
        ff = QtGui.QFont()
        ff.setPointSize(16)
        ff.setBold(True)
        date.setFont(ff)
        date.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        pic = QtGui.QLabel()
        pic.setScaledContents(True)
        pixmap = QtGui.QPixmap(self.getIcon(w.get_weather_code()))
        pic.setPixmap(pixmap) #icon
        pic.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        temp = QtGui.QLabel()
        ff.setPointSize(12)
        ff.setBold(False)
        temp.setFont(ff)
        temp.setText(str(w.get_temperature('fahrenheit')['temp']) + '°') # temperature
        temp.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        det = QtGui.QLabel()
        det.setText(w.get_detailed_status()) # details
        det.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        self.grid.addWidget(date, 0, 0)
        self.grid.addWidget(pic, 1, 0)
        self.grid.addWidget(temp, 2, 0)
        self.grid.addWidget(det, 3, 0)

        # Initialize next 4 days of weather
        forecast = owm.daily_forecast_at_id(self.observation.get_location().get_ID(), limit=5)
        f = forecast.get_forecast()
        wlist = f.get_weathers()

        i = 1
        ff.setPointSize(14)
        for weather in wlist[1:]:
            t = weather.get_reference_time('iso')
            w = weather.get_temperature('fahrenheit')

            date = QtGui.QLabel()
            date.setText(t.split(" ")[0][5:]) # date
            date.setFont(ff)
            date.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

            pic = QtGui.QLabel()
            pic.setScaledContents(True)
            pixmap = QtGui.QPixmap(self.getIcon(weather.get_weather_code()))
            # scaledPix = pixmap.scaled(pixmap.width(), pixmap.height(), QtCore.Qt.KeepAspectRatio)
            pic.setPixmap(pixmap) #icon
            pic.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

            temp = QtGui.QLabel()
            temp.setText('H: ' + str(w['max']) + '°\nL: ' + str(w['min']) + '°') # temperature
            temp.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

            det = QtGui.QLabel()
            det.setText(weather.get_detailed_status()) # details
            det.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

            self.grid.addWidget(date, 0, i)
            self.grid.addWidget(pic, 1, i)
            self.grid.addWidget(temp, 2, i)
            self.grid.addWidget(det, 3, i)
            i = i + 1

        self.show() # SHOW YOURSELF

    def getIcon(self, code): # Fetch correct weather icon based on weather code (http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes)
        if (code in wIcons.keys()):
            return "weathericons/" + wIcons[code]
        else:
            print("MISSING WEATHER CODE IS: " + str(code))
            return "weathericons/na.png" # no image available for given weather code

    def updateWeather(self): # Update the current weather
        w = self.observation.get_weather()

        pic = self.grid.itemAtPosition(1,0).widget()
        temp = self.grid.itemAtPosition(2,0).widget()
        det = self.grid.itemAtPosition(3,0).widget()

        pixmap = QtGui.QPixmap(self.getIcon(w.get_weather_code())) # Update icon
        pic.setPixmap(pixmap) #icon

        temp.setText(str(w.get_temperature('fahrenheit')['temp']) + '°')
        det.setText(w.get_detailed_status())

    def updateForecast(self): # Update the forecast (next 4 days of weather)
        forecast = owm.daily_forecast_at_id(self.observation.get_location().get_ID(), limit=5)
        f = forecast.get_forecast()
        wlist = f.get_weathers()

        i = 1
        for weather in wlist[1:]:
            t = weather.get_reference_time('iso')
            w = weather.get_temperature('fahrenheit')

            date = self.grid.itemAtPosition(0,i).widget()
            date.setText(t.split(" ")[0][5:]) # date

            pic = self.grid.itemAtPosition(1,i).widget()
            pixmap = QtGui.QPixmap(self.getIcon(weather.get_weather_code()))
            pic.setPixmap(pixmap) #icon

            temp = self.grid.itemAtPosition(2,i).widget()
            temp.setText('H: ' + str(w['max']) + '°\nL: ' + str(w['min']) + '°') # temperature

            det = self.grid.itemAtPosition(3,i).widget()
            det.setText(weather.get_detailed_status()) # details

            i = i + 1