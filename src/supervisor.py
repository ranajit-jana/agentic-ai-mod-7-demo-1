import json
import anthropic
from travel_agent import TravelAgent
from hotel_agent import HotelAgent

client = anthropic.Anthropic()

SYSTEM_PROMPT = [
    {
        "type": "text",
        "text": """You are a friendly and knowledgeable travel concierge.

You can directly answer general questions about:
- Travel destinations, cultures, visa requirements, best times to visit
- Tourist attractions, local food, things to do
- General travel tips and advice

For specialised tasks, you delegate to expert agents:
- Flight searches and bookings → call_travel_agent
- Hotel searches and bookings → call_hotel_agent

When delegating, write a clear focused task description for the agent that includes
all relevant details from the conversation (destination, dates, passenger/guest name,
budget preferences, etc.).

After receiving an agent's response, summarise it naturally for the user.
Always mention prices in USD. Be warm, concise, and helpful.""",
        "cache_control": {"type": "ephemeral"},
    }
]

TOOL_DEFINITIONS = [
    {
        "name": "call_travel_agent",
        "description": (
            "Delegate a travel or flight task to the travel booking specialist. "
            "Use this for: searching destinations, finding flights, booking flights."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": (
                        "A complete, self-contained task description for the travel agent. "
                        "Include destination, origin, dates, passenger name, and any preferences."
                    ),
                }
            },
            "required": ["task"],
        },
    },
    {
        "name": "call_hotel_agent",
        "description": (
            "Delegate a hotel task to the hotel booking specialist. "
            "Use this for: searching hotels, checking availability, booking hotels."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": (
                        "A complete, self-contained task description for the hotel agent. "
                        "Include location, check-in/check-out dates, guest name, and any preferences."
                    ),
                }
            },
            "required": ["task"],
        },
    },
]


class SupervisorAgent:
    def __init__(self):
        self.agent_registry = {
            "call_travel_agent": TravelAgent(),
            "call_hotel_agent":  HotelAgent(),
        }
        self.history: list[dict] = []

    def run(self, user_message: str) -> tuple[str, list[str]]:
        """
        Process a user message and return (reply_text, list_of_agents_called).
        agents_called is used by the UI to show delegation indicators.
        """
        self.history.append({"role": "user", "content": user_message})
        agents_called: list[str] = []

        while True:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS,
                messages=self.history,
            )

            self.history.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        return block.text, agents_called
                return "", agents_called

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    agent = self.agent_registry.get(block.name)
                    if agent is None:
                        result_text = json.dumps({"error": f"Unknown agent: {block.name}"})
                    else:
                        agents_called.append(block.name)
                        result_text = agent.run(block.input["task"])

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_text,
                    })

                self.history.append({"role": "user", "content": tool_results})
