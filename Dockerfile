FROM ubuntu:latest
MAINTAINER Komarov Leonid
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]