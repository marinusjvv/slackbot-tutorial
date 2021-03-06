import logging
from flask import Flask, request, make_response, Response
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Slash():

  def __init__(self, verifier):
    self.verifier = verifier

  def verify(self, request):
    return self.verifier.is_valid_request(request.get_data(), request.headers)

  def processCommand(self, slack_client, info):
    if info['text'].startswith('create'):
      self.processCreateCommand(slack_client, info)
      return
    if info['text'].startswith('bump'):
      self.processBumpCommand(slack_client, info)
      return

    self.processHelpCommand(slack_client, info)

  def processCreateCommand(self, slack_client, info):
    expiresDate = datetime.today() + relativedelta(months=+1)
    chanName = info['text'].replace('create ','')
    chanName = chanName.replace(' ','-')
    chanName = 'temp-' + chanName + '-' + expiresDate.strftime('%Y%m%d%H%M%S')

    slack_client.conversations_create(
      name=chanName
    )

    responseMessage = 'Created new channel #' + chanName + ' which expires ' + expiresDate.strftime('%Y-%m-%d %H:%M:%S')
    self.sendResponse(info["channel_name"], slack_client, info, responseMessage)

  def processBumpCommand(self, slack_client, info):
    channelName = info["channel_name"]
    if not channelName.startswith('temp-'):
      return self.sendResponse(info["channel_name"], slack_client, info, 'Please use this command from a temporary channel')

    expires = channelName.rpartition('-')[-1]
    expiresDate = datetime.strptime(expires, '%Y%m%d%H%M%S')
    expiresDate = expiresDate + relativedelta(weeks=+2)

    newChannelName = channelName.replace(expires, expiresDate.strftime('%Y%m%d%H%M%S'))

    slack_client.conversations_rename(
      channel=info["channel_id"],
      name=newChannelName
    )
    self.sendResponse(newChannelName, slack_client, info, 'Channel bumped, new expiration date ' + expiresDate.strftime('%Y-%m-%d %H:%M:%S'))

  def processHelpCommand(self, slack_client, info):
    block = [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "Some useful commands"
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "`create <channel name>` - Creates a temporary channel. Default life is 2 weeks"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "`bump` - Extends current channel's lifetime with 2 weeks"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "`delete` - Archives the current channel"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "`permanent` - Requests that this channel be changed to a permanent channel"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "`help` - Shows this help section"
        }
      }
    ]
    self.sendResponse(info["channel_name"], slack_client, info, block, 'blocks')

  def sendResponse(self, channelName, slack_client, info, responseMessage, type = 'text'):
    if channelName == 'directmessage':
      outChannel = slack_client.conversations_open(
        users=info["user_id"]
      )["channel"]["id"]
    else:
      outChannel = '#{}'.format(channelName)

    kwargs = {
      "channel": outChannel,
      "link_names": 1,
    }
    kwargs[type] = responseMessage
    slack_client.chat_postMessage(**kwargs)