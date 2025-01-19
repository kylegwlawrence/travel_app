from searchAirbnbByAddress import search_address as searchAbb
from searchPricelineByAddress import search as searchPcln

address = "820 15 ave sw calgary ab"
range = 1000
checkIn = "2025-05-03"
checkOut = "2025-05-07"
limit = 10

airbnbs = searchAbb(address, range)

hotels = searchPcln(address, checkIn, checkOut, limit)