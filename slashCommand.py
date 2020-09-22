from pprint import pprint

class Slash():

  def __init__(self, verifier, slack_client, info):
    self.verifier = verifier
    self.slack_client = slack_client
    self.info = info

  def verify(self, request):
    return self.verifier.is_valid_request(request.get_data(), request.headers)

  def process(self):
    pprint(self.info)

  def send():
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
      response = self.slack_client.chat_postMessage(
        channel='#{}'.format(info["channel_name"]),
        text='aaaa'
      )#.get()
    except SlackApiError as e:
      logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
      logging.error(e.response)
      return make_response("", e.response.status_code)

    return make_response("", response.status_code)