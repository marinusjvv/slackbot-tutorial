import os
import json
import logging

from flask import Flask, request, make_response, Response

from slack.web.client import WebClient
from slack.signature import SignatureVerifier

from slashCommand import Slash

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route("/slack/test", methods=["POST"])
def command():
  SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
  SLACK_SIGNATURE = os.environ['SLACK_SIGNATURE']

  verifier = SignatureVerifier(SLACK_SIGNATURE)
  commander = Slash(verifier)
  if not commander.verify(request):
    return make_response("invalid request", 403)

  slack_client = WebClient(SLACK_BOT_TOKEN)
  info = request.form
  return commander.processCommand(slack_client, info)

# Start the Flask server
if __name__ == "__main__":
  app.run()