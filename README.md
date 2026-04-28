# Travel Concierge — Multi-Agent Chatbot | Anthropic SDK

A multi-agent travel chatbot built with the **Anthropic Claude SDK** and **Streamlit**.  
Three collaborative AI agents handle destination advice, flight booking, and hotel booking — all driven by a Supervisor that routes requests intelligently with no hardcoded logic.

---

## Architecture

```
User (Streamlit UI)
        │
        ▼
  SupervisorAgent
        │
        │  Claude LLM detects intent — no hardcoded routing
        │
        ├── General query ──────────────► answers directly
        │
        ├── Flight / destination need ──► TravelAgent.run(task)
        │                                  search_destinations
        │                                  search_flights
        │                                  book_flight
        │
        └── Hotel need ─────────────────► HotelAgent.run(task)
                                           search_hotels
                                           check_availability
                                           book_hotel
```

### Key design decisions

| Decision | Rationale |
|----------|-----------|
| LLM-driven intent detection | Supervisor LLM decides when to delegate — no if/else routing in Python |
| Generic registry dispatch | Adding a new agent = one line in `agent_registry`, loop never changes |
| Agents as classes | Each agent has its own `run()` method, system prompt, tools, and API loop |
| Stateless sub-agents | Conversation memory lives in the Supervisor; sub-agents are stateless workers |
| Prompt caching | Supervisor system prompt uses `cache_control` to reduce latency |
| Local data only | All bookings and searches use the local in-memory database exclusively |

---

## Project Structure

```
agentic-ai-mod-7-demo-1/
├── src/
│   ├── app.py           — Streamlit chat UI
│   ├── supervisor.py    — SupervisorAgent (LLM routing + registry dispatch)
│   ├── travel_agent.py  — TravelAgent + flight tools
│   ├── hotel_agent.py   — HotelAgent + hotel tools
│   └── dummy_db.py      — In-memory mock database
├── plan.md              — Architecture and design decisions
├── pyproject.toml       — uv dependencies
└── .env                 — API key (not committed)
```

---

## Quickstart

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure API key

Edit `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run

```bash
uv run streamlit run src/app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Agents

### Supervisor
- Model: `claude-sonnet-4-6`
- Answers general destination and tourist questions directly
- Delegates to sub-agents only when needed via LLM tool calls
- Maintains full conversation history across all turns
- Returns `(reply_text, agents_called)` so the UI can show delegation indicators

### Travel Booking Agent
- Model: `claude-sonnet-4-6`
- **Tools:** `search_destinations`, `search_flights`, `book_flight`
- Covers 7 destinations and 12 flights in the local database

### Hotel Booking Agent
- Model: `claude-sonnet-4-6`
- **Tools:** `search_hotels`, `check_availability`, `book_hotel`
- Covers 10 hotels across 6 cities in the local database

---

## How the Agent Loop Works

```
1. User sends message
2. Supervisor Claude responds with stop_reason:
   ├── "end_turn"  → Claude has a final answer → return text to user
   └── "tool_use"  → Claude wants to delegate → call the sub-agent
3. Sub-agent (TravelAgent / HotelAgent) runs its own tool loop:
   ├── calls search/availability/book tools against local DB
   └── returns final text when stop_reason = "end_turn"
4. Sub-agent result is fed back to Supervisor
5. Supervisor summarises and returns to user
```

---

## Example Questions

```
"What's a good destination for a beach holiday?"
"Find me flights from New York to Tokyo"
"Find me flights from New York to Bali in June"
"Book flight F1009 for John Smith"
"Show me hotels in Tokyo"
"Show me hotels in Paris"
"Check availability for hotel H2009 from 2026-06-15 to 2026-06-20"
"Book hotel H2010 for Jane Doe, check-in 2026-06-18, check-out 2026-06-22"
"What's the best time to visit Kyoto?"
"What are the visa requirements for the Maldives?"
```

---

## Extending — Adding a New Agent

```python
# 1. Create src/car_rental_agent.py
class CarRentalAgent:
    def run(self, task: str) -> str:
        ...

# 2. Register in supervisor.py — one line
agent_registry = {
    "call_travel_agent":     TravelAgent(),
    "call_hotel_agent":      HotelAgent(),
    "call_car_rental_agent": CarRentalAgent(),  # ← add here
}

# 3. Add tool definition to TOOL_DEFINITIONS in supervisor.py
{
    "name": "call_car_rental_agent",
    "description": "Delegate car rental searches and bookings.",
    ...
}
```

The dispatch loop needs no other changes.

---

## Tech Stack

- [Streamlit](https://streamlit.io/) — chat UI
- [uv](https://docs.astral.sh/uv/) — Python package and project manager

## Anthropic SDK Features Used

| Feature | Where | What it does |
|---------|-------|--------------|
| `anthropic.Anthropic()` | All agents | Initialises the SDK client to talk to the Claude API |
| `client.messages.create()` | All agents | Sends a message to Claude and gets a response back |
| `tools=` parameter | All agents | Defines the list of tools Claude is allowed to call |
| `stop_reason: "tool_use"` | All agents | Claude signals it wants to call a tool before answering |
| `stop_reason: "end_turn"` | All agents | Claude signals it has a final answer ready for the user |
| `block.type == "tool_use"` | All agents | Detects which response blocks are tool call requests |
| `block.input` | All agents | Reads the arguments Claude chose for the tool call |
| `type: "tool_result"` | All agents | Sends tool output back to Claude so it can continue |
| `cache_control: ephemeral` | Supervisor | Caches the system prompt to reduce latency and cost |
| Multi-turn `messages` history | Supervisor | Passes the full conversation so Claude has context across turns |
