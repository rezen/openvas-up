#!/usr/bin/env python
from __future__ import print_function
import time
from openvasup.omp import OmpConnection

host = 'openvas'
port = 9390
username = 'admin'
password = 'admin'
connected = False
timeout = 10
start = time.time()
spent = 0

print('Trying to connect to openvas at %s' % host)


while not connected:
  try:
    # select name, password from users;
    conn = OmpConnection(host=host, port=port, username=username, password=password)
    conn.open(username, password)
    print("Connected!")
    connected = True
  except:
    print("Still waiting ...")
    spent = spent + 1
    time.sleep(60)
    continue

  try:
    request = conn.command_dict('get_nvts', {})
    print(request.get_status_text())
    print(request.get_response_data())
  except:
    connected = False

  if spent >=  timeout:
    exit(0)


end = time.time()
print("Took %s to connect" % (end - start))
exit(0)