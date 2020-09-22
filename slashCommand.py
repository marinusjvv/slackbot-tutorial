from pprint import pprint

class Slash():

  def __init__(self, verifier, client, info):
    self.verifier = verifier
    self.client = client
    self.info = info

  def verify(self, request):
    return self.verifier.is_valid_request(request.get_data(), request.headers)

  def process(self):
    pprint(info)
