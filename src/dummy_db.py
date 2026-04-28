"""
In-memory dummy database simulating real travel and hotel booking data.
All tool functions query this module.
"""

import uuid
from datetime import datetime

# ---------------------------------------------------------------------------
# Destinations
# ---------------------------------------------------------------------------

DESTINATIONS = [
    {
        "id": "D001",
        "name": "Bali",
        "country": "Indonesia",
        "climate": "Tropical",
        "best_season": "April – October",
        "avg_daily_budget_usd": "$80–$150/day",
        "currency": "IDR (USD widely accepted)",
        "highlights": ["Tanah Lot Temple", "Seminyak Beach", "Ubud Rice Terraces", "Mount Batur"],
        "visa": "Visa on arrival for most nationalities – $35",
        "language": "Bahasa Indonesia / English widely spoken",
    },
    {
        "id": "D002",
        "name": "Paris",
        "country": "France",
        "climate": "Temperate",
        "best_season": "March – May, September – November",
        "avg_daily_budget_usd": "$200–$350/day",
        "currency": "EUR",
        "highlights": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Montmartre", "Seine River Cruise"],
        "visa": "Schengen visa required for non-EU (US/UK exempt for 90 days)",
        "language": "French / English in tourist areas",
    },
    {
        "id": "D003",
        "name": "Maldives",
        "country": "Maldives",
        "climate": "Tropical",
        "best_season": "November – April",
        "avg_daily_budget_usd": "$400–$800/day",
        "currency": "MVR (USD universally accepted)",
        "highlights": ["Overwater bungalows", "Coral reefs", "Whale shark snorkelling", "Male city tour"],
        "visa": "Free on arrival 30 days",
        "language": "Dhivehi / English",
    },
    {
        "id": "D004",
        "name": "New York",
        "country": "USA",
        "climate": "Temperate",
        "best_season": "September – November, April – June",
        "avg_daily_budget_usd": "$250–$450/day",
        "currency": "USD",
        "highlights": ["Times Square", "Central Park", "Statue of Liberty", "Broadway", "Brooklyn Bridge"],
        "visa": "ESTA for visa waiver countries – $21",
        "language": "English",
    },
    {
        "id": "D005",
        "name": "Kyoto",
        "country": "Japan",
        "climate": "Temperate",
        "best_season": "March – May (cherry blossoms), October – November",
        "avg_daily_budget_usd": "$120–$220/day",
        "currency": "JPY",
        "highlights": ["Fushimi Inari Shrine", "Arashiyama Bamboo Grove", "Kinkaku-ji", "Geisha district Gion"],
        "visa": "Visa-free for most western nationalities 90 days",
        "language": "Japanese / English in tourist areas",
    },
    {
        "id": "D007",
        "name": "Tokyo",
        "country": "Japan",
        "climate": "Temperate",
        "best_season": "March – May (cherry blossoms), October – November",
        "avg_daily_budget_usd": "$150–$300/day",
        "currency": "JPY",
        "highlights": ["Shibuya Crossing", "Shinjuku", "Senso-ji Temple", "teamLab Borderless", "Tsukiji Market"],
        "visa": "Visa-free for most western nationalities 90 days",
        "language": "Japanese / English in tourist areas",
    },
    {
        "id": "D006",
        "name": "Cape Town",
        "country": "South Africa",
        "climate": "Mediterranean",
        "best_season": "November – February",
        "avg_daily_budget_usd": "$100–$180/day",
        "currency": "ZAR (USD/EUR accepted in tourist spots)",
        "highlights": ["Table Mountain", "Cape of Good Hope", "V&A Waterfront", "Boulders Penguin Colony"],
        "visa": "Visa-free for most nationalities 90 days",
        "language": "English (plus 10 official languages)",
    },
]

# ---------------------------------------------------------------------------
# Flights
# ---------------------------------------------------------------------------

FLIGHTS = [
    {
        "id": "F1001",
        "from": "New York (JFK)",
        "to": "Bali (DPS)",
        "date": "2026-06-10",
        "airline": "Singapore Airlines",
        "flight_no": "SQ 26",
        "departs": "09:00",
        "arrives": "18:30 (+1 day)",
        "duration": "21h 30m (1 stop – Singapore)",
        "class": "Economy",
        "price_usd": 850,
        "seats_available": 12,
    },
    {
        "id": "F1002",
        "from": "New York (JFK)",
        "to": "Bali (DPS)",
        "date": "2026-06-12",
        "airline": "Emirates",
        "flight_no": "EK 204",
        "departs": "22:00",
        "arrives": "08:15 (+2 days)",
        "duration": "22h 15m (1 stop – Dubai)",
        "class": "Economy",
        "price_usd": 720,
        "seats_available": 4,
    },
    {
        "id": "F1003",
        "from": "New York (JFK)",
        "to": "Paris (CDG)",
        "date": "2026-06-10",
        "airline": "Air France",
        "flight_no": "AF 011",
        "departs": "19:00",
        "arrives": "08:30 (+1 day)",
        "duration": "7h 30m (non-stop)",
        "class": "Economy",
        "price_usd": 620,
        "seats_available": 20,
    },
    {
        "id": "F1004",
        "from": "New York (JFK)",
        "to": "Paris (CDG)",
        "date": "2026-06-15",
        "airline": "Delta",
        "flight_no": "DL 264",
        "departs": "11:00",
        "arrives": "00:45 (+1 day)",
        "duration": "7h 45m (non-stop)",
        "class": "Economy",
        "price_usd": 580,
        "seats_available": 8,
    },
    {
        "id": "F1005",
        "from": "New York (JFK)",
        "to": "Tokyo (NRT)",
        "date": "2026-06-10",
        "airline": "ANA",
        "flight_no": "NH 010",
        "departs": "13:00",
        "arrives": "16:30 (+1 day)",
        "duration": "14h 30m (non-stop)",
        "class": "Economy",
        "price_usd": 950,
        "seats_available": 6,
    },
    {
        "id": "F1006",
        "from": "London (LHR)",
        "to": "Bali (DPS)",
        "date": "2026-06-11",
        "airline": "Qatar Airways",
        "flight_no": "QR 008",
        "departs": "08:00",
        "arrives": "05:30 (+1 day)",
        "duration": "17h 30m (1 stop – Doha)",
        "class": "Economy",
        "price_usd": 780,
        "seats_available": 15,
    },
    {
        "id": "F1007",
        "from": "New York (JFK)",
        "to": "Cape Town (CPT)",
        "date": "2026-06-14",
        "airline": "South African Airways",
        "flight_no": "SA 203",
        "departs": "20:00",
        "arrives": "19:45 (+1 day)",
        "duration": "15h 45m (1 stop – Johannesburg)",
        "class": "Economy",
        "price_usd": 890,
        "seats_available": 9,
    },
    {
        "id": "F1008",
        "from": "New York (JFK)",
        "to": "Kyoto via Osaka (KIX)",
        "date": "2026-06-13",
        "airline": "JAL",
        "flight_no": "JL 006",
        "departs": "12:30",
        "arrives": "15:00 (+1 day)",
        "duration": "14h 30m (non-stop to Osaka, 1h train to Kyoto)",
        "class": "Economy",
        "price_usd": 920,
        "seats_available": 7,
    },
    {
        "id": "F1009",
        "from": "New York (JFK)",
        "to": "Tokyo (NRT)",
        "date": "2026-06-15",
        "airline": "JAL",
        "flight_no": "JL 004",
        "departs": "11:00",
        "arrives": "14:30 (+1 day)",
        "duration": "14h 30m (non-stop)",
        "class": "Economy",
        "price_usd": 880,
        "seats_available": 18,
    },
    {
        "id": "F1010",
        "from": "New York (JFK)",
        "to": "Tokyo (NRT)",
        "date": "2026-06-18",
        "airline": "United Airlines",
        "flight_no": "UA 837",
        "departs": "10:30",
        "arrives": "14:00 (+1 day)",
        "duration": "14h 30m (non-stop)",
        "class": "Economy",
        "price_usd": 810,
        "seats_available": 22,
    },
    {
        "id": "F1011",
        "from": "New York (JFK)",
        "to": "Osaka (KIX)",
        "date": "2026-06-20",
        "airline": "ANA",
        "flight_no": "NH 012",
        "departs": "14:00",
        "arrives": "17:45 (+1 day)",
        "duration": "15h 45m (non-stop)",
        "class": "Economy",
        "price_usd": 860,
        "seats_available": 10,
    },
    {
        "id": "F1012",
        "from": "New York (JFK)",
        "to": "Tokyo (NRT)",
        "date": "2026-07-01",
        "airline": "ANA",
        "flight_no": "NH 008",
        "departs": "13:00",
        "arrives": "16:30 (+1 day)",
        "duration": "14h 30m (non-stop)",
        "class": "Business",
        "price_usd": 2450,
        "seats_available": 5,
    },
]

# ---------------------------------------------------------------------------
# Hotels
# ---------------------------------------------------------------------------

HOTELS = [
    {
        "id": "H2001",
        "name": "The Mulia Bali",
        "location": "Bali",
        "stars": 5,
        "price_per_night_usd": 320,
        "amenities": ["Infinity pool", "Private beach", "Spa", "5 restaurants", "Butler service"],
        "room_types": ["Deluxe Ocean View – $320/night", "Suite – $580/night", "Villa – $950/night"],
        "review_score": 9.4,
        "reviews": 3812,
        "address": "Jl. Raya Nusa Dua Selatan, Bali 80363",
    },
    {
        "id": "H2002",
        "name": "Alaya Resort Ubud",
        "location": "Bali",
        "stars": 4,
        "price_per_night_usd": 180,
        "amenities": ["Pool", "Yoga pavilion", "Rice field view", "Organic restaurant", "Spa"],
        "room_types": ["Garden Room – $180/night", "Pool Suite – $280/night"],
        "review_score": 9.1,
        "reviews": 2145,
        "address": "Jl. Hanoman, Ubud, Bali 80571",
    },
    {
        "id": "H2003",
        "name": "Hotel Le Marais Paris",
        "location": "Paris",
        "stars": 4,
        "price_per_night_usd": 210,
        "amenities": ["Rooftop bar", "City center", "Concierge", "Breakfast included", "Fitness center"],
        "room_types": ["Classic – $210/night", "Superior – $265/night", "Junior Suite – $380/night"],
        "review_score": 8.8,
        "reviews": 4201,
        "address": "15 Rue de Bretagne, 75003 Paris",
    },
    {
        "id": "H2004",
        "name": "Shangri-La Paris",
        "location": "Paris",
        "stars": 5,
        "price_per_night_usd": 550,
        "amenities": ["Eiffel Tower view", "Spa", "Michelin-starred restaurant", "Pool", "Valet parking"],
        "room_types": ["Deluxe – $550/night", "Eiffel Suite – $1,200/night"],
        "review_score": 9.6,
        "reviews": 1890,
        "address": "10 Avenue d'Iéna, 75116 Paris",
    },
    {
        "id": "H2005",
        "name": "The Peninsula New York",
        "location": "New York",
        "stars": 5,
        "price_per_night_usd": 695,
        "amenities": ["Rooftop pool", "Spa", "Fine dining", "Midtown location", "Rolls-Royce fleet"],
        "room_types": ["Deluxe – $695/night", "Executive Suite – $1,100/night"],
        "review_score": 9.5,
        "reviews": 2760,
        "address": "700 Fifth Avenue, New York, NY 10019",
    },
    {
        "id": "H2006",
        "name": "citizenM Times Square",
        "location": "New York",
        "stars": 3,
        "price_per_night_usd": 195,
        "amenities": ["Rooftop bar", "24h canteen", "Smart rooms", "Times Square steps away", "Free WiFi"],
        "room_types": ["Standard – $195/night"],
        "review_score": 8.9,
        "reviews": 6543,
        "address": "218 W 50th Street, New York, NY 10019",
    },
    {
        "id": "H2007",
        "name": "Gion Hatanaka Ryokan",
        "location": "Kyoto",
        "stars": 5,
        "price_per_night_usd": 480,
        "amenities": ["Traditional ryokan", "Kaiseki multi-course dinner", "Yukata robes", "Geisha district", "Onsen"],
        "room_types": ["Tatami Room – $480/night (includes dinner & breakfast)"],
        "review_score": 9.7,
        "reviews": 890,
        "address": "505 Shimokawara-cho, Gion, Kyoto 605-0074",
    },
    {
        "id": "H2009",
        "name": "Park Hyatt Tokyo",
        "location": "Tokyo",
        "stars": 5,
        "price_per_night_usd": 520,
        "amenities": ["Shinjuku skyline view", "Indoor pool", "Spa", "New York Bar & Grill", "Fitness center"],
        "room_types": ["Park Deluxe – $520/night", "Park Suite – $980/night", "Presidential Suite – $2,200/night"],
        "review_score": 9.5,
        "reviews": 3120,
        "address": "3-7-1-2 Nishi Shinjuku, Shinjuku-ku, Tokyo 163-1055",
    },
    {
        "id": "H2010",
        "name": "Shibuya Stream Excel Hotel Tokyu",
        "location": "Tokyo",
        "stars": 4,
        "price_per_night_usd": 220,
        "amenities": ["Shibuya crossing views", "Rooftop terrace", "On-site restaurant", "Free WiFi", "Concierge"],
        "room_types": ["Standard – $220/night", "Superior – $275/night", "Corner Suite – $420/night"],
        "review_score": 8.9,
        "reviews": 1850,
        "address": "2-2-43 Shibuya, Shibuya-ku, Tokyo 150-0002",
    },
    {
        "id": "H2008",
        "name": "The Table Bay Hotel",
        "location": "Cape Town",
        "stars": 5,
        "price_per_night_usd": 290,
        "amenities": ["V&A Waterfront", "Table Mountain view", "Pool", "Award-winning restaurant", "Spa"],
        "room_types": ["Mountain View – $290/night", "Harbour Suite – $520/night"],
        "review_score": 9.3,
        "reviews": 2310,
        "address": "Quay 6, V&A Waterfront, Cape Town 8002",
    },
]

# ---------------------------------------------------------------------------
# Bookings store (grows at runtime)
# ---------------------------------------------------------------------------

BOOKINGS: list[dict] = []


# ---------------------------------------------------------------------------
# Query helpers — called by agent tool functions
# ---------------------------------------------------------------------------

def search_destinations(query: str) -> list[dict]:
    q = query.lower()
    results = []
    for d in DESTINATIONS:
        searchable = " ".join([
            d["name"], d["country"], d["climate"],
            d["best_season"], " ".join(d["highlights"])
        ]).lower()
        if any(word in searchable for word in q.split()):
            results.append(d)
    return results if results else DESTINATIONS  # return all if no match


def search_flights(origin: str, destination: str, date: str | None = None) -> list[dict]:
    o, d = origin.lower(), destination.lower()
    results = []
    for f in FLIGHTS:
        from_match = any(word in f["from"].lower() for word in o.split())
        to_match   = any(word in f["to"].lower()   for word in d.split())
        if from_match and to_match:
            if date is None or date in f["date"]:
                results.append(f)
    return results


def get_flight(flight_id: str) -> dict | None:
    for f in FLIGHTS:
        if f["id"].upper() == flight_id.upper():
            return f
    return None


def book_flight(flight_id: str, passenger_name: str) -> dict:
    flight = get_flight(flight_id)
    if not flight:
        return {"success": False, "error": f"Flight {flight_id} not found."}
    if flight["seats_available"] < 1:
        return {"success": False, "error": "No seats available on this flight."}

    flight["seats_available"] -= 1
    booking = {
        "booking_id": "BKF-" + uuid.uuid4().hex[:8].upper(),
        "type": "flight",
        "flight_id": flight["id"],
        "flight_no": flight["flight_no"],
        "airline": flight["airline"],
        "route": f"{flight['from']} → {flight['to']}",
        "date": flight["date"],
        "departs": flight["departs"],
        "arrives": flight["arrives"],
        "passenger": passenger_name,
        "price_usd": flight["price_usd"],
        "status": "Confirmed",
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    BOOKINGS.append(booking)
    return {"success": True, "booking": booking}


def search_hotels(location: str, checkin: str | None = None, checkout: str | None = None) -> list[dict]:
    loc = location.lower()
    results = [h for h in HOTELS if loc in h["location"].lower() or h["location"].lower() in loc]
    return results if results else HOTELS


def get_hotel(hotel_id: str) -> dict | None:
    for h in HOTELS:
        if h["id"].upper() == hotel_id.upper():
            return h
    return None


def check_availability(hotel_id: str, checkin: str, checkout: str) -> dict:
    hotel = get_hotel(hotel_id)
    if not hotel:
        return {"available": False, "error": f"Hotel {hotel_id} not found."}

    try:
        ci = datetime.strptime(checkin, "%Y-%m-%d")
        co = datetime.strptime(checkout, "%Y-%m-%d")
        nights = (co - ci).days
        if nights <= 0:
            return {"available": False, "error": "Check-out must be after check-in."}
    except ValueError:
        nights = 1

    total = hotel["price_per_night_usd"] * nights
    return {
        "available": True,
        "hotel_id": hotel_id,
        "hotel_name": hotel["name"],
        "checkin": checkin,
        "checkout": checkout,
        "nights": nights,
        "price_per_night_usd": hotel["price_per_night_usd"],
        "total_usd": total,
    }


def book_hotel(hotel_id: str, guest_name: str, checkin: str, checkout: str) -> dict:
    avail = check_availability(hotel_id, checkin, checkout)
    if not avail["available"]:
        return {"success": False, "error": avail.get("error", "Not available.")}

    hotel = get_hotel(hotel_id)
    booking = {
        "booking_id": "BKH-" + uuid.uuid4().hex[:8].upper(),
        "type": "hotel",
        "hotel_id": hotel_id,
        "hotel_name": hotel["name"],
        "location": hotel["location"],
        "guest": guest_name,
        "checkin": checkin,
        "checkout": checkout,
        "nights": avail["nights"],
        "price_per_night_usd": hotel["price_per_night_usd"],
        "total_usd": avail["total_usd"],
        "status": "Confirmed",
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    BOOKINGS.append(booking)
    return {"success": True, "booking": booking}
