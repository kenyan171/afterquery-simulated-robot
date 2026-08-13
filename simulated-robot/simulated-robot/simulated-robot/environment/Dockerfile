FROM python:3.13-slim-bookworm

WORKDIR /app

COPY robot.py /app/robot.py
COPY experiment.py /app/experiment.py

RUN mkdir -p /app

CMD ["python", "-c", "print('robot environment ready')"]
