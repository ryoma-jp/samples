#! /bin/bash

cat <<EOF > .env
UID=$(id -u)
GID=$(id -g)
UNAME=$(whoami)
DISPLAY=$DISPLAY
EOF