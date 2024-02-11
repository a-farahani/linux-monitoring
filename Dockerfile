FROM python:3.12-slim-bookworm as builder
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN python -m venv /opt/venv &&\
    pip install -Ur requirements.txt

FROM python:3.12-slim-bookworm as runner
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .

ENTRYPOINT [ "python3" ]
CMD [ "check-host.py" ]
