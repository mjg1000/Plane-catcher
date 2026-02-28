# Plane-catcher
Hackathon project

## Architecture
### Backend
Python + Flask
#### Components
##### Main
- Photo to tail number
- - gemini
- tail number to plane data
- - wtf ever is the api
- - call 'add plane' with the data we find 
- plane info to cartoon image
- - have folder of cartoon images
- Frontend x,y locations of planes to display
- - get planes in e.g. 10 sq km 
- - get plane data for each
- - convert lat/long to x,y for front

##### DB linked
- get plane data
- get user's offers
- get user's badges
- get user's inventory
- add plane 
#### DB
##### Tables
Users
Planes
Inventories
Offers
Offer_types
Badges
Badge_types

### Frontend 
react
