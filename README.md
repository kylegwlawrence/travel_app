## Problem
Planning a trip requires visiting multiple websites and manually gathering data to determine the best options for your trip as a whole. This can involve researching driving directions, parking, flights, car rentals, accommodations, attractions and more. There is no tool that can provide recommendations for all parts of a trip with various parameters and filters. 

## Current travel site market
There are lots of travel aggregating sites out there such as Expedia and Kayak but no one has an application that plans the entire trip and reccommends and refines its options based on your feedback.

## Solution
Create an application that will accept parameter and filter inputs to define and design a trip from end to end. 

## How it works
At a high level, this app takes inputs for your trip and returns options by calling APIs from various travel websites

# APIs
- AirBnb: 
    - https://rapidapi.com/ntd119/api/airbnb-search
    - https://rapidapi.com/3b-data-3b-data-default/api/airbnb13
- Booking.com
    - https://rapidapi.com/ntd119/api/booking-com18
- Hotels.com
    - https://rapidapi.com/tipsters/api/hotels-com-provider
- Priceline:
    - https://rapidapi.com/ntd119/api/priceline-com2
- Flight scraper:
    - https://rapidapi.com/ntd119/api/sky-scanner3
- Flight data:
    - https://rapidapi.com/Travelpayouts/api/flight-data
- Compare flight prices:
    - https://rapidapi.com/obryan-software-obryan-software-default/api/compare-flight-prices
- Route optimization:
    - https://rapidapi.com/geoapify-gmbh-geoapify/api/route-optimization

# Output
## Accommodations
### Defining good accomodations
- show best guest ratings (>=90% rating)
- show best prices for top guest ratings (ie. sort ascending order)
- show hotel star rating
- show proximity to city center (?)

### Priceline
#### Fields:
- hotel name
- hotel id
- priceline id
- address
- city name
- province code
- neighborhood name
- overall guest rating (out of 10)
- deal types
- nightly rate including taxes and fees
- grand total
- proximity (to lat long of location id?)
- checkIn and checkOut dates
- lat and long of hotel

##### need:
- star rating

### Bookingdotcom

