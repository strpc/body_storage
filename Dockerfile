FROM python:3.9-alpine as builder

ARG TIMEZONE=Europe/Moscow

RUN apk add --no-cache \
  tzdata \
  && ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
  && echo $TIMEZONE > /etc/timezone

COPY requirements.txt .
RUN pip install --prefix=/install -r ./requirements.txt


# ========== final image
FROM python:3.9-alpine as production
LABEL maintainer="https://github.com/strpc"

RUN apk add --no-cache curl

RUN adduser --uid 1000 --home /src --disabled-password --gecos "" backend && \
    chown -hR backend: /src

WORKDIR /src

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src

COPY --from=builder /etc/timezone /etc/timezone
COPY --from=builder /etc/localtime /etc/localtime
COPY --from=builder /install /usr/local

COPY --chown=backend:backend ./app /src/app
COPY --chown=backend:backend ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh

USER backend

ENTRYPOINT ["./entrypoint.sh"]
CMD ["prod"]
