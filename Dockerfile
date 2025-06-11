FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN pip install --no-cache-dir -U uv \
    && if [ -f uv.lock ]; then uv pip sync; else uv pip install --system; fi

COPY . .

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "-m", "planner_bot.main"]
