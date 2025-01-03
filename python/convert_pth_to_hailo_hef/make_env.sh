#! /bin/bash

cat <<EOF > .env
UID=$(id -u)
GID=$(id -g)
UNAME=hailo
EOF
