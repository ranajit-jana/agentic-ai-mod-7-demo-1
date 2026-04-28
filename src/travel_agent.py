import json
import anthropic
from dummy_db import search_destinations, search_flights, book_flight

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a travel and flight booking specialist.

IMPORTANT: You MUST use the provided tools to fetch all data. Never invent, guess, or hallucinate destination or flight information — only return data that comes from a tool result.

Rules:
- To find destinations → call search_destinations
- To find flights → call search_flights
- To book a flight → call book_flight
- You do NOT handle hotel bookings — politely note that hotels are handled separately

Presentation:
- Always show prices in USD
- For flights: include flight ID, airline, route, date, departure/arrival times, price, seats available
- For bookings: clearly show the booking ID and full confirmation details
- Be concise and friendly"""

TOOLS = [
    {
        "name": "search_destinations",
        "description": "Search travel destinations by keyword (beach, mountain, city name, country, climate, etc.).",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keyword, e.g. 'beach', 'tropical', 'Europe', 'Bali'",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "search_flights",
        "description": "Search available flights by origin, destination, and optional date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Departure city or airport, e.g. 'New York', 'London'",
                },
                "destination": {
                    "type": "string",
                    "description": "Destination city or airport, e.g. 'Bali', 'Paris'",
                },
                "date": {
                    "type": "string",
                    "description": "Travel date in YYYY-MM-DD format (optional)",
                },
            },
            "required": ["origin", "destination"],
        },
    },
    {
        "name": "book_flight",
        "description": "Book a specific flight by its ID for a passenger.",
        "input_schema": {
            "type": "object",
            "properties": {
                "flight_id": {
                    "type": "string",
                    "description": "Flight ID from search results, e.g. 'F1001'",
                },
                "passenger_name": {
                    "type": "string",
                    "description": "Full name of the passenger",
                },
            },
            "required": ["flight_id", "passenger_name"],
        },
    },
]

TOOL_FUNCTIONS = {
    "search_destinations": lambda args: search_destinations(args["query"]),
    "search_flights":      lambda args: search_flights(
                                args["origin"],
                                args["destination"],
                                args.get("date"),
                           ),
    "book_flight":         lambda args: book_flight(args["flight_id"], args["passenger_name"]),
}


class TravelAgent:
    def run(self, task: str) -> str:
        messages = [{"role": "user", "content": task}]

        while True:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        return block.text
                return ""

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        fn = TOOL_FUNCTIONS.get(block.name)
                        result = fn(block.input) if fn else {"error": f"Unknown tool: {block.name}"}
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        })
                messages.append({"role": "user", "content": tool_results})
