FROM python:2.7

WORKDIR /app
COPY ./setup.py /app/setup.py
COPY ./wait.py /app/wait.py
COPY ./tests /app/tests
COPY ./openvasup /app/openvasup
COPY ./examples /app/examples
RUN pip install /app

ENV SCAN_TARGET="" \ 
    SCAN_NAME="" \
    SCAN_OS=linux \
    SCAN_TIMEOUT=60

CMD [ "python", "/app/examples/scan_wizard.py" ]
