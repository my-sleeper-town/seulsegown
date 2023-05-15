FROM python:3-slim

ENV KAKAO_REST_KEY ''
ENV KAKAO_JS_KEY ''
ENV SECRET_KEY ''
ENV DEBUG 'False'
ENV ALLOWED_HOSTS 'localhost 127.0.0.1'

# install nginx
RUN apt-get update && apt-get install nginx -y

COPY ./docker/nginx.conf /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/sites-enabled/*
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install pip --upgrade && \
    /opt/venv/bin/python -m pip install -r requirements.txt

# copy project
COPY . .

RUN mkdir /var/log/gunicorn
RUN chmod +x docker/entrypoint.sh

CMD ["./docker/entrypoint.sh"]

EXPOSE 80
