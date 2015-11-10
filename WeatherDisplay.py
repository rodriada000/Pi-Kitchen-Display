# -*- coding: utf-8 -*-
import pyowm
from time import *
from datetime import datetime
from PyQt4 import QtCore, QtGui

wIcons = {800:'sunny.png', 801:'partcloudy.png', 802:'cloudy.png', 803:'clouds.png', 804:'clouds.png', 701:'mist.png',
          500:'drizzle.png', 301:'drizzle.png', 501:'drizzle.png', 502:'rainy.png', 503:'rainy.png', 504:'rainy.png',
          600:'snowfall.png', 601:'snowfall.png', 602:'snowfall.png', 741:'morningfog.png',
          200:'lightning.png', 201:'lightning.png', 202:'lightning.png', 211:'lightning.png', 212:'lightning.png'}

class WeatherWidget(QtGui.QWidget):

    def __init__(self, parent):
        """
            Initialize the browser GUI and connect the events
        """
        super(WeatherWidget, self).__init__(parent)

        self.origIcons = list() # contains original version of icon to do proper scaling

        # Load API key and location from weather.cfg file
        self.API_key = None
        self.userLocation = ''
        try:
            with open('weather.cfg') as settings:
                lines = [line.rstrip('\n') for line in settings]
                i = 0
                while (lines[i][0] == '#'): i += 1
                self.API_key = lines[i] # API Key should be first line in weather.cfg
                self.userLocation = lines[i+1] # Location should be second line
        except:
            print("Failed to open weather.cfg..")
            return

        # Get OWM object based off given API key
        try:
            self.owm = pyowm.OWM(self.API_key)
        except:
            print("Failed to get owm object with given API key: " + self.API_key)
            return

        # Get observation object based off given location
        try:
            self.observation = self.owm.weather_at_place(self.userLocation)
            if (self.observation is None):
                raise Exception()
        except:
            print("Failed to get weather at given location: " + self.userLocation)
            return

        #Initialize timers
        self.currentTimer = QtCore.QTimer()
        self.currentTimer.timeout.connect(self.updateWeather)
        self.currentTimer.start(900000) # Update current weather every 15 min

        self.forecastTimer = QtCore.QTimer()
        self.forecastTimer.timeout.connect(self.updateForecast)
        self.forecastTimer.start(3600000) # Update forecast every hour

        self.initUI()
    #def end

    def initUI(self):
        self.grid = QtGui.QGridLayout(self) # Gridlayout to contain all widgets

        # Today date label
        date = QtGui.QLabel()
        date.setText("Today")
        ff = QtGui.QFont()
        ff.setPointSize(14)
        ff.setBold(True)
        date.setFont(ff)
        date.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        # Today Icon label
        pic = QtGui.QLabel()
        pic.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.origIcons.append(QtGui.QPixmap())

        # Today temps label
        temp = QtGui.QLabel()
        temp.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        # Today weather details label
        det = QtGui.QLabel()
        det.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

        self.grid.addWidget(date, 0, 0)
        self.grid.addWidget(pic, 1, 0)
        self.grid.addWidget(temp, 2, 0)
        self.grid.addWidget(det, 3, 0)

        # Initialize 4-day Forecast widgets
        i = 1
        while i < 5:
            date = QtGui.QLabel()
            date.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)

            pic = QtGui.QLabel()
            pic.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            self.origIcons.append(QtGui.QPixmap())

            temp = QtGui.QLabel()
            temp.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            
            det = QtGui.QLabel()
            det.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            
            self.grid.addWidget(date, 0, i)
            self.grid.addWidget(pic, 1, i)
            self.grid.addWidget(temp, 2, i)
            self.grid.addWidget(det, 3, i)

            i = i + 1

        self.updateWeather()
        self.updateForecast() # populate with weather

        self.grid.setContentsMargins(2, 2, 2, 2)
        self.grid.setSpacing(3)
        self.show() # SHOW YOURSELF
    #def end

    def getIcon(self, code): # Fetch correct weather icon based on weather code (http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes)
        if code in wIcons.keys():
            return "weathericons/" + wIcons[code]
        else:
            print("MISSING WEATHER CODE IS: " + str(code))
            return "weathericons/na.png" # no image available for given weather code
    #def end

    def updateWeather(self): # Update the current weather
        self.observation = self.owm.weather_at_place(self.userLocation) # update observation object
        w = self.observation.get_weather()

        pic = self.grid.itemAtPosition(1,0).widget()
        temp = self.grid.itemAtPosition(2,0).widget()
        det = self.grid.itemAtPosition(3,0).widget()

        self.origIcons[0] = QtGui.QPixmap(self.getIcon(w.get_weather_code())) # Update icon
        rect = self.grid.cellRect(1, 0) # get bounds of grid cell
        if rect.width() < rect.height(): # use mininum of width or height for icon size
            picSize = rect.width()
        else:
            picSize = rect.height() 
        scaledPix = self.origIcons[0].scaled(picSize, picSize)
        pic.setPixmap(scaledPix) #icon

        temp.setText(str(w.get_temperature('fahrenheit')['temp']) + '°')
        det.setText(w.get_detailed_status().replace(' ', '\n'))
    #def end

    def updateForecast(self): # Update the forecast (next 4 days of weather)
        self.observation = self.owm.weather_at_place(self.userLocation) # update observation object
        forecast = self.owm.daily_forecast_at_id(self.observation.get_location().get_ID(), 5)
        f = forecast.get_forecast()
        wlist = f.get_weathers()

        i = 1
        for weather in wlist[1:]:
            t = weather.get_reference_time('iso').split(' ')[0] # Get date in format YYYY-MM-DD
            w = weather.get_temperature('fahrenheit')

            date = self.grid.itemAtPosition(0,i).widget()
            date.setText(datetime.strptime(t, '%Y-%m-%d').strftime('%a')) # date converted to day of week

            self.origIcons[i] = QtGui.QPixmap(self.getIcon(weather.get_weather_code())) # Update icon
            rect = self.grid.cellRect(1, i) # get bounds of grid cell
            if rect.width() < rect.height(): # use mininum of width or height for icon size
                picSize = rect.width()
            else:
                picSize = rect.height() 
            scaledPix = self.origIcons[i].scaled(picSize, picSize)

            pic = self.grid.itemAtPosition(1,i).widget() # get icon label widget
            pic.setPixmap(scaledPix)

            # Update temperature label with new temp
            temp = self.grid.itemAtPosition(2,i).widget()
            temp.setText('High: ' + str(w['max']) + '°\nLow: ' + str(w['min']) + '°')

            det = self.grid.itemAtPosition(3,i).widget()
            det.setText(weather.get_detailed_status().replace(' ', '\n')) # details

            i = i + 1
    #def end
            
    def bestFontSize(self, text, cellRect):
        size = 2 # minimum font size of 2
        ff = QtGui.QFont()
        ff.setPointSize(size)
        
        if '\n' in text: # measure width of text upto newline if there is one
            text = text.split('\n')[0]
        
        qf = QtGui.QFontMetrics(ff)
        
        while (True):
            textRect = qf.boundingRect(text)
            if textRect.width() > cellRect.width():
                break
            size += 1
            ff.setPointSize(size)
            qf = QtGui.QFontMetrics(ff)
            
        return size - 1 # reduce font size by 1 to fit within cellRect
    #def end

    def resizeEvent(self,resizeEvent): # Resizes text to fit inside each grid cell
        font = QtGui.QFont("Arial")
        maxDateSize = 18 # max font for displaying the dates
        maxSize = 14 # max font for displaying temperatures & details
        i = 0
        
        while i < 5:
            # Resize dates
            widg = self.grid.itemAtPosition(0, i).widget()
            rect = self.grid.cellRect(0, i)
            size = self.bestFontSize(widg.text(), rect)
            if (size > maxDateSize):
                size = maxDateSize
            
            if i == 0:
                font.setBold(True) # have "Today" be bolded to stand out
                font.setPointSize(size + 1)
            else:
                font.setPointSize(size - 1) # have dates be 1pt smaller than "Today"
                font.setBold(False)
            widg.setFont(font)
            font.setBold(False)

            # Resize pictures to keep aspectratio
            widg = self.grid.itemAtPosition(1, i).widget()
            rect = self.grid.cellRect(1, i)
            if rect.width() < rect.height(): # get mininum of width and height
                picSize = rect.width()
            else:
                picSize = rect.height() 
            scaledPix = self.origIcons[i].scaled(picSize, picSize)
            widg.setPixmap(scaledPix) #icon
            
             # Resize Temperatures label
            widg = self.grid.itemAtPosition(2, i).widget()
            rect = self.grid.cellRect(2, i)
            size = self.bestFontSize(widg.text(), rect) - 1
            if size > maxSize:
                size = maxSize
            font.setPointSize(size)
            widg.setFont(font)
            
            # Resize weather details
            widg = self.grid.itemAtPosition(3, i).widget()
            rect = self.grid.cellRect(3, i)
            size = self.bestFontSize(widg.text(), rect) - 1
            if size > maxSize:
                size = maxSize
            font.setPointSize(size)
            widg.setFont(font)
            
            i += 1
    #def end
