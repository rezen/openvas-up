# openvas-up
Takes interacting with OpenVAS up to the next level. The library enables you to interact with the OpenVAS manager via it's custom protocol,  omp. The goal is to be simple and readable.

```python
from openvasup.model import OpenvasObject
from openvasup.scan import Task

# Default creds for Docker image  mikesplain/openvas
username = 'admin'
password = 'admin'

# Login
OpenvasObject.connect(username=username, password=password)

# Get scan tasks
tasks = Task.get_by_name("Scan of 127.0.0.1")

``` 

## Requirements
- Python
- OpenVAS 9

## Getting Started
I've done most of the development with Docker which makes getting going with OpenVAS pretty quick.

`docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`

There is an example you can run in the `examples/` directory.

## Ideas
- Automatically tag asset hosts based on scan results