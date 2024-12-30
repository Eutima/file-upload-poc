#!/bin/sh
mkdir -p keys
# openssl dhparam -out ./keys/dhparam.pem 2048 && \
openssl req -new -newkey rsa:2048 -nodes -keyout ./keys/server.key -out ./keys/server.csr && \
openssl x509 -signkey ./keys/server.key -in ./keys/server.csr -req -days 358000 -out ./keys/server.crt
