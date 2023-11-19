FROM python:3.9.18

LABEL Maintainer="dydkina"

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./
COPY data ./data

CMD [ "python", "./main.py"]