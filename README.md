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
The free tier for [this API](https://rapidapi.com/ntd119/api/Priceline%20COM) allows 500 requests per month at a max of 1,000 requests per hour. 
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

### Airbnb
The free tier for [this API](https://rapidapi.com/insidebnb-team-insidebnb-team-default/api/airbnb-listings) allows 16,000 requests per month at a max of 1,000 requests per hour. 
#### Fields:
##### Listings by lat long
- airbnb_id
- distance in meters to lat long provided

The max range is 20,000 metres.

##### Listing details
- airbnb_id
- city
- listingTitle
- reviewCount
- starRating
- maxGuestCapacity
- bedrooms
- beds
- bathrooms
- bathroomsShared
- propertyType
- listingLat
- listingLng
- cancel_policy
- min_nights
- max_nights
- check_in_time
- check_out_time
- listingstatus (what does this mean?)

#### Additional API calls:

##### Availability
This API provides two endpoints to access availablity data for a specific airbnb id:
- [availability by month](https://airbnb-listings.p.rapidapi.com/v2/listingavailability)
- [availability for next 12 months](https://airbnb-listings.p.rapidapi.com/v2/listingAvailabilityFull)

**Note**: the available field can be true but this by itself does not means that the listing can be booked. It only tells indicates that this day is not taken. To confirm if it is really available for stay you must verify that all previous and following day rules for stay length are respected. To get the real available for stay status you can use the Listing Status endpoint.

##### Availability status
This API also provides two endpoints to access availability status for a specific airbnb same as the above Availability APIs - [one month](https://airbnb-listings.p.rapidapi.com/v2/listingstatus) and [next 12 months](https://airbnb-listings.p.rapidapi.com/v2/listingStatusFull). This data is needed to confirm if a unit is actually available on a specific date since the aformentioned API may return a false positive (ie positive = available).

##### Listing prices
Same as above, there is a [one month](https://api.insidebnb.com:8443/v2/listingPrices) and [next 12 months](https://api.insidebnb.com:8443/v2/listingPricesFull) endpoint to get prices for a specific unit.

##### Amenitiy codes
[This API endpoint](https://airbnb-listings.p.rapidapi.com/v2/amenities) returns amenity ids and descriptions, 50 results only. 

##### Listing reviews
[This endpoint](https://api.insidebnb.com:8443/v2/listingReviews) returns up to 20 reviews after the specified datetime. Each reviews contains those fields: reviewid, comments, response, datetime, language, rating: 5, guest_id. Available only for properties

### Bookingdotcom

