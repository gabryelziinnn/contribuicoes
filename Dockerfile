FROM python:3.9.14-buster
LABEL author="Gabryel Bento"

WORKDIR /usr/src/app
COPY * ./

# Aponta as credenciais no container
ENV AWS_CONFIG_FILE /usr/src/app/config

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "vpc1.py" ] 