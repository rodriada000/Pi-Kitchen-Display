# Pi-Kitchen-Display
Kitchen Display for music, weather, and recipes written in python 3 using PyQt4

I bought a Raspberry Pi 2 and a 7" touchscreen lcd display recently 
so I decided to create my own kitchen display.

It currently has:
  - digital clock
  - calendar (for looks right now..)
  - Current weather and the forecast for the next 4 days (updated every 15 and 60 minutes respectively)
  - Musicplayer (requires cherrymusic)
  
Requires:
  - PyQt 4.x
  - pyowm to be installed (sudo pip install pyowm or sudo pip3 install pyowm)
  - cherrymusic to be installed and running for music server (https://github.com/devsnd/cherrymusic)
          - use port 4200 for now (user cannot change yet)
