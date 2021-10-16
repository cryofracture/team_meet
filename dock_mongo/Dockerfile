FROM mongo:latest
EXPOSE 27017
ADD init_scripts/mongo-init.js /docker-entrypoint-initdb.d/
WORKDIR /var/lib/mongodb
ENTRYPOINT ["/usr/bin/mongod"]
# VOLUME 
CMD ["--quiet"] 