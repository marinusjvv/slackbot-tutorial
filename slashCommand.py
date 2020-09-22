# basic starter code for a class that can be expanded to handle callbacks, attachents (buttons, etc) and more!
class Slash():

  def __init__(self, verifier):
    self.verifier = verifier

  def verify(request):
    return verifier.is_valid_request(request.get_data(), request.headers)

  def process(self):
      return self.msg
