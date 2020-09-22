import os
import json
import logging

from flask import Flask, request, make_response, Response

from slack.web.client import WebClient
from slack.errors import SlackApiError
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
  logging.debug('AAAAAAAAAAAAAAAAAAAAAA')
  logging.debug(info)

  # # send user a response via DM
  # im_id = slack_client.im_open(user=info["user_id"])["channel"]["id"]
  # ownerMsg = slack_client.chat_postMessage(
  #   channel=im_id,
  #   text=commander.getMessage()
  # )

  # # send channel a response
  # response = slack_client.chat_postMessage(
  #   channel='#{}'.format(info["channel_name"]),
  #   text=commander.getMessage()
  # )

  try:
    response = slack_client.conversations_create(
      name='temp-channel4'
    )
  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)
    return make_response("", e.response.status_code)

  try:
    response = slack_client.chat_postMessage(
      channel='#{}'.format(info["channel_name"]),
      text='Created new channel #temp-channel4',
      link_names=1
    )
  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)
    return make_response("", e.response.status_code)

  try:
    return commander.message(slack_client, info)
  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)
    return make_response("", e.response.status_code)

# Start the Flask server
if __name__ == "__main__":
  app.run()