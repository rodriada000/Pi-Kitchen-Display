# Pi-Kitchen-Display
Kitchen Display for music, weather, and web browsing written in python 3 using PyQt4

I bought a Raspberry Pi 2 and a 7" touchscreen lcd display so I decided to create my own kitchen display. 
The UI is tailored for smaller touch screens and that is why the buttons are larger.

It currently has:
  - Digital clock
  - Current weather and the forecast for the next 4 days (updated every 15 and 60 minutes respectively)
        + place wunderground API key and location in file named weather.cfg
        + can press the weather icon to hear the weather
  - Musicplayer (requires cherrymusic)
        + place host server in file named music.cfg
  - Web browser with ad-blocking capabilities
  - RSS news feed
        + click on RSS titles to open the article in the web browser
        + create a file named rssfeed.cfg and place urls of RSS feeds in there, seperated by newline
  - Dishwasher status
        + Tell whether dishes in the dishwasher are dirty or clean. Update status easily with the press of a button
  
Requires:
  - PyQt 4.x
  - wunderground API key
  - cherrymusic to be installed and running for music server (https://github.com/devsnd/cherrymusic)
  - pyttsx for python3 (https://github.com/jpercent/pyttsx)
  - feedparser
