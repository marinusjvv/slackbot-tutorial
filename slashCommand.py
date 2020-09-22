# basic starter code for a class that can be expanded to handle callbacks, attachents (buttons, etc) and more!
class Slash():

  def __init__(self, verifier):
    self.verifier = verifier

  def verify(self, request):
    return self.verifier.is_valid_request(request.get_data(), request.headers)