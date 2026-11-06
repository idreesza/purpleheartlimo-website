# Purple Heart Limo — production image (Render, or any Docker host).
#
# Stage 1 builds the minified, cache-versioned assets into compiled-static/
# (needs Node for esbuild). Stage 2 runs server.py on the Python standard
# library only, without node_modules or build tooling.

FROM node:20-bookworm-slim AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ENV PYTHONUTF8=1
RUN python3 scripts/build_static_assets.py

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /app /app
RUN rm -rf /app/node_modules
ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PRODUCTION=1 \
    PORT=10000
EXPOSE 10000
CMD ["python3", "server.py"]
