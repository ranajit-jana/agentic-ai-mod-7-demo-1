import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from supervisor import SupervisorAgent

st.set_page_config(
    page_title="Travel Concierge",
    page_icon="✈️",
    layout="centered",
)

st.title("✈️ Travel Concierge")
st.caption("Ask me about destinations, flights, and hotels. I'll connect you with the right specialist.")

# -- session state -----------------------------------------------------------

if "agent" not in st.session_state:
    st.session_state.agent = SupervisorAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []          # list of {role, content, meta?}

# -- render chat history -----------------------------------------------------

AGENT_LABELS = {
    "call_travel_agent": "✈️ Travel agent consulted",
    "call_hotel_agent":  "🏨 Hotel agent consulted",
}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("delegated_to"):
            for agent_name in msg["delegated_to"]:
                st.caption(AGENT_LABELS.get(agent_name, agent_name))
        st.markdown(msg["content"])

# -- handle new input --------------------------------------------------------

if prompt := st.chat_input("Where would you like to go?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.caption("Thinking…")

        reply, agents_called = st.session_state.agent.run(prompt)

        status_placeholder.empty()

        if agents_called:
            for agent_name in agents_called:
                st.caption(AGENT_LABELS.get(agent_name, agent_name))

        st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "delegated_to": agents_called,
    })
