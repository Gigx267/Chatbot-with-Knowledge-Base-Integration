# Streamlit Chatbot using the Botpress Chat API

Code for running a stream-lit chatbot.

- An unofficial python client for the Botpress [Chat API](https://botpress.com/docs/api-reference/chat-api/introduction)
- Boilerplate code for running a bot in Streamlit, adapted from the [Streamlit chatbot guide](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps#build-a-chatgpt-like-app).

## Setup

Following the [Chat API guide](https://botpress.com/docs/api-reference/chat-api/introduction).

### 1. Create a secrets file

Secrets are kept in `.streamlit/secrets.toml`.

- Store the CHAT_API_ID in your secrets file:

```toml
CHAT_API_ID=<YOUR_CHAT_API_ID>
```

### 2. Create a user

run `python create_user.py --name NAME --id ID` to create a new user. The details, inclduing the `x-user-key` will be stored in `.streamlit/secrets.toml`.
Think `--id` as a username, and `--name` as the name you'd like to go by. For example, I'd do:

`python create_user.py --name Ben --id benbotluks`

### 3. Run the Streamlit app

`python -m streamlit run app.py`

...and you're good to go!
