from flask import make_response

class Slash():

  def __init__(self, verifier):
    self.verifier = verifier

  def verify(self, request):
    return self.verifier.is_valid_request(request.get_data(), request.headers)

  def process(self, request):
    info = request.form



    try:
      response = slack_client.chat_postMessage(
        channel='#{}'.format(info["channel_name"]),
        text='aaaa'
      )#.get()
    except SlackApiError as e:
      logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
      logging.error(e.response)
      return make_response("", e.response.status_code)

    return make_response("", response.status_code)