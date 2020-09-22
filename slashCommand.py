from flask import Flask, request, make_response, Response

class Slash():

  def __init__(self, verifier):
    self.verifier = verifier

  def verify(self, request):
    return self.verifier.is_valid_request(request.get_data(), request.headers)

  def message(self, slack_client):
    response = slack_client.conversations_create(
      name='temp-channel3'
    )
