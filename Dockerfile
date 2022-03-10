FROM python:3.8-alpine as builder

ARG TIMEZONE=Europe/Moscow

RUN apk add --no-cache \
  tzdata \
  && ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
  && echo $TIMEZONE > /etc/timezone

COPY requirements.txt .
RUN pip install --prefix=/install -r ./requirements.txt


# ========== final image
FROM python:3.8-alpine as production
LABEL maintainer="https://github.com/strpc"

RUN apk add --no-cache curl

ENV PYTHONUNBUFFERED 1

RUN adduser --uid 1000 --home /app --disabled-password --gecos "" backend && \
    chown -hR backend: /app

WORKDIR /app

COPY --from=builder /etc/timezone /etc/timezone
COPY --from=builder /etc/localtime /etc/localtime
COPY --from=builder /install /usr/local

COPY --chown=backend:backend . /app

ENV PYTHONPATH=/app/app

RUN chmod +x ./entrypoint.sh

USER backend

ENTRYPOINT ["./entrypoint.sh"]
CMD ["prod"]
