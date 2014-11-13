FROM debian:wheezy
MAINTAINER jj <somemail@mail.com>
ENV DEBIAN_FRONTEND noninteractive
RUN  apt-get update && apt-get -y install python-flask unzip &&  rm -rf /var/lib/apt/lists/* 
ADD https://github.com/httpPrincess/fakedEpicServer/archive/master.zip /app/
WORKDIR /app/
RUN unzip master.zip && rm master.zip 
EXPOSE 5000 
WORKDIR /app/fakedEpicServer-master/
CMD python simpleEpic.py


