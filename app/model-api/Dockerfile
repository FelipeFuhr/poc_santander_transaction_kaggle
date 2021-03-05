# First Stage

FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install python3-pip

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src .
COPY ./models ./models
COPY ./data ./data

RUN pip3 install pytest

ENTRYPOINT [ "pytest" ]

# Second Stage

FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install python3-pip

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src .
COPY ./models ./models
COPY ./data ./data
COPY ./tmp ./tmp
EXPOSE 9001

CMD [ "python3", "./app.py" ]
