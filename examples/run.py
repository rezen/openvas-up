from __future__ import print_function
import pprint
import sys
sys.path.insert(0, '..')
from model import OpenvasObject
from wizard import ScanWizard

# Start openvas with Docker to get things doing quick!
# `docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`
def main():
  pp = pprint.PrettyPrinter(indent=2)
  username ='admin'
  password ='admin'
  OpenvasObject.connect(username=username, password=password)

  wizard = ScanWizard()
  wizard.start({'host': '127.0.0.1'})

  for message in wizard.messages:
    print('[i] %s' % message)

main()