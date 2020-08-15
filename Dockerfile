FROM python:3.7-slim-buster
RUN apt-get update && apt-get install -y git
#TODO
RUN git clone -b 1.3.1 https://github.com/obrigg/cisco-dnac-platform-syslog-notifications.git
WORKDIR /cisco-dnac-platform-syslog-notifications/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "run.py"]
