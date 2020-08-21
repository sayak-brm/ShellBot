#!/bin/bash

docker run -d \
    --name shellbot-server \
    -p 9999:9999 \
    -p 9090:9090 \
    --restart=unless-stopped \
    sayakbrm/shellbot-server:latest 9999 9090 password

printf 'Starting up shellbot-server container '
for i in $(seq 1 20); do
    if [ "$(docker inspect -f "{{.State.Health.Status}}" shellbot-server)" == "healthy" ] ; then
        printf ' OK'
        exit 0
    else
        sleep 3
        printf '.'
    fi

    if [ $i -eq 20 ] ; then
        echo -e "\nTimed out waiting for shellbot-server start, consult check your container logs for more info (\`docker logs shellbot-server\`)"
        exit 1
    fi
done;