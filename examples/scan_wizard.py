from __future__ import print_function
import pprint
import sys
sys.path.insert(0, '..')
from openvasup.model import OpenvasObject
from openvasup.scan import Result
from openvasup.wizard import ScanWizard

# Start openvas with Docker to get things doing quick!
# `docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`
def main():
  pp = pprint.PrettyPrinter(indent=2)
  username ='admin'
  password ='admin'
  OpenvasObject.connect(host='172.17.0.4', username=username, password=password)

  wizard = ScanWizard()
  wizard.start({'host': '127.0.0.1'})

  for message in wizard.messages:
    print('[i] %s' % message)


  wizard.wait_for_tasks()


  results = wizard.results()

  print("name | host | port | threat | severity")
  for result in results:
    print(result.as_text())

main()
