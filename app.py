# app.py

from client import BotpressClient
import streamlit as st

st.title("Botpress Front-end for Streamlit")

client = BotpressClient(
    api_id=st.secrets["CHAT_API_ID"], user_key=st.secrets["users"][0]["key"]
)

# user info
user = client.get_user()
user_id = user["user"]["id"]

# conversations
conversations = client.list_conversations()["conversations"]
conversation_ids = [conv["id"] for conv in conversations]


def create_conversation():
    res = client.create_conversation()
    print(f"Created new conversation: {res}")
    conversation_id = res["conversation"]["id"]
    st.session_state.active_conversation = conversation_id
    st.session_state.messages = []
    st.rerun()


if not conversations:
    create_conversation()

if "active_conversation" not in st.session_state:
    st.session_state["active_conversation"] = conversations[0]["id"]


col1, col2 = st.columns([5, 1])
with col1:
    conversation_id = st.selectbox(
        "Select Conversation",
        options=[conv["id"] for conv in conversations],
        index=conversation_ids.index(st.session_state.active_conversation),
    )

with col2:
    st.markdown("<div style='height: 1.9em'></div>", unsafe_allow_html=True)
    if st.button("➕"):
        create_conversation()

selected_conversation = client.get_conversation(conversation_id)

if (
    "messages" not in st.session_state
    or st.session_state.get("active_conversation") != conversation_id
):
    st.session_state.active_conversation = conversation_id
    st.session_state.messages = []

    messages = client.list_messages(conversation_id)
    next_token = messages["meta"].get("nextToken")

    for message in messages["messages"][::-1]:
        role = "user" if message["userId"] == user_id else "assistant"
        text = message["payload"]["text"]
        st.session_state.messages.append({"role": role, "content": text})

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("*wine*-d it up"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    client.create_message(prompt, conversation_id=conversation_id)

    with st.chat_message("assistant"):
        response_box = st.empty()
        last_rendered = ""

        for message in client.listen_conversation(st.session_state.active_conversation):

            message_id = message["id"]
            message_text = message["text"]

            if message_id != last_rendered:
                last_rendered = message_id
                response_box.markdown(message_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": message_text}
                )
