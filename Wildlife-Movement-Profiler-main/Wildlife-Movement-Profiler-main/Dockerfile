# syntax=docker/dockerfile:1
FROM python:3.10-slim as base

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variable to select service: simulator, processor, dashboard, api
ENV SERVICE=api
ENV PORT=8000

CMD ["sh", "-c", "\
    if [ \"$SERVICE\" = \"simulator\" ]; then \
        python simulator/generator.py; \
    elif [ \"$SERVICE\" = \"processor\" ]; then \
        python -c 'from processor.preprocessing import preprocess; preprocess("simulated_telemetry.csv")'; \
    elif [ \"$SERVICE\" = \"dashboard\" ]; then \
        uvicorn dashboard.app:app --host 0.0.0.0 --port $PORT; \
    else \
        uvicorn api.main:app --host 0.0.0.0 --port $PORT; \
    fi"] 