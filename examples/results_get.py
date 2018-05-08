from __future__ import print_function
from sets import Set
import sys
sys.path.append("..")
from openvasup.model import OpenvasObject
from openvasup.scan import Report

# Start openvas with Docker to get things doing quick!
# `docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`
def main():
    username = 'admin'
    password = 'admin'
    OpenvasObject.connect(username=username, password=password)

    reports = [r for r in Report.get_by_host('127.0.0.1') if 'OpenVAS' in r.task.name]
    report = reports[-1]
    print("Report:\n  %s\n" %  report.name)
    print("Task:\n  %s\n" % report.task.name)
    print("Results:")
   
    results = report.get_results()
    for result in results:
        print("  %s" %  result.as_text())

if __name__ == "__main__":
    main()
