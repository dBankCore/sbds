FROM kennethreitz/pipenv

ENV DPAYD_HTTP_URL https://greatbase.dpaynodes.com
ENV DPDS_LOG_LEVEL INFO
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV APP_ROOT /app
ENV WSGI_APP ${APP_ROOT}/dpds/server/serve.py
ENV HTTP_SERVER_PORT 8080
ENV DPDS_APP_HTTP_PORT 9000

ENV PIPENV_DEFAULT_PYTHON_VERSION 3.6.4

ENV NGINX_SERVER_PORT 8080

RUN \
    apt-get update && \
    apt-get install -y \
        build-essential \
        checkinstall \
        daemontools \
        git \
        libbz2-dev \
        libc6-dev \
        libffi-dev \
        libgdbm-dev \
        libmysqlclient-dev \
        libncursesw5-dev \
        libreadline-gplv2-dev \
        libsqlite3-dev \
        libssl-dev \
        libxml2-dev \
        libxslt-dev \
        nginx \
        nginx-extras \
        make \
        lua-zlib \
        runit \
        tk-dev \
        wget && \
    apt-get clean


# nginx
RUN \
  mkdir -p /var/lib/nginx/body && \
  mkdir -p /var/lib/nginx/scgi && \
  mkdir -p /var/lib/nginx/uwsgi && \
  mkdir -p /var/lib/nginx/fastcgi && \
  mkdir -p /var/lib/nginx/proxy && \
  chown -R www-data:www-data /var/lib/nginx && \
  mkdir -p /var/log/nginx && \
  touch /var/log/nginx/access.log && \
  touch /var/log/nginx/access.json && \
  touch /var/log/nginx/error.log && \
  chown www-data:www-data /var/log/nginx/* && \
  touch /var/run/nginx.pid && \
  chown www-data:www-data /var/run/nginx.pid && \
  mkdir -p /var/www/.cache && \
  chown www-data:www-data /var/www/.cache

RUN \
    python -m pip3 install --upgrade pip && \
    python -m pip3 install pipenv

COPY . /app

RUN \
    mv /app/service/* /etc/service && \
    chmod +x /etc/service/*/run

WORKDIR /app

RUN pipenv install

RUN \
    apt-get remove -y \
        build-essential \
        libffi-dev \
        libssl-dev && \
    apt-get autoremove -y && \
    rm -rf \
        /root/.cache \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /var/cache/* \
        /usr/include \
        /usr/local/include

EXPOSE ${HTTP_SERVER_PORT}

