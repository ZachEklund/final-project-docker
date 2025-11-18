# Flask Survey App – Docker Demo

This project is a Dockerized version of the survey app you built previously. It demonstrates how to containerize a Python Flask application so it can run consistently on any machine with Docker installed.

---

## Installation

If you don't have Docker yet, download it here:  
[Get Docker – Official Install Guide](https://www.docker.com/get-started/)

---

## What Does the Dockerfile Do?

The provided `Dockerfile` automates the following steps:

1. **Uses a lightweight Python base image** (`python:3.11-slim`).
2. **Sets up a working directory** inside the container.
3. **Copies your code and requirements** into the container.
4. **Installs Python dependencies** using `pip`.
5. **Exposes port 5000** (the Flask default).
6. **Runs your app** with `python app.py`.

This means you don't need to install dependencies on your own machine- just Docker (this will make grading your final projects a lot easier on us)!

---

## How to Run the App with Docker

### 1. Build the Docker image

From the project root, run:

```sh
docker build -t flask-survey-app .
```

### 2. Run the Docker container

```sh
docker run -p 5000:5000 flask-survey-app
```

### 3. Open the app in your browser

```sh
$BROWSER http://localhost:5000
```

## How to Stop a Docker Container

If you want to stop the running Docker container, just press `Ctrl+C` in the terminal where it's running.

Or, you can stop it from another terminal with:

```sh
docker ps          # Find your container's ID or name
docker stop <container_id_or_name>
```
---
Hopefully this helps you guys containerize your projects- good luck!
