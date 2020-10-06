import logging
from flask import Flask, request, make_response, Response
from slack.errors import SlackApiError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Slash():

  def __init__(self, verifier):
    self.verifier = verifier

  def verify(self, request):
    return self.verifier.is_valid_request(request.get_data(), request.headers)

  def processCommand(self, slack_client, info):
    if info['text'].startswith('create'):
      return processCreateCommand(slack_client, info)

  def processCreateCommand(self, slack_client, info):
    expiresDate = datetime.today() + relativedelta(months=+1)
    chanName = info['text'].replace('create ','')
    chanName = chanName.replace(' ','-')
    chanName = 'temp-' + chanName + '-' + expiresDate.strftime('%Y%m%d%H%M%S')

    try:
      slack_client.conversations_create(
        name=chanName
      )
    except SlackApiError as e:
      logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
      logging.error(e.response)
      return make_response("", e.response.status_code)

    responseMessage = 'Created new channel #' + chanName + ' which expires ' + expiresDate.strftime('%Y-%m-%d %H:%M:%S')
    try:
      if info["channel_name"] == 'directmessage':
        im_id = slack_client.conversations_open(
          users=info["user_id"]
        )["channel"]["id"]
        ownerMsg = slack_client.chat_postMessage(
          channel=im_id,
          text=responseMessage,
          link_names=1
        )
      else:
        slack_client.chat_postMessage(
          channel='#{}'.format(info["channel_name"]),
          text=responseMessage,
          link_names=1
        )
    except SlackApiError as e:
      logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
      logging.error(e.response)
      return make_response("", e.response.status_code)

    return make_response("", 200)