from __future__ import print_function
import pprint
from sets import Set
import sys
sys.path.append("..")
from openvasup.model import OpenvasObject
from openvasup.scan import Report

# Start openvas with Docker to get things doing quick!
# `docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`
def main():
    pp = pprint.PrettyPrinter(indent=2)
    username = 'admin'
    password = 'admin'
    OpenvasObject.connect(username=username, password=password)

    reports = Report.get_by_host('127.0.0.1')
    report = reports.pop()
    results = report.get_results()

    for result in results:
        print(result.as_text())

if __name__ == "__main__":
    main()
