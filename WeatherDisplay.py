# -*- coding: utf-8 -*-
import requests
import json
from time import *
from PyQt4 import QtCore, QtGui

wIcons = {'Clear':'sunny.png', 'Partly Cloudy':'partcloudy.png', 'Mostly Cloudy':'cloudy.png', 'Scattered Clouds':'clouds.png', 'Mist':'mist.png',
          'Light Drizzel':'drizzle.png', 'Drizzle':'drizzle.png', 'Heavy Drizzle':'drizzle.png', 'Light Rain':'rainy.png', 'Rain':'rainy.png', 'Heavy Rain':'rainy.png',
          'Light Snow':'snowfall.png', 'Snow':'snowfall.png', 'Heavy Snow':'snowfall.png', 'Snow Showers':'snowfall.png', 'Fog':'morningfog.png',
          'Light Thunderstorm':'lightning.png', 'Thunderstorm':'lightning.png', 'Heavy Thunderstorm':'lightning.png'}

class WeatherWidget(QtGui.QWidget):

    def __init__(self, parent):
        """
            Initialize the browser GUI and connect the events
        """
        super(WeatherWidget, self).__init__(parent)

        self.origIcons = list() # contains original version of icon to do proper scaling

        # Load API key and location from weather.cfg file
        self.API_key = None
        self.userCity = ''
        self.userState = ''
        try:
            with open('weather.cfg') as settings:
                lines = [line.rstrip('\n') for line in settings]
                i = 0
                while (lines[i][0] == '#'): i += 1
                self.API_key = lines[i] # API Key should be first line in weather.cfg
                location = lines[i+1]  # Location should be second line
                self.userCity = location.split(' ')[0]
                self.userState = location.split(' ')[1]
        except:
            print("Failed to open weather.cfg..")
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

    def getIcon(self, code): # Fetch correct weather icon based on weather code
        if code in wIcons.keys():
            return "weathericons/" + wIcons[code]
        else:
            print("MISSING WEATHER CODE IS: " + code)
            return "weathericons/na.png" # no image available for given weather code
    #def end

    def updateWeather(self): # Update the current weather
        try:
            r = requests.get("http://api.wunderground.com/api/" + self.API_key + "/hourly/q/" + self.userState + "/" + self.userCity + ".json") # get json request
            data = r.json()
            weather = data['hourly_forecast'][0]
        except Exception as e:
            print("Failed to get current weather ... " + str(e))
            return

        pic = self.grid.itemAtPosition(1,0).widget()
        temp = self.grid.itemAtPosition(2,0).widget()
        det = self.grid.itemAtPosition(3,0).widget()

        self.origIcons[0] = QtGui.QPixmap(self.getIcon(weather['condition'])) # Update icon
        rect = self.grid.cellRect(1, 0) # get bounds of grid cell
        if rect.width() < rect.height(): # use mininum of width or height for icon size
            picSize = rect.width()
        else:
            picSize = rect.height()
        scaledPix = self.origIcons[0].scaled(picSize, picSize)
        pic.setPixmap(scaledPix) #icon

        temp.setText("Real Temp: " + weather['temp']['english'] + '°\nFeels Like: ' + weather['feelslike']['english'] + '°')
        det.setText(weather['condition'].replace(' ', '\n'))
    #def end

    def updateForecast(self): # Update the forecast (next 4 days of weather)
        try:
            r = requests.get("http://api.wunderground.com/api/" + self.API_key + "/forecast10day/q/" + self.userState + "/" + self.userCity + ".json") # get json request
            data = r.json()
            forecast = data['forecast']['simpleforecast']['forecastday']
        except Exception as e:
            print("Failed to get forecast ... " + str(e))
            return
                         
        i = 1
        for day in forecast[1:]:
            t = day['date']['weekday']
            highTemp = day['high']['fahrenheit']
            lowTemp = day['low']['fahrenheit']

            date = self.grid.itemAtPosition(0,i).widget()
            date.setText(t) # Update day of week

            self.origIcons[i] = QtGui.QPixmap(self.getIcon(day['conditions'])) # Update icon
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
            temp.setText('H: ' + highTemp + '°\nL: ' + lowTemp + '°')

            det = self.grid.itemAtPosition(3,i).widget()
            det.setText(day['conditions'].replace(' ', '\n')) # conditions

            i = i + 1
            if i > 4:
                break
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
