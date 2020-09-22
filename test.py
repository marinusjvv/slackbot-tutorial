import os
from slack import WebClient
from slack.errors import SlackApiError

client = WebClient(token='xoxb-1390984204065-1371664617398-IbhhkgLW8bqYxEZo1ENDWzxs')

try:
    response = client.chat_postMessage(
        channel='#bots',
        text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")