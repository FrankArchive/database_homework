FROM python:3-alpine

RUN pip install \
    flask flask-sqlalchemy flask-migrate flask-restx sqlalchemy-utils \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY docker-entrypoint /etc/docker-entrypoint
RUN chmod +x /etc/docker-entrypoint

ENTRYPOINT [ "/etc/docker-entrypoint" ]
