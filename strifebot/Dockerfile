FROM python:3.9.12-buster

WORKDIR /usr/src/strifebot

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "bot.py", "nan0bot.conf" ]
