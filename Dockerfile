FROM alpine:3.10

ENV PYTHONDONTWRITEBYTECODE=1
RUN apk add --no-cache python3 py3-flask py3-gunicorn

WORKDIR /
COPY . .
USER nobody
EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "cards"]
