# syntax=docker/dockerfile:1.10.0
FROM python:3.11 AS build

ENV DEBIAN_FRONTEND=noninteractive

ARG BUILD_PACKAGES="iverilog gtkwave"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

SHELL ["/bin/bash", "-c"]
RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    --mount=type=cache,target=/root/.cache \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt update && \
    apt install -y --no-install-recommends build-essential $BUILD_PACKAGES &&\
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip twine wheel setuptools

FROM build AS dev
RUN pip install -e .[dev] && \

