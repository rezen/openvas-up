from __future__ import print_function
import sys
sys.path.insert(0, '..')
from openvasup.model import OpenvasObject
from openvasup.config import Alert, AlertCondition, AlertMethod, AlertEvent

def main():
  username ='admin'
  password ='admin'
  OpenvasObject.connect(username=username, password=password)

  for alert in Alert.get():

    print("\nName: %s" % alert.name)
    print("\nMethod:")
    print(" %s" % alert.method.method)
    print(" %s" % alert.method.data)

    print("\nCondition:")
    print(" %s" % alert.condition.event)
    print(" %s" % alert.condition.name)
    print(" %s" % alert.condition.value)

    print("\nEvent:")
    print(" %s" % alert.event.event)
    print(" %s" % alert.event.name)
    print(" %s" % alert.event.value)
    print('-' * 20)
  # exit()

  alert = Alert()
  alert.name = "What?! syslog"
  alert.condition = AlertCondition('Always')
  alert.event = AlertEvent(AlertEvent.TASK_CHANGED, 'status', 'Done')
  alert.method = AlertMethod('Syslog', { 
    'submethod': 'syslog',
    # 'start_task_task': '81961c59-188e-459e-bed9-fd09fb6ac420', 
    # 'details_url': 'https://secinfo.greenbone.net/omp?cmd=get_info&info_type=$t&info_id=$o&details=1&token=guest'
  })

  try:
    print(alert.save())
  except:
    print("\n[!] Alert already exists")
    exit(2)



main()
