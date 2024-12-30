FROM python:3.11-alpine

RUN apk update && apk upgrade --no-cache
RUN apk add gettext postgresql-libs gcc musl-dev postgresql-dev busybox openrc su-exec

# Install dependencies for wkhtmltopdf
RUN apk add --no-cache \
    libstdc++ \
    libx11 \
    libxrender \
    libxext \
    libssl3 \
    ca-certificates \
    fontconfig \
    freetype \
    ttf-dejavu \
    ttf-droid \
    ttf-freefont \
    ttf-liberation \
  && apk add --no-cache --virtual .build-deps \
    msttcorefonts-installer \
  && update-ms-fonts \
  && fc-cache -f \
  && rm -rf /tmp/* \
  && apk del .build-deps

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=false
ENV DJANGO_LOGGING_DIR='/var/log/portal/'
ENV DJANGO_DB_DIR='/var/data/portal/db'
ENV DJANGO_STATIC_DIR='/var/data/portal/static'
ENV DJANGO_MEDIA_DIR='/var/data/portal/media'
RUN mkdir -p ${DJANGO_LOGGING_DIR}
RUN mkdir -p ${DJANGO_DB_DIR}
RUN mkdir -p ${DJANGO_STATIC_DIR}
RUN mkdir -p ${DJANGO_MEDIA_DIR}

WORKDIR /opt/app

COPY requirements.txt /opt/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /opt/app/

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown appuser:appgroup ${DJANGO_LOGGING_DIR} -R
RUN chown appuser:appgroup ${DJANGO_DB_DIR} -R
RUN chown appuser:appgroup ${DJANGO_STATIC_DIR} -R
RUN chown appuser:appgroup ${DJANGO_MEDIA_DIR} -R

CMD ["./entrypoint-user.sh"]
