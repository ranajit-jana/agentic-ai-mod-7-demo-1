# Plan: Multi-Agent Travel Chatbot with Claude SDK + Streamlit

## Goal
Build a Streamlit chat application using the Anthropic Claude SDK.
Three agents: **Supervisor**, **Travel Booking Agent**, **Hotel Booking Agent**.
All booking data comes from a realistic in-memory dummy database.

---

## Architecture

```
Browser (Streamlit UI)
      │  user types message
      ▼
app.py  →  SupervisorAgent.run(user_message)
                │
                │  LLM analyses intent — no hardcoded routing
                │
                ├── intent: general info   → LLM answers directly
                │
                ├── intent: travel needed  → tool call "call_travel_agent"
                │                                  │
                │                          agent_registry lookup
                │                                  │
                │                          TravelAgent.run(task)
                │                            ├── search_destinations(query)   ┐
                │                            ├── search_flights(...)          ├── dummy_db.py
                │                            └── book_flight(...)             ┘
                │
                └── intent: hotel needed   → tool call "call_hotel_agent"
                                                   │
                                           agent_registry lookup
                                                   │
                                           HotelAgent.run(task)
                                             ├── search_hotels(...)           ┐
                                             ├── check_availability(...)      ├── dummy_db.py
                                             └── book_hotel(...)              ┘
```

---

## Project Structure

```
agentic-ai-mod-7-demo-1/
├── plan.md
├── pyproject.toml           ← uv-managed: anthropic, streamlit, python-dotenv
├── .env                     ← ANTHROPIC_API_KEY
└── src/
    ├── app.py               ← Streamlit UI + session state
    ├── supervisor.py        ← SupervisorAgent class
    ├── travel_agent.py      ← TravelAgent class + tool implementations
    ├── hotel_agent.py       ← HotelAgent class + tool implementations
    └── dummy_db.py          ← All mock data (destinations, flights, hotels, bookings)
```

---

## Dummy Database (`dummy_db.py`)

Realistic in-memory data simulating a real DB. All tools query this module.

### Destinations
```
ID   | Name              | Country      | Climate   | Best season | Avg daily budget | Highlights
-----|-------------------|--------------|-----------|-------------|------------------|----------------------------
D001 | Bali              | Indonesia    | Tropical  | Apr–Oct     | $80–$150/day     | Temples, beaches, rice fields
D002 | Paris             | France       | Temperate | Mar–May     | $200–$350/day    | Eiffel Tower, museums, cuisine
D003 | Maldives          | Maldives     | Tropical  | Nov–Apr     | $400–$800/day    | Overwater bungalows, coral reefs
D004 | New York          | USA          | Temperate | Sep–Nov     | $250–$450/day    | Times Square, Central Park
D005 | Kyoto             | Japan        | Temperate | Mar–May     | $120–$220/day    | Shrines, cherry blossoms
D006 | Cape Town         | South Africa | Mild      | Nov–Feb     | $100–$180/day    | Table Mountain, wine tours
```

### Flights (one-way, per person)
```
ID    | From    | To      | Date       | Airline       | Departs | Arrives | Price  | Seats
------|---------|---------|------------|---------------|---------|---------|--------|------
F1001 | NYC     | Bali    | 2026-06-10 | Singapore Air | 09:00   | 18:30+1 | $850   | 12
F1002 | NYC     | Bali    | 2026-06-12 | Emirates      | 22:00   | 08:15+2 | $720   | 4
F1003 | NYC     | Paris   | 2026-06-10 | Air France    | 19:00   | 08:30+1 | $620   | 20
F1004 | NYC     | Paris   | 2026-06-15 | Delta         | 11:00   | 00:45+1 | $580   | 8
F1005 | NYC     | Tokyo   | 2026-06-10 | ANA           | 13:00   | 16:30+1 | $950   | 6
F1006 | London  | Bali    | 2026-06-11 | Qatar Airways | 08:00   | 05:30+1 | $780   | 15
```

### Hotels
```
ID    | Name                   | Location  | Stars | Price/night | Amenities
------|------------------------|-----------|-------|-------------|---------------------------
H2001 | The Mulia              | Bali      | 5★    | $320        | Pool, spa, beach, restaurant
H2002 | Alaya Resort           | Bali      | 4★    | $180        | Pool, yoga, rice field view
H2003 | Hotel Le Marais        | Paris     | 4★    | $210        | City center, rooftop bar
H2004 | Shangri-La Paris       | Paris     | 5★    | $550        | Eiffel view, spa, Michelin dining
H2005 | The Peninsula          | New York  | 5★    | $695        | Midtown, rooftop pool, fine dining
H2006 | citizenM Times Square  | New York  | 3★    | $195        | Smart rooms, rooftop bar
H2007 | Gion Hatanaka          | Kyoto     | 5★    | $480        | Traditional ryokan, kaiseki dining
H2008 | The Table Bay          | Cape Town | 5★    | $290        | V&A Waterfront, mountain view
```

### Bookings (confirmation store — starts empty, grows as user books)
```
Booking ID | Type   | Details snapshot  | Status
-----------|--------|-------------------|----------
(empty)    |        |                   |
```

---

## Agent Details

### SupervisorAgent
| Item | Detail |
|------|--------|
| Model | `claude-sonnet-4-6` |
| System prompt | Friendly travel concierge; answers general destination/tourist questions; delegates bookings |
| Tool definitions | `call_travel_agent(task)`, `call_hotel_agent(task)` |
| Dispatch | Generic registry loop — never hardcoded |
| Memory | Full `history` list across all Streamlit session turns |
| Prompt caching | System prompt marked with `cache_control` |

### TravelAgent
| Item | Detail |
|------|--------|
| Model | `claude-sonnet-4-6` |
| System prompt | Travel & flight booking specialist |
| Tools | `search_destinations(query)`, `search_flights(origin, destination, date)`, `book_flight(flight_id, passenger_name)` |
| Data source | `dummy_db.py` |

### HotelAgent
| Item | Detail |
|------|--------|
| Model | `claude-sonnet-4-6` |
| System prompt | Hotel booking specialist |
| Tools | `search_hotels(location, checkin, checkout)`, `check_availability(hotel_id, dates)`, `book_hotel(hotel_id, guest_name, checkin, checkout)` |
| Data source | `dummy_db.py` |

---

## Streamlit UI (`app.py`)

- `st.chat_message` bubbles for user and assistant
- `st.chat_input` for user entry
- `st.session_state` holds `SupervisorAgent` instance + message display list
- Spinner shown while agents are running
- Agent delegation visually indicated (e.g. "Consulting travel agent…")

---

## Implementation Steps

1. **Setup** — `uv init`, `uv add anthropic streamlit python-dotenv`
2. **dummy_db.py** — all mock data + query helper functions
3. **travel_agent.py** — TravelAgent class, tool implementations querying dummy_db
4. **hotel_agent.py** — HotelAgent class, tool implementations querying dummy_db
5. **supervisor.py** — SupervisorAgent with generic registry dispatch loop
6. **app.py** — Streamlit chat UI wired to SupervisorAgent
7. **Run** — `uv run streamlit run src/app.py`
