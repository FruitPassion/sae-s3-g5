FROM python:3.12-bookworm

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 netcat-traditional sqlite3 libsqlite3-dev -y 

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh && chmod +x /usr/src/app/entrypoint.sh


ENTRYPOINT ["/usr/src/app/entrypoint.sh"]