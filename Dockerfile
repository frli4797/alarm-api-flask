# this is an official Python runtime, used as the parent image
FROM python:3.6-alpine

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# execute everyone's favorite pip command, pip install -r
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh && \
    pip install --trusted-host pypi.python.org -r requirements.txt 

# execute the Flask app
CMD ["python3", "alarmservice/app.py"]
