from __future__ import print_function
import pprint
from sets import Set
import sys
sys.path.append("..")
from openvasup.model import OpenvasObject
from openvasup.scan import Result
from openvasup.asset import Asset
from openvasup.meta import Tag

# Start openvas with Docker to get things doing quick!
# `docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`
def main():
    """ Tag web server assets """
    pp = pprint.PrettyPrinter(indent=2)
    username = 'admin'
    password = 'admin'
    OpenvasObject.connect(username=username, password=password)

    asset_map = {a.name: a for a in Asset.get()}

    results = Result.get({'@filter': 'vulnerability="HTTP Server type and version" rows=2000'})
    hosts = Set([r.get_host() for r in results])

    for host in hosts:
        asset = asset_map.get(host)
        if asset is None:
            continue

        tag = Tag.attach(asset)
        tag.name = 'Services'
        tag.value = 'WebServer'
        success = tag.create_if_new()

        if success is not None:
            print('[i] Tagged host %s' % host)
        else:
            print('[i]Seems host %s was already tagged' % host)


if __name__ == "__main__":
    main()
