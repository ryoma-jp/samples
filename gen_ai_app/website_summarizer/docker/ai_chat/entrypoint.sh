#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -U "ai_chat_user"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

>&2 echo "Postgres is up - executing command"
exec $cmd
