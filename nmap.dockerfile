FROM ubuntu:22.10
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nmap

COPY requirements.txt /usr/src/bot
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/bot

CMD [ "python3", "auto_bot.py"  ]