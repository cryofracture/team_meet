FROM ubuntu:latest
#COMMENT { "description": "mongodb service container",
# "usage": "docker run -d -p 27017:27017 --name mongodb mlamouri/mongodb --volume=/mydbdatadir:/var/lib/mongodb" }
RUN sudo apt update
RUN  sudo apt install -y mongodb-server
RUN  mkdir -p /var/lib/mongodb &&
    touch /var/lib/mongodb/.keep &&
    chown -R mongodb:mongodb /var/lib/mongodb
ADD mongodb.conf /etc/mongodb.conf
VOLUME [ "/var/lib/mongodb" ]
EXPOSE 27017
USER mongodb
WORKDIR /var/lib/mongodb
ENTRYPOINT ["/usr/bin/mongod", "--config", "/etc/mongodb.conf"]
CMD ["--quiet"]