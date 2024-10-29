# syntax=docker/dockerfile:1.10.0
FROM ubuntu:noble AS build

ENV DEBIAN_FRONTEND=noninteractive

ARG BUILD_PACKAGES="iverilog gtkwave"

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
        apt update && \
        apt install -y --no-install-recommends $BUILD_PACKAGES

WORKDIR /build
COPY . .