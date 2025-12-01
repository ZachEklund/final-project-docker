#!/usr/bin/env bash
# run.sh - build and run docker container locally (one-liner)
set -e
IMAGE_NAME=blackjack-advisor:latest
docker build -t ${IMAGE_NAME} .
docker run --rm -p 8080:8080 --env-file .env ${IMAGE_NAME}