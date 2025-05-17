import json
import os
import requests
import sseclient
from dotenv import load_dotenv
from constants import BASE_URI, HEADERS

load_dotenv()


class BotpressClient:
    def __init__(self, api_id=None, user_key=None):
        self.api_id = api_id or os.getenv("CHAT_API_ID")
        self.user_key = user_key or os.getenv("USER_KEY")
        self.base_url = f"{BASE_URI}/{self.api_id}"
        self.headers = {
            **HEADERS,
            "x-user-key": self.user_key,
        }

    def _request(self, method, path, json=None):
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, headers=self.headers, json=json)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return response.status_code, response.text

    # --- Core API Methods ---

    def get_user(self):
        return self._request("GET", "/users/me")

    def create_user(self, name, id):
        user_data = {"name": name, "id": id}
        return self._request("POST", "/users", json=user_data)

    def set_user_key(self, key):
        self.user_key = key
        self.headers["x-user-key"] = key

    def create_and_set_user(self, name, id):
        new_user = self.create_user(name, id)
        self.set_user_key(new_user["key"])

    def create_conversation(self):
        return self._request("POST", "/conversations", json={"body": {}})

    def list_conversations(self):
        return self._request("GET", "/conversations")

    def get_conversation(self, conversation_id):
        return self._request("GET", f"/conversations/{conversation_id}")

    def create_message(self, message, conversation_id):
        payload = {
            "payload": {"type": "text", "text": message},
            "conversationId": conversation_id,
        }
        return self._request("POST", "/messages", json=payload)

    def list_messages(self, conversation_id):
        return self._request("GET", f"/conversations/{conversation_id}/messages")

    def listen_conversation(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/listen"
        for event in sseclient.SSEClient(url, headers=self.headers):
            # print(event.data)
            if event.data == "ping":
                continue
            data = json.loads(event.data)["data"]
            yield {"id": data["id"], "text": data["payload"]["text"]}


if __name__ == "__main__":
    client = BotpressClient()
