import json
import anthropic
from dummy_db import search_hotels, check_availability, book_hotel

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a hotel booking specialist.

IMPORTANT: You MUST use the provided tools to fetch all data. Never invent, guess, or hallucinate hotel information — only return data that comes from a tool result. All bookings, availability checks, and hotel searches MUST use the local database exclusively — do NOT use or reference any external systems, live APIs, or outside data sources.

Rules:
- To find hotels → call search_hotels
- To check availability and total cost → call check_availability
- To book a hotel → call book_hotel
- You do NOT handle flights or travel bookings — politely note that flights are handled separately

Presentation:
- Always show prices in USD per night and total cost
- For hotels: include hotel ID, name, stars, price per night, amenities, and review score
- For bookings: clearly show the booking ID, total cost, and full confirmation details
- Be concise and friendly"""

TOOLS = [
    {
        "name": "search_hotels",
        "description": "Search available hotels by location with optional check-in and check-out dates.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City or destination name, e.g. 'Bali', 'Paris', 'New York'",
                },
                "checkin": {
                    "type": "string",
                    "description": "Check-in date in YYYY-MM-DD format (optional)",
                },
                "checkout": {
                    "type": "string",
                    "description": "Check-out date in YYYY-MM-DD format (optional)",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "check_availability",
        "description": "Check availability and total cost for a specific hotel and date range.",
        "input_schema": {
            "type": "object",
            "properties": {
                "hotel_id": {
                    "type": "string",
                    "description": "Hotel ID from search results, e.g. 'H2001'",
                },
                "checkin": {
                    "type": "string",
                    "description": "Check-in date in YYYY-MM-DD format",
                },
                "checkout": {
                    "type": "string",
                    "description": "Check-out date in YYYY-MM-DD format",
                },
            },
            "required": ["hotel_id", "checkin", "checkout"],
        },
    },
    {
        "name": "book_hotel",
        "description": "Book a hotel room for a guest.",
        "input_schema": {
            "type": "object",
            "properties": {
                "hotel_id": {
                    "type": "string",
                    "description": "Hotel ID from search results, e.g. 'H2001'",
                },
                "guest_name": {
                    "type": "string",
                    "description": "Full name of the guest",
                },
                "checkin": {
                    "type": "string",
                    "description": "Check-in date in YYYY-MM-DD format",
                },
                "checkout": {
                    "type": "string",
                    "description": "Check-out date in YYYY-MM-DD format",
                },
            },
            "required": ["hotel_id", "guest_name", "checkin", "checkout"],
        },
    },
]

TOOL_FUNCTIONS = {
    "search_hotels":      lambda args: search_hotels(
                                args["location"],
                                args.get("checkin"),
                                args.get("checkout"),
                           ),
    "check_availability": lambda args: check_availability(
                                args["hotel_id"],
                                args["checkin"],
                                args["checkout"],
                           ),
    "book_hotel":         lambda args: book_hotel(
                                args["hotel_id"],
                                args["guest_name"],
                                args["checkin"],
                                args["checkout"],
                           ),
}


class HotelAgent:
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
