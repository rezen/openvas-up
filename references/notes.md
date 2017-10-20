# OpenVAS

## nasl
- https://github.com/tenable/nasl
- http://www.vijaymukhi.com/seccourse/nasl.htm

```shell
openvas-nasl -B -d -x -T $ip /var/lib/openvas/plugins/nginx_detect.nasl
openvas-nasl -B -d -X -t 66.147.244.193 /var/lib/openvas/plugins/wp_detect.nasl
```

## Filters
- `name~"Name of Scan"`
- https://secinfo.greenbone.net/help/powerfilter.html?r=1&token=guest


## Installing
- https://avleonov.com/2017/04/10/installing-openvas-9-from-the-sources/
- http://muntashirsecurity.blogspot.com/2016/10/install-openvas-vulnerability-scanner.html
- http://www.arvinep.com/2015/11/openvas-security-and-vulnerability.html

## Postgres
https://www.ryanschulze.net/archives/1718
https://fossies.org/linux/openvas-manager/doc/postgres-HOWTO


## API
- http://docs.greenbone.net/API/OMP/omp-7.0.html

## Slave
- https://sysadmin-ramblings.blogspot.com/2017/04/openvas-9-distributed-setup.html
- https://blog.haardiek.org/setup-oScanpenvas-as-master-and-slave.html
- https://www.slideshare.net/JeremyCanale/vaaas
- https://github.com/vertexclique/openvas_tasks

## Agent
- https://localhost/help/glossary.html?token=6916c1ba-0dfa-40c9-98bb-d6b21f186573#agent

## Links
- https://medium.com/linode-cube/openvas-checking-for-holes-before-the-hackers-do-it-for-you-9ea5a4c01786
- https://www.open-scap.org/resources/documentation/perform-vulnerability-scan-of-rhel-6-machine/

```shell
echo | openssl s_client -showcerts -connect 192.168.99.100:443 2>/dev/null |     openssl x509 -text > openvas.crt
```
