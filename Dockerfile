FROM python:3.13 AS build

ARG python_version=3.13

SHELL ["/bin/sh", "-exc"]

RUN <<EOF
apt-get update --quiet
apt-get install --quiet --no-install-recommends --assume-yes \
  build-essential
EOF

COPY --link --from=ghcr.io/astral-sh/uv:0.6 /uv /usr/local/bin/uv

ENV UV_PYTHON="python$python_version" \
  UV_PYTHON_DOWNLOADS=never \
  UV_PROJECT_ENVIRONMENT=/app \
  UV_LINK_MODE=copy \
  UV_COMPILE_BYTECODE=1 \
  PYTHONOPTIMIZE=1

COPY pyproject.toml uv.lock /_project/

RUN --mount=type=cache,destination=/root/.cache/uv <<EOF
cd /_project
uv sync \
  --no-dev \
  --no-install-project \
  --frozen
EOF

ENV UV_PYTHON=$UV_PROJECT_ENVIRONMENT

COPY backend /_project/backend

RUN --mount=type=cache,destination=/root/.cache/uv <<EOF
cd /_project
uv sync \
  --no-dev \
  --no-editable \
  --frozen
EOF

FROM python:3.13-slim

ARG user_id=1000
ARG group_id=1000
ARG python_version=3.13

ENTRYPOINT ["/docker-entrypoint.sh"]
STOPSIGNAL SIGINT
EXPOSE 8080/tcp

SHELL ["/bin/sh", "-exc"]

RUN <<EOF
[ $user_id -gt 0 ] && user="$(id --name --user $user_id 2> /dev/null)" && userdel "$user"

if [ $group_id -gt 0 ]; then
  group="$(id --name --group $group_id 2> /dev/null)" && groupdel "$group"
  groupadd --gid $group_id app
fi

[ $user_id -gt 0 ] && useradd --uid $user_id --gid $group_id --home-dir /app app
EOF

RUN <<EOF
apt-get update --quiet
rm -rf /var/lib/apt/lists/*
EOF

ENV PATH=/app/bin:$PATH \
  PYTHONOPTIMIZE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1

COPY docker-entrypoint.sh /

COPY --link --chown=$user_id:$group_id --from=build /app/ /app
COPY ./backend/alembic /app/alembic
COPY ./backend/alembic.ini /app
COPY ./backend/src /app/src
RUN mkdir -p /app/storage && chown $user_id:$group_id -R /app/storage
RUN mkdir -p /app/logs && chown $user_id:$group_id -R /app/logs

USER $user_id:$group_id
WORKDIR /app
