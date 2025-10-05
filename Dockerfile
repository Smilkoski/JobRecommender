# Stage 1: Builder (install deps)
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (lightweight)
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Gunicorn for prod-like serving (install in reqs if not)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "job_recommender.wsgi:application"]