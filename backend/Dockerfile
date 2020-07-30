FROM python:3-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk update && apk add --no-cache mysql-client \
    libffi-dev musl-dev linux-headers gcc make
RUN pip install --no-cache-dir gunicorn gevent -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apk del libffi-dev musl-dev linux-headers gcc make
RUN pip install --no-cache-dir \
    flask flask-sqlalchemy flask-migrate flask-marshmallow flask-migrate \
    flask-restx sqlalchemy-utils marshmallow-sqlalchemy PyMySQL \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY docker-entrypoint /etc/docker-entrypoint
RUN chmod +x /etc/docker-entrypoint

WORKDIR /opt
ENTRYPOINT [ "/etc/docker-entrypoint" ]
