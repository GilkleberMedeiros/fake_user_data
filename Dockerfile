FROM python:3.12.9-slim-bookworm

ENTRYPOINT [ "fastapi", "run", "--workers", "2", "--port", "80", "./app/main.py" ]

WORKDIR /app

COPY . .

RUN python3 -m pip install -r requirements.txt

EXPOSE 80

CMD [ ]
