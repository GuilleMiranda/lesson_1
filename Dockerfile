FROM python:3.10-bookworm

WORKDIR /app

COPY . /app

ENV DB_HOSTNAME=$DB_HOSTNAME
ENV DB_PORT=$DB_PORT
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_NAME=$DB_NAME
ENV DB_USERNAME=$DB_USERNAME
ENV SECRET_KEY=$SECRET_KEY
ENV ALGORITHM=$ALGORITHM
ENV ACCESS_TOKEN_EXPIRY_MINUTES=$ACCESS_TOKEN_EXPIRY_MINUTES

RUN pip install --no-cache-dir -r requirements.txt && \
    python3 -m alembic upgrade head

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000" ]
