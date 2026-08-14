FROM python:3-alpine AS base

ENV VIRTUAL_ENV=/venv

FROM base AS build

RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
  apk add uv

COPY pyproject.toml uv.lock .

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --active --frozen --link-mode=copy

FROM base AS runtime

COPY --from=build /venv /venv

WORKDIR /app

COPY . .

USER nobody

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "cards"]
