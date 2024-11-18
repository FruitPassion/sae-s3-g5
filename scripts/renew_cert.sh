#!/bin/bash
DOMAIN_NAME=$1
FOLDER_PATH=$2
cd $FOLDER_PATH/nginx/ssl
openssl req -new -newkey rsa:4096 -x509 -sha256 -nodes -subj "/C=FR/ST=France/L=Toulouse/O=APEAJ/OU=Aide/CN=$DOMAIN_NAME" -out certs/self_ssl_certs.pem -keyout private/self_ssl_certs.key
docker-compose exec nginx /bin/sh -c "nginx -s reload"