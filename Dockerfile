FROM python:3-alpine

ENV \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=true \
  PIP_DISABLE_PIP_VERSION_CHECK=true

WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
USER nobody
EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "cards"]
